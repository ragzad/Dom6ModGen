# nations/views.py
# Where the nation-related views live.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Nation
from .forms import NationForm

# Pull in libraries for AI stuff (Gemini and Vertex)
import google.generativeai as genai
from google.cloud import aiplatform

# Stuff needed to handle Google Cloud credentials from JSON.
import json
from google.oauth2 import service_account
from decouple import config
import os
import numpy as np # Often needed by client libraries

# --- Settings & API Keys ---

# Get the Gemini API Key from environment variables.
try:
    GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        print("Gemini API Key configured.")
    else:
        print("WARN: GEMINI_API_KEY not found in environment. AI generation will fail.")
except NameError:
    # Fails gracefully if the Gemini library isn't installed.
    print("WARN: google-generativeai library not found. Install it (pip install google-generativeai) to use AI features.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

# --- Vertex AI Index Settings (from environment variables) ---
GCP_PROJECT_ID = config('GCP_PROJECT_ID', default=None)
GCP_REGION = config('GCP_REGION', default='europe-west3')

# ---- First Index (Nation Data) ----
VERTEX_INDEX_ENDPOINT_ID = config('VERTEX_INDEX_ENDPOINT_ID', default='YOUR_ORIGINAL_ENDPOINT_ID_HERE')
VERTEX_DEPLOYED_INDEX_ID = config('VERTEX_DEPLOYED_INDEX_ID', default='YOUR_ORIGINAL_DEPLOYED_ID_HERE')

# ---- Second Index (Modding Guidelines) ----
GUIDELINE_VERTEX_INDEX_ENDPOINT_ID = config('GUIDELINE_VERTEX_INDEX_ENDPOINT_ID', default='3238035355521253376')
GUIDELINE_VERTEX_DEPLOYED_INDEX_ID = config('GUIDELINE_VERTEX_DEPLOYED_INDEX_ID', default='dom6modgen_guideline')

# --- Optional: Load Google Cloud Service Account Key ---
# Tries to load credentials from a specific environment variable if it exists.
GCP_SERVICE_ACCOUNT_JSON_STR = config('GCP_SERVICE_ACCOUNT_KEY_JSON', default=None)
credentials = None # Initialize credentials variable
if GCP_SERVICE_ACCOUNT_JSON_STR:
    try:
        # Parse the JSON key.
        key_info = json.loads(GCP_SERVICE_ACCOUNT_JSON_STR)
        # Make credentials object.
        credentials = service_account.Credentials.from_service_account_info(key_info)
        print("Loaded Service Account credentials from GCP_SERVICE_ACCOUNT_KEY_JSON.")
    except json.JSONDecodeError:
        print("ERROR: GCP_SERVICE_ACCOUNT_KEY_JSON environment variable contains invalid JSON.")
    except Exception as cred_err:
        print(f"ERROR loading credentials from GCP_SERVICE_ACCOUNT_KEY_JSON: {cred_err}")
# If not found, it'll try default Google credentials later when aiplatform.init is called.

# Setup the main Vertex AI connection (once per app load).
try:
    if not GCP_PROJECT_ID:
         print("WARN: GCP_PROJECT_ID not configured. Vertex AI initialization skipped.")
    else:
        print("Initializing Vertex AI Platform client library...")
        aiplatform.init(
            project=GCP_PROJECT_ID,
            location=GCP_REGION,
            credentials=credentials # Pass the loaded credentials object (None if not loaded)
        )
        print(f"Vertex AI library initialized for project {GCP_PROJECT_ID} in {GCP_REGION}.")
except ImportError:
    print("ERROR: google-cloud-aiplatform library not found. Run pip install google-cloud-aiplatform")
except Exception as init_err:
    print(f"ERROR initializing Vertex AI library: {init_err}")

# Get ready to talk to our specific search indices.
vertex_ai_endpoint_nation = None
guideline_vertex_ai_endpoint = None

# ---- Connect to the Nation Data Index Endpoint ----
try:
    # Make sure we have the IDs needed for the nation index.
    if not all([GCP_PROJECT_ID, GCP_REGION, VERTEX_INDEX_ENDPOINT_ID, VERTEX_DEPLOYED_INDEX_ID]) or \
       'YOUR_' in VERTEX_INDEX_ENDPOINT_ID or 'YOUR_' in VERTEX_DEPLOYED_INDEX_ID:
        print("WARN: Missing config for NATION index. Nation RAG won't work.")
    else:
        print(f"Creating NATION index endpoint reference: {VERTEX_INDEX_ENDPOINT_ID}")
        # Create an object to represent the nation index endpoint.
        vertex_ai_endpoint_nation = aiplatform.MatchingEngineIndexEndpoint(
            index_endpoint_name=VERTEX_INDEX_ENDPOINT_ID
        )
        print(f"Vertex AI NATION Matching Engine endpoint reference created: {VERTEX_INDEX_ENDPOINT_ID}")
except NameError: # Handles case where Vertex library is missing.
     print("ERROR: Cannot create NATION endpoint reference - aiplatform library likely missing.")
except Exception as e:
    # Catch any other setup problems for the nation endpoint.
    print(f"ERROR initializing Vertex AI NATION endpoint ({VERTEX_INDEX_ENDPOINT_ID}): {e}")
    vertex_ai_endpoint_nation = None

# ---- Connect to the Modding Guideline Index Endpoint ----
try:
    # Make sure we have the IDs needed for the guideline index.
    if not all([GCP_PROJECT_ID, GCP_REGION, GUIDELINE_VERTEX_INDEX_ENDPOINT_ID, GUIDELINE_VERTEX_DEPLOYED_INDEX_ID]) or \
       'YOUR_' in GUIDELINE_VERTEX_INDEX_ENDPOINT_ID or 'YOUR_' in GUIDELINE_VERTEX_DEPLOYED_INDEX_ID:
        print("WARN: Missing config for GUIDELINE index. Guideline RAG won't work.")
    else:
        print(f"Creating GUIDELINE index endpoint reference: {GUIDELINE_VERTEX_INDEX_ENDPOINT_ID}")
        # Create an object to represent the guideline index endpoint.
        guideline_vertex_ai_endpoint = aiplatform.MatchingEngineIndexEndpoint(
            index_endpoint_name=GUIDELINE_VERTEX_INDEX_ENDPOINT_ID
        )
        print(f"Vertex AI GUIDELINE Matching Engine endpoint reference created: {GUIDELINE_VERTEX_INDEX_ENDPOINT_ID}")
except NameError: # Handles case where Vertex library is missing.
     print("ERROR: Cannot create GUIDELINE endpoint reference - aiplatform library likely missing.")
except Exception as e:
    # Catch any other setup problems for the guideline endpoint.
    print(f"ERROR initializing Vertex AI GUIDELINE endpoint ({GUIDELINE_VERTEX_INDEX_ENDPOINT_ID}): {e}")
    guideline_vertex_ai_endpoint = None
# --- End Settings ---


# --- Standard Django Views (List, Detail, Create, Update, Delete) ---
# These handle the basic web pages for nations.
def nation_list(request):
    nations = Nation.objects.all().order_by('name')
    context = { 'nations': nations }
    return render(request, 'nations/nation_list.html', context)

def nation_detail(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    context = { 'nation': nation }
    return render(request, 'nations/nation_detail.html', context)

def nation_create(request):
    if request.method == 'POST':
        form = NationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nations:nation_list')
    else:
        form = NationForm()
    context = { 'form': form }
    return render(request, 'nations/nation_form.html', context)

def nation_update(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    if request.method == 'POST':
        form = NationForm(request.POST, instance=nation)
        if form.is_valid():
            form.save()
            return redirect('nations:nation_detail', pk=nation.pk)
    else:
        form = NationForm(instance=nation)
    context = { 'form': form, 'nation': nation }
    return render(request, 'nations/nation_form.html', context)

def nation_delete(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    if request.method == 'POST':
        nation.delete()
        return redirect('nations:nation_list')
    context = { 'nation': nation }
    return render(request, 'nations/nation_confirm_delete.html', context)


# --- AI Generation View (Using RAG) ---
def nation_generate_dm(request, pk):
    """Generates Dominions 6 mod code using RAG with two indices + Gemini."""
    nation = get_object_or_404(Nation, pk=pk)
    # Set some defaults in case things go wrong.
    generated_code = "# Generation failed or prerequisites missing."
    error_message = None
    prompt_used = ""
    # Default text for nation context.
    nation_context_str = "Nation RAG system inactive or failed."
    # Default text for guideline context.
    guideline_context_str = "Guideline RAG system inactive or failed."
    combined_retrieved_context_display = f"Nation Context:\n{nation_context_str}\n\nGuideline Context:\n{guideline_context_str}"

    # Flags to check if we can actually query the indices.
    # Initialize based on whether the endpoint objects were created successfully at startup
    can_query_nation = bool(vertex_ai_endpoint_nation)
    can_query_guideline = bool(guideline_vertex_ai_endpoint)
    query_embedding = None # Ensure defined before try block

    try:
        # --- RAG Step: Get Context from Vertex AI ---
        # We'll build the context for the AI prompt here.
        rag_context_for_prompt = ""

        # Only try embedding if at least one index connection is ready.
        if can_query_nation or can_query_guideline:
            try:
                print("Generating query embedding using Gemini...")
                query_text = f"{nation.name} {nation.description}"
                # Turn the nation name/description into a vector using Gemini.
                # Make sure this embedding model matches the one used for indexing!
                query_embedding_response = genai.embed_content(
                    model="models/embedding-001", # Or text-embedding-004 etc.
                    content=query_text,
                    task_type="RETRIEVAL_QUERY"
                )
                query_embedding = query_embedding_response['embedding']
                print("Query embedding generated.")

            except Exception as embed_e:
                print(f"Error generating query embedding: {embed_e}")
                error_message = f"Failed to generate query embedding: {embed_e}"
                # Can't search without the embedding vector.
                # Mark indices as unavailable if embedding failed.
                can_query_nation = False
                can_query_guideline = False
                query_embedding = None # Ensure embedding is None if it failed

        # ---- Search the Nation Index ----
        # Check if we can query this index (and have an embedding).
        if can_query_nation and query_embedding:
            try:
                # Use the global vertex_ai_endpoint_nation directly
                print(f"Querying NATION Index Endpoint: {VERTEX_INDEX_ENDPOINT_ID} with Deployed Index ID: {VERTEX_DEPLOYED_INDEX_ID}...")
                NUM_NEIGHBORS = 5 # How many results to fetch.
                nation_response = vertex_ai_endpoint_nation.find_neighbors(
                    queries=[query_embedding],
                    deployed_index_id=VERTEX_DEPLOYED_INDEX_ID,
                    num_neighbors=NUM_NEIGHBORS
                )

                retrieved_docs_info_nation = []
                if nation_response and nation_response[0]:
                    print(f"Received {len(nation_response[0])} neighbors from NATION Index.")
                    # TODO: If index stores full text, fetch it here based on neighbor.id
                    for neighbor in nation_response[0]:
                        retrieved_docs_info_nation.append(f"Nation ID: {neighbor.id} (Distance: {neighbor.distance:.4f})")
                    nation_context_str = "\n".join(retrieved_docs_info_nation)
                else:
                     nation_context_str = "No relevant neighbors found in NATION Index."
                     print("WARN: No relevant neighbors found in NATION Index query.")

            except Exception as nation_rag_e:
                print(f"Error during NATION Index RAG retrieval: {nation_rag_e}")
                nation_context_str = f"Error during NATION Index retrieval: {nation_rag_e}"
                if not error_message: error_message = "Failed to retrieve context from Nation Index."
        # Explain why the query was skipped.
        elif not can_query_nation:
             nation_context_str = "NATION Index endpoint not initialized or embedding failed."
             print("WARN: Skipping NATION RAG query due to initialization or embedding failure.")


        # ---- Search the Guideline Index ----
        # Check if we can query this index (and have an embedding).
        if can_query_guideline and query_embedding:
            try:
                # Use the global guideline_vertex_ai_endpoint directly
                print(f"Querying GUIDELINE Index Endpoint: {GUIDELINE_VERTEX_INDEX_ENDPOINT_ID} with Deployed Index ID: {GUIDELINE_VERTEX_DEPLOYED_INDEX_ID}...")
                NUM_NEIGHBORS_GUIDELINE = 3 # How many results to fetch (can be different).
                guideline_response = guideline_vertex_ai_endpoint.find_neighbors(
                    queries=[query_embedding],
                    deployed_index_id=GUIDELINE_VERTEX_DEPLOYED_INDEX_ID,
                    num_neighbors=NUM_NEIGHBORS_GUIDELINE
                )

                retrieved_docs_info_guideline = []
                if guideline_response and guideline_response[0]:
                    print(f"Received {len(guideline_response[0])} neighbors from GUIDELINE Index.")
                    # TODO: If index stores full text, fetch it here based on neighbor.id
                    for neighbor in guideline_response[0]:
                        retrieved_docs_info_guideline.append(f"Guideline ID: {neighbor.id} (Distance: {neighbor.distance:.4f})")
                    guideline_context_str = "\n".join(retrieved_docs_info_guideline)
                else:
                     guideline_context_str = "No relevant neighbors found in GUIDELINE Index."
                     print("WARN: No relevant neighbors found in GUIDELINE Index query.")

            except Exception as guideline_rag_e:
                print(f"Error during GUIDELINE Index RAG retrieval: {guideline_rag_e}")
                guideline_context_str = f"Error during GUIDELINE Index retrieval: {guideline_rag_e}"
                if not error_message: error_message = "Failed to retrieve context from Guideline Index."
        # Explain why the query was skipped.
        elif not can_query_guideline:
             guideline_context_str = "GUIDELINE Index endpoint not initialized or embedding failed."
             print("WARN: Skipping GUIDELINE RAG query due to initialization or embedding failure.")

        # ---- Combine Retrieved Info ----
        # Prepare the context string for the main Gemini prompt.
        rag_context_for_prompt = f"Retrieved Relevant Context (Context lookup pending):\n\n--- Nation Data Context ---\n{nation_context_str}\n\n--- Modding Guideline Context ---\n{guideline_context_str}\n\n"

        # Prepare a combined string to show the user what context was found.
        combined_retrieved_context_display = f"Nation Context:\n```\n{nation_context_str}\n```\n\nGuideline Context:\n```\n{guideline_context_str}\n```"


        # --- Generation Step: Ask Gemini ---
        loaded_api_key = config('GEMINI_API_KEY', default=None)
        if not loaded_api_key:
            raise ValueError("Gemini API Key not found in environment variables.")

        # Choose the Gemini model to use (e.g., Flash or Pro).
        generation_model = genai.GenerativeModel('gemini-1.5-flash')

        # Build the big prompt with instructions and the retrieved context.
        prompt = f"""You are an expert Dominions 6 modder creating a new nation mod file (.dm format).
Use the following retrieved game data context (Nation Data) and modding guideline context (Guideline Data) to ensure accuracy and correct syntax. If context is missing or doesn't apply, use reasonable defaults based on the Nation Name and Description provided below the context. Prioritize guideline context for syntax questions.

{rag_context_for_prompt}
Task: Generate ONLY the core nation definition block AND definitions for 8 basic starting units (2 Commander, 1 mage, 1 priest, 4 troops). Start the nation block exactly with '#newnation' and end it exactly with '#end'. Start each unit block exactly with '#newmonster' and end it exactly with '#end'. Do not include explanations or markdown formatting outside the required commands.

Nation Name: {nation.name}
Nation Description: {nation.description}

Output only the raw .dm commands.
"""
        # Keep a copy of the prompt for debugging.
        prompt_used = prompt

        print("Attempting to call Gemini API for generation...")
        # Send the prompt to the Gemini API.
        generation_response = generation_model.generate_content(prompt)
        print("Gemini API generation call completed.")

        # Handle the response from Gemini.
        try:
            generated_code = generation_response.text
            if not generated_code.strip(): generated_code = "# Error: AI response was empty."
        except ValueError:
             # Check if the response was blocked (safety filters).
             generated_code = f"# Error: AI response blocked or invalid."
             try: error_message = f"AI Response Feedback: {generation_response.prompt_feedback}"
             except Exception: error_message = "AI response blocked or invalid, feedback unavailable."
        except Exception as resp_err:
             # Catch other problems reading the response.
             generated_code = f"# Error: Could not parse AI response."
             error_message = f"Error processing AI response: {resp_err}"

    # --- General Error Handling for the View ---
    except ValueError as ve:
        # Catch config issues (like missing API keys).
        print(f"Configuration Error: {ve}")
        error_message = str(ve)
        generated_code = f"Error: Configuration problem ({ve}). Check environment variables."
    except NameError as ne:
         # Catch missing Python libraries.
         print(f"NameError: {ne}. Required library missing or import failed?")
         error_message = f"Required library not available ({ne}). Please run pip install."
         generated_code = "Error: Required library missing."
    except Exception as e:
        # Catch any other unexpected errors.
        print(f"Error during generation view: {e}")
        error_message = f"An error occurred: {e}"
        generated_code = f"Error: Could not generate code ({e})."

    # Gather everything to send to the results page.
    context = {
        'nation': nation,
        'generated_code': generated_code,
        'error_message': error_message,
        'prompt_used': prompt_used,
        # Send the retrieved context (or errors) to the template.
        'retrieved_context': combined_retrieved_context_display,
    }
    # Show the results page.
    return render(request, 'nations/nation_generate_dm.html', context)