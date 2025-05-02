# nations/tasks.py
# Defines Celery background tasks for the nations app, like AI generation.

from celery import shared_task
from decouple import config
import time
import google.generativeai as genai

from .models import Nation, NationGenerationStatus # Database model and status enums

# Import the shared Vertex AI client objects and config
from .vertex_client import (
    vertex_ai_endpoint_nation,
    guideline_vertex_ai_endpoint,
    VERTEX_DEPLOYED_INDEX_ID,
    GUIDELINE_VERTEX_DEPLOYED_INDEX_ID
    # GCP_PROJECT_ID, GCP_REGION - Import only if task needs them directly
)

# --- Configure Gemini API ---
# It's often best practice to configure this once globally (e.g., in celery.py)
# If not configured globally, configure it here when the task runs.
try:
    TASK_GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)
    if TASK_GEMINI_API_KEY:
        # Simple check to avoid reconfiguring if already done globally
        if not getattr(genai, '_client', None):
             genai.configure(api_key=TASK_GEMINI_API_KEY)
             print("Gemini API Key configured in tasks.")
        else:
             print("Gemini API Key already configured, skipping in tasks.")
    else:
        # This task cannot run without the API key.
        print("CRITICAL WARN: tasks.py: GEMINI_API_KEY not found. AI generation will fail.")
except NameError:
    print("ERROR: tasks.py: google-generativeai library not found. Run pip install google-generativeai")
except Exception as e:
    print(f"Error configuring Gemini API in tasks: {e}")
# --- End Gemini Config ---


@shared_task(bind=True) # bind=True gives access to task instance (self)
def generate_nation_dm_task(self, nation_id):
    """
    Celery background task to generate Dominions 6 mod code for a Nation.
    Uses RAG with Vertex AI Matching Engine and Gemini for generation.
    Updates the Nation object's status and results in the database.
    """
    task_id = self.request.id
    print(f"Starting task {task_id} for Nation ID: {nation_id}")
    nation = None

    # --- Initial Setup & Status Update ---
    try:
        nation = Nation.objects.get(pk=nation_id)
        # Mark the nation as generating in the database
        nation.generation_status = NationGenerationStatus.GENERATING
        nation.generation_task_id = task_id
        nation.generated_dm_code = None # Clear previous results
        nation.generation_error = None
        nation.last_prompt_used = None # Clear previous prompt
        nation.save(update_fields=['generation_status', 'generation_task_id', 'generated_dm_code', 'generation_error', 'last_prompt_used'])
    except Nation.DoesNotExist:
        print(f"Error [Task {task_id}]: Nation with ID {nation_id} not found. Task cannot proceed.")
        # No nation to update, so the task simply fails here.
        return f"Task {task_id} failed: Nation ID {nation_id} not found."
    except Exception as setup_e:
        print(f"Error [Task {task_id}]: Initial DB update failed: {setup_e}")
        # Try to mark failure if possible, otherwise task fails hard.
        try:
            nation.generation_status = NationGenerationStatus.FAILURE
            nation.generation_error = f"Task setup failed: {setup_e}"[:1024]
            nation.save(update_fields=['generation_status', 'generation_error'])
        except Exception as fail_save_e:
             print(f"Error [Task {task_id}]: Could not even save failure status: {fail_save_e}")
        return f"Task {task_id} failed during setup: {setup_e}"


    # --- Task Execution ---
    generated_code = "# Generation did not complete successfully."
    error_message = None
    prompt_used = ""
    nation_context_str = "Nation RAG system inactive, failed, or disabled."
    guideline_context_str = "Guideline RAG system inactive, failed, or disabled."
    rag_context_for_prompt = "" # Initialize context for prompt

    try:
        # --- RAG: Retrieve Context from Vertex AI ---
        query_embedding = None
        # Check if Vertex AI clients are available (initialized in vertex_client.py)
        can_query_nation = bool(vertex_ai_endpoint_nation and VERTEX_DEPLOYED_INDEX_ID)
        can_query_guideline = bool(guideline_vertex_ai_endpoint and GUIDELINE_VERTEX_DEPLOYED_INDEX_ID)

        # 1. Generate Embedding for the Query
        if can_query_nation or can_query_guideline:
            try:
                print(f"[Task {task_id}] Generating query embedding...")
                query_text = f"Nation Name: {nation.name}\nDescription: {nation.description}" # More structured query
                # Ensure Gemini API is configured before calling embed_content
                if not getattr(genai, '_client', None) and not TASK_GEMINI_API_KEY:
                     raise ValueError("Gemini API Key not configured for embedding.")

                query_embedding_response = genai.embed_content(
                    model="models/embedding-001", # Or text-embedding-004 etc. Ensure match with index!
                    content=query_text,
                    task_type="RETRIEVAL_QUERY"
                )
                query_embedding = query_embedding_response['embedding']
                print(f"[Task {task_id}] Query embedding generated.")
            except Exception as embed_e:
                print(f"[Task {task_id}] Error generating query embedding: {embed_e}")
                error_message = f"Failed to generate query embedding: {embed_e}"
                # Disable RAG if embedding fails
                can_query_nation = False
                can_query_guideline = False
                query_embedding = None

        # 2. Query Nation Index (if possible)
        if can_query_nation and query_embedding:
            try:
                print(f"[Task {task_id}] Querying NATION Index ({VERTEX_DEPLOYED_INDEX_ID})...")
                NUM_NEIGHBORS = 5
                nation_response = vertex_ai_endpoint_nation.find_neighbors(
                    queries=[query_embedding],
                    deployed_index_id=VERTEX_DEPLOYED_INDEX_ID,
                    num_neighbors=NUM_NEIGHBORS
                )
                retrieved_docs_info_nation = []
                if nation_response and nation_response[0]:
                    print(f"[Task {task_id}] Received {len(nation_response[0])} neighbors from NATION Index.")
                    # TODO: Fetch actual content based on neighbor.id if index stores it.
                    for neighbor in nation_response[0]:
                        retrieved_docs_info_nation.append(f"- ID: {neighbor.id} (Dist: {neighbor.distance:.4f})") # Placeholder
                    nation_context_str = "\n".join(retrieved_docs_info_nation)
                else:
                     nation_context_str = "No relevant neighbors found in NATION Index."
            except Exception as nation_rag_e:
                print(f"[Task {task_id}] Error during NATION Index RAG retrieval: {nation_rag_e}")
                nation_context_str = f"Error during NATION Index retrieval: {nation_rag_e}"
                if not error_message: error_message = "Failed Nation Index retrieval." # Keep it brief
        elif not can_query_nation:
             print(f"[Task {task_id}] Skipping NATION index query (disabled or embedding failed).")
             # nation_context_str already has default error message

        # 3. Query Guideline Index (if possible)
        if can_query_guideline and query_embedding:
            try:
                print(f"[Task {task_id}] Querying GUIDELINE Index ({GUIDELINE_VERTEX_DEPLOYED_INDEX_ID})...")
                NUM_NEIGHBORS_GUIDELINE = 3
                guideline_response = guideline_vertex_ai_endpoint.find_neighbors(
                    queries=[query_embedding],
                    deployed_index_id=GUIDELINE_VERTEX_DEPLOYED_INDEX_ID,
                    num_neighbors=NUM_NEIGHBORS_GUIDELINE
                )
                retrieved_docs_info_guideline = []
                if guideline_response and guideline_response[0]:
                    print(f"[Task {task_id}] Received {len(guideline_response[0])} neighbors from GUIDELINE Index.")
                    # TODO: Fetch actual content based on neighbor.id if index stores it.
                    for neighbor in guideline_response[0]:
                        retrieved_docs_info_guideline.append(f"- ID: {neighbor.id} (Dist: {neighbor.distance:.4f})") # Placeholder
                    guideline_context_str = "\n".join(retrieved_docs_info_guideline)
                else:
                     guideline_context_str = "No relevant neighbors found in GUIDELINE Index."
            except Exception as guideline_rag_e:
                print(f"[Task {task_id}] Error during GUIDELINE Index RAG retrieval: {guideline_rag_e}")
                guideline_context_str = f"Error during GUIDELINE Index retrieval: {guideline_rag_e}"
                if not error_message: error_message = "Failed Guideline Index retrieval." # Keep it brief
        elif not can_query_guideline:
             print(f"[Task {task_id}] Skipping GUIDELINE index query (disabled or embedding failed).")
             # guideline_context_str already has default error message

        # 4. Combine Context for Prompt
        rag_context_for_prompt = f"Retrieved Context:\n\n--- Nation Data Context ---\n{nation_context_str}\n\n--- Modding Guideline Context ---\n{guideline_context_str}\n\n"

        # --- Generation: Call Gemini ---
        # Ensure Gemini API is configured before calling generate_content
        if not getattr(genai, '_client', None) and not TASK_GEMINI_API_KEY:
             raise ValueError("Gemini API Key not configured for generation.")

        # Choose the Gemini model
        # Consider making model name configurable via settings/env vars
        generation_model = genai.GenerativeModel('gemini-1.5-flash') # Using 1.5 Flash

        # Construct the prompt
        prompt = f"""You are an expert Dominions 6 modder creating a new nation mod file (.dm format).
Use the following retrieved game data context (Nation Data) and modding guideline context (Guideline Data) to ensure accuracy and correct syntax. If context is missing or doesn't apply, use reasonable defaults based on the Nation Name and Description provided below the context. Prioritize guideline context for syntax questions.

{rag_context_for_prompt}
Task: Generate ONLY the core nation definition block AND definitions for 8 basic starting units (2 Commander, 1 mage, 1 priest, 4 troops). Start the nation block exactly with '#newnation' and end it exactly with '#end'. Start each unit block exactly with '#newmonster' and end it exactly with '#end'. Do not include explanations or markdown formatting outside the required commands.

Nation Name: {nation.name}
Nation Description: {nation.description}

Output only the raw .dm commands.
"""
        prompt_used = prompt # Store for potential debugging

        print(f"[Task {task_id}] Sending prompt to Gemini model {generation_model.model_name}...")
        # Call the Gemini API
        generation_response = generation_model.generate_content(prompt)
        print(f"[Task {task_id}] Gemini API call completed.")

        # Process the response
        try:
            # Attempt to get the text part of the response
            generated_code = generation_response.text
            if not generated_code.strip():
                generated_code = "# Error: AI response was empty."
                if not error_message: error_message = "AI response was empty."
            print(f"[Task {task_id}] Successfully extracted text from Gemini response.")
        except ValueError:
             # Handle cases where the response was blocked (e.g., safety filters)
             generated_code = f"# Error: AI response blocked or invalid."
             try:
                 feedback = f"Prompt Feedback: {generation_response.prompt_feedback}"
                 print(f"[Task {task_id}] {feedback}")
                 if not error_message: error_message = f"AI response blocked. {feedback}"
             except Exception:
                 print(f"[Task {task_id}] AI response blocked, feedback unavailable.")
                 if not error_message: error_message = "AI response blocked, feedback unavailable."
        except Exception as resp_err:
             # Catch other potential errors processing the response object
             print(f"[Task {task_id}] Error processing Gemini response: {resp_err}")
             generated_code = f"# Error: Could not parse AI response."
             if not error_message: error_message = f"Error processing AI response: {resp_err}"

    # --- General Task Error Handling ---
    except ValueError as ve:
        # Catch configuration errors (like missing API key detected within the try block)
        print(f"[Task {task_id}] Configuration Error during task execution: {ve}")
        error_message = str(ve)
        generated_code = f"# Error: Configuration problem ({ve})."
    except NameError as ne:
         # Catch missing libraries if imports failed silently earlier
         print(f"[Task {task_id}] NameError: {ne}. Required library missing?")
         error_message = f"Required library not available ({ne})."
         generated_code = "# Error: Required library missing."
    except Exception as e:
        # Catch-all for any other unexpected errors during RAG or Generation
        print(f"[Task {task_id}] Unexpected error during task execution: {e}")
        error_message = f"An unexpected error occurred: {e}"
        generated_code = f"# Error: Generation failed unexpectedly ({e})."
        # Include traceback for debugging if possible/desired
        # import traceback
        # error_message += f"\n{traceback.format_exc()}"


    # --- Final Status Update ---
    # Update the nation object in the database with the results or errors.
    final_status = NationGenerationStatus.COMPLETED
    if error_message:
        final_status = NationGenerationStatus.FAILURE
        nation.generation_error = str(error_message)[:1024] # Truncate if needed
        print(f"[Task {task_id}] Task failed: {error_message}")
    else:
        nation.generated_dm_code = generated_code
        nation.generation_error = None
        print(f"[Task {task_id}] Task completed successfully.")

    nation.generation_status = final_status
    nation.last_prompt_used = prompt_used[:2048] # Store prompt used, truncate if needed
    try:
        nation.save(update_fields=['generation_status', 'generated_dm_code', 'generation_error', 'last_prompt_used'])
        print(f"[Task {task_id}] Final status ({final_status}) saved to database.")
    except Exception as final_save_e:
         print(f"Error [Task {task_id}]: Failed to save final task status to DB: {final_save_e}")
         # This is bad, the task completed/failed but DB doesn't reflect it fully.

    return f"Nation {nation_id} generation finished with status: {final_status}"

