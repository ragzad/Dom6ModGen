# nations/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Nation
from .forms import NationForm
import google.generativeai as genai
from google.cloud import aiplatform
from decouple import config
import os

# --- Configuration Section ---

# Configure Gemini API Key (from .env or Heroku Config Vars)
try:
    GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        print("Gemini API Key configured.")
    else:
        print("WARN: GEMINI_API_KEY not found in environment. AI generation will fail.")
except NameError:
    print("WARN: google-generativeai library not found. Install it (pip install google-generativeai) to use AI features.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

# --- Vertex AI Configuration (Read from Environment Variables) ---
GCP_PROJECT_ID = config('GCP_PROJECT_ID', default=None)
GCP_REGION = config('GCP_REGION', default='europe-west3') # specified region
VERTEX_INDEX_ENDPOINT_ID = config('VERTEX_INDEX_ENDPOINT_ID', default='8216764743579336704') # e.g., '1234567890123456789'
VERTEX_DEPLOYED_INDEX_ID = config('VERTEX_DEPLOYED_INDEX_ID', default='dom6modgen-v1') # e.g., 'deployed_dom6_index_v1'

# Authentication for Vertex AI Client (uses Application Default Credentials - ADC)
vertex_ai_endpoint = None
try:
    if not all([GCP_PROJECT_ID, GCP_REGION, VERTEX_INDEX_ENDPOINT_ID, VERTEX_DEPLOYED_INDEX_ID]) or \
       'YOUR_' in VERTEX_INDEX_ENDPOINT_ID or 'YOUR_' in VERTEX_DEPLOYED_INDEX_ID:
        print("WARN: Missing required Vertex AI config (Project ID, Region, Endpoint ID, Deployed Index ID). Check environment variables. RAG will be disabled.")
    else:
        print("Initializing Vertex AI Platform client...")
        aiplatform.init(project=GCP_PROJECT_ID, location=GCP_REGION)
        # Get the endpoint resource reference using the numeric ID
        vertex_ai_endpoint = aiplatform.MatchingEngineIndexEndpoint(
            endpoint_name=VERTEX_INDEX_ENDPOINT_ID # Use the numeric ID here
        )
        print(f"Vertex AI Matching Engine endpoint reference created for: {VERTEX_INDEX_ENDPOINT_ID}")

except ImportError:
     print("ERROR: google-cloud-aiplatform library not found. Run pip install google-cloud-aiplatform")
     vertex_ai_endpoint = None
except Exception as e:
    print(f"ERROR initializing Vertex AI client or endpoint: {e}")
    vertex_ai_endpoint = None
# --- End Configuration ---


# --- Standard CRUD Views ---
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


# --- Vertex AI RAG-Integrated AI Generation View ---
def nation_generate_dm(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    generated_code = "# Generation failed or prerequisites missing."
    error_message = None
    prompt_used = ""
    retrieved_context = "RAG system inactive or failed." # Default display value

    try:
        # --- RAG Retrieval Step using Vertex AI ---
        rag_context_for_prompt = ""
        # Check if Vertex AI endpoint was initialized successfully
        if vertex_ai_endpoint:
            try:
                print("Generating query embedding using Gemini...")
                query_text = f"{nation.name} {nation.description}"
                # Use Gemini API to get embedding for the query
                # Ensure GEMINI_API_KEY is configured
                query_embedding_response = genai.embed_content(
                    model="models/embedding-001", # Or the specific model used for indexing e.g., text-embedding-004
                    content=query_text,
                    task_type="RETRIEVAL_QUERY" # Use appropriate task type
                )
                query_embedding = query_embedding_response['embedding']

                print(f"Querying Vertex AI Matching Engine Endpoint: {VERTEX_INDEX_ENDPOINT_ID}...")
                # Query the deployed index endpoint using find_neighbors
                NUM_NEIGHBORS = 5 # How many results to retrieve
                response = vertex_ai_endpoint.find_neighbors(
                    queries=[query_embedding],
                    deployed_index_id=VERTEX_DEPLOYED_INDEX_ID, # Use the ID you noted down
                    num_neighbors=NUM_NEIGHBORS
                )

                # Process the results
                retrieved_docs_info = [] # Store info about retrieved docs
                if response and response[0]: # Response is a list containing one list of neighbors for our query
                    print(f"Received {len(response[0])} neighbors from Vertex AI.")
                    for neighbor in response[0]:
                        retrieved_docs_info.append(f"ID: {neighbor.id} (Distance: {neighbor.distance:.4f})")

                    retrieved_context = "\n".join(retrieved_docs_info)
                    # Placeholder context for the prompt (replace once text lookup is implemented)
                    rag_context_for_prompt = f"Retrieved Relevant Game Data IDs (Context lookup pending):\n```\n{retrieved_context}\n```\n\n"
                else:
                     retrieved_context = "No relevant neighbors found in Vertex AI."
                     print("WARN: No relevant neighbors found in Vertex AI query.")

            except Exception as rag_e:
                print(f"Error during Vertex AI RAG retrieval: {rag_e}")
                retrieved_context = f"Error during Vertex AI RAG retrieval: {rag_e}"
                error_message = "Failed to retrieve context from Vertex AI."
        else:
             retrieved_context = "Vertex AI RAG components not initialized correctly."
             error_message = retrieved_context # Pass initialization error
             print("WARN: Skipping RAG query due to Vertex AI initialization failure.")
        # --- End RAG Retrieval ---

        # Check for Gemini API Key (ensure it was configured)
        loaded_api_key = config('GEMINI_API_KEY', default=None)
        if not loaded_api_key:
            raise ValueError("Gemini API Key not found in environment variables.")

        # Select the Gemini model for generation
        generation_model = genai.GenerativeModel('gemini-1.5-flash')

        # Construct the final prompt, injecting the retrieved RAG context (or IDs)
        prompt = f"""You are an expert Dominions 6 modder creating a new nation mod file (.dm format).
Use the following retrieved game data context (IDs of relevant items/units/spells/etc.) to ensure accuracy where possible. If context is missing or doesn't apply, use reasonable defaults based on the Nation Name and Description provided below the context.

{rag_context_for_prompt}
Task: Generate ONLY the core nation definition block AND definitions for 3 basic starting units (1 Commander, 1 Infantry, 1 Ranged/Other). Start the nation block exactly with '#newnation' and end it exactly with '#end'. Start each unit block exactly with '#newmonster' and end it exactly with '#end'. Do not include explanations or markdown formatting outside the required commands.

Nation Name: {nation.name}
Nation Description: {nation.description}

Generate the following commands, using the context above AND the nation details:
- #name "{nation.name}"
- #epithet "..."
- #era <number> (Assume 2/MA)
- #descr "{nation.description}"
- #summary "..."
- #brief "..."
- #flag "PLACEHOLDER/{nation.name}_flag.tga"
- #color <r> <g> <b>
- #secondarycolor <r> <g> <b>
- #idealcold <number>
- #startsite "..."
- #startcom "{nation.name} Commander"
- #startunittype1 "{nation.name}"
- #startunittype2 "{nation.name}"
- #dominionstr <number>
- #castleprod <number>
Also generate the '#newmonster' blocks for the 3 starting units mentioned above, including basic stats (#hp, #str, #att, #def, #prec, #mor, #mr, #move, #ap), costs (#recruitcost, #resourcecost, #upkeep), basic #weapon/#armor suggestions (using names), and appropriate tags (#commander, #infantry, #startunit etc.).

Output only the raw .dm commands.
"""
        prompt_used = prompt

        # Make the Generation API call
        print("Attempting to call Gemini API for generation...")
        generation_response = generation_model.generate_content(prompt)
        print("Gemini API generation call completed.")

        # Process the generation response
        try:
            generated_code = generation_response.text
            if not generated_code.strip(): generated_code = "# Error: AI response was empty."
        except ValueError:
             generated_code = f"# Error: AI response blocked or invalid."
             error_message = f"AI Response Feedback: {generation_response.prompt_feedback}"
        except Exception as resp_err:
             generated_code = f"# Error: Could not parse AI response."
             error_message = f"Error processing AI response: {resp_err}"

    # --- Exception Handling ---
    except ValueError as ve: # Catch missing key/config error
        print(f"Configuration Error: {ve}")
        error_message = str(ve)
        generated_code = f"Error: Configuration problem ({ve}). Check environment variables."
    except NameError as ne: # Catch if a required library wasn't imported
         print(f"NameError: {ne}. Required library missing or import failed?")
         error_message = f"Required library not available ({ne}). Please run pip install."
         generated_code = "Error: Required library missing."
    except Exception as e: # Catch other potential errors (API calls, network, Vertex AI query errors etc.)
        print(f"Error during generation view: {e}")
        error_message = f"An error occurred: {e}"
        generated_code = f"Error: Could not generate code ({e})."

    context = {
        'nation': nation,
        'generated_code': generated_code,
        'error_message': error_message,
        'prompt_used': prompt_used,
        'retrieved_context': retrieved_context, # Pass retrieved context/IDs for display
    }
    return render(request, 'nations/nation_generate_dm.html', context)

