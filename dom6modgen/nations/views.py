# nations/views.py

# --- Keep other imports ---
from django.shortcuts import render, get_object_or_404, redirect
from .models import Nation
from .forms import NationForm
import google.generativeai as genai
from google.cloud import aiplatform
# --- Add these imports for Method B ---
import json
from google.oauth2 import service_account
# --- End Added imports ---
from decouple import config
import os
import numpy as np

# --- Keep Gemini API Key Configuration ---
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
GCP_REGION = config('GCP_REGION', default='europe-west3') 
VERTEX_ENDPOINT_ID = config('VERTEX_ENDPOINT_ID', default=None) 
VERTEX_INDEX_ID = config('VERTEX_INDEX_ID', default=None) 
vertex_endpoint = None # Initialize endpoint variable

# Inside the Vertex AI Configuration section of views.py

try:
    if GCP_PROJECT_ID:
        # --- Modification Start ---
        # Construct the regional API endpoint hostname
        regional_api_endpoint = f"{GCP_REGION}-aiplatform.googleapis.com"
        print(f"DEBUG: Explicitly setting API endpoint to: {regional_api_endpoint}")

        aiplatform.init(
            project=GCP_PROJECT_ID,
            location=GCP_REGION,
            credentials=credentials, # Pass the loaded credentials object (or None)
            api_endpoint=regional_api_endpoint # Explicitly set the regional endpoint
        )
        # --- Modification End ---

        print(f"Vertex AI initialized for project {GCP_PROJECT_ID} in {GCP_REGION}.")

        # ... (rest of the endpoint loading logic remains the same) ...

    else:
         print("WARN: GCP_PROJECT_ID not found in environment. Vertex AI initialization skipped.")
         # ...
except Exception as e:
     # Catch errors during aiplatform.init() itself
     print(f"ERROR initializing Vertex AI client or endpoint: {e}")
     # ...

# --- Start Integration of Method B ---
GCP_SERVICE_ACCOUNT_JSON_STR = config('GCP_SERVICE_ACCOUNT_KEY_JSON', default=None)
credentials = None # Initialize credentials variable
if GCP_SERVICE_ACCOUNT_JSON_STR:
    try:
        # Attempt to parse the JSON string from the environment variable
        key_info = json.loads(GCP_SERVICE_ACCOUNT_JSON_STR)
        # Create credentials object from the parsed info
        credentials = service_account.Credentials.from_service_account_info(key_info)
        print("Loaded Service Account credentials from environment variable.")
    except json.JSONDecodeError:
        print("ERROR: GCP_SERVICE_ACCOUNT_KEY_JSON environment variable contains invalid JSON.")
    except Exception as cred_err:
        print(f"ERROR loading credentials from GCP_SERVICE_ACCOUNT_KEY_JSON: {cred_err}")
# --- End Integration of Method B ---

try:
    # Check if Project ID is available (needed for initialization)
    if GCP_PROJECT_ID:
        # Initialize Vertex AI client, explicitly passing credentials if loaded
        aiplatform.init(
            project=GCP_PROJECT_ID,
            location=GCP_REGION,
            credentials=credentials # Pass the loaded credentials object (or None)
        )
        print(f"Vertex AI initialized for project {GCP_PROJECT_ID} in {GCP_REGION}.")

        # Now, proceed ONLY if Endpoint ID is also available
        if VERTEX_ENDPOINT_ID:
            try:
                # Attempt to load the specific endpoint
                vertex_endpoint = aiplatform.MatchingEngineIndexEndpoint(
                    index_endpoint_name=VERTEX_ENDPOINT_ID # Use the full ID or resource name from env var
                )
                print(f"Successfully loaded Vertex AI Matching Engine endpoint: {VERTEX_ENDPOINT_ID}")
            except Exception as endpoint_err:
                 print(f"ERROR loading Vertex AI endpoint '{VERTEX_ENDPOINT_ID}': {endpoint_err}")
                 vertex_endpoint = None # Ensure it's None if endpoint load fails
        else:
            print("WARN: VERTEX_ENDPOINT_ID not found in environment. RAG will be skipped.")
            vertex_endpoint = None # Explicitly set to None

    else:
         print("WARN: GCP_PROJECT_ID not found in environment. Vertex AI initialization skipped.")
         vertex_endpoint = None # Ensure endpoint is None if project ID is missing

except Exception as e:
     # Catch errors during aiplatform.init() itself
     print(f"ERROR initializing Vertex AI client or endpoint: {e}")
     vertex_endpoint = None # Ensure endpoint is None if init fails

# --- Keep CRUD Views (nation_list, nation_detail, etc.) ---
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


# --- Updated AI Generation View (with RAG using Vertex AI) ---
def nation_generate_dm(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    generated_code = None # Initialize
    error_message = None
    prompt_used = ""
    retrieved_context = "RAG context not generated (feature disabled or error)." # Default message

    try:
        # Check Gemini API Key (still needed for generation)
        if not GEMINI_API_KEY: # Check the globally configured key status
            raise ValueError("Gemini API Key not configured or found.")

        # --- RAG - Query Vertex AI Matching Engine ---
        if vertex_endpoint and VERTEX_INDEX_ID: # Ensure endpoint AND index ID are loaded
            try:
    # ... (prepare query_embeddings) ...

                print(f"Querying Vertex AI Index: {VERTEX_INDEX_ID} on Endpoint: {VERTEX_ENDPOINT_ID}") # Use full ID here too for clarity

    # --- Modification Start ---
    # Pass the full VERTEX_INDEX_ID directly
                match_response = vertex_endpoint.match(
                    deployed_index_id=VERTEX_INDEX_ID, # <-- Use the full ID variable
                    queries=[query_embeddings],
                    num_neighbors=3
    )
                print(f"Vertex AI Match Response received (neighbors found: {len(match_response[0])})")

                # Process the response to build context string
                neighbor_texts = []
                if match_response and match_response[0]:
                    for neighbor in match_response[0]:
                        # Assuming neighbor.id holds the document text or an ID to fetch it
                        neighbor_texts.append(f"[Neighbor ID: {neighbor.id}, Distance: {neighbor.distance:.4f}]")
                    retrieved_context = "Retrieved Context based on similarity search:\n" + "\n---\n".join(neighbor_texts)
                else:
                    retrieved_context = "No relevant context found via RAG."

            except Exception as rag_err:
                 print(f"ERROR during RAG query: {rag_err}")
                 error_message = f"RAG query failed: {rag_err}"
                 retrieved_context = "Error during RAG context retrieval."
        else:
             retrieved_context = "RAG skipped: Vertex AI endpoint/index not available or configured."

        # --- Generation using Gemini (potentially with RAG context) ---
        model = genai.GenerativeModel('gemini-1.5-flash') # Or your preferred model

        # Construct the prompt, including the retrieved RAG context
        prompt = f"""You are an expert Dominions 6 modder creating a new nation mod file (.dm format).
Your task is to generate ONLY the core nation definition block AND definitions for 3 basic starting units (1 Commander, 1 Infantry, 1 Ranged/Other). Start the nation block exactly with '#newnation' and end it exactly with '#end'. Start each unit block exactly with '#newmonster' and end it exactly with '#end'. Do not include explanations or markdown formatting outside the required commands. Use reasonable defaults based on the Nation Name and Description.

Incorporate the following related context if relevant, otherwise ignore it:
--- CONTEXT START ---
{retrieved_context}
--- CONTEXT END ---

Nation Name: {nation.name}
Nation Description: {nation.description}

Generate the following commands:
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
- #startunittype1 "{nation.name} Infantry"
- #startunittype2 "{nation.name} Skirmisher"
- #dominionstr <number>
- #castleprod <number>
Also generate the '#newmonster' blocks for the 3 starting units mentioned above, including basic stats (#hp, #str, #att, #def, #prec, #mor, #mr, #move, #ap), costs (#recruitcost, #resourcecost, #upkeep), basic #weapon/#armor suggestions (using names), and appropriate tags (#commander, #infantry, #startunit etc.).

Output only the raw .dm commands.
"""
        prompt_used = prompt # Store for display/debugging

        print("Attempting to call Gemini API for generation...")
        generation_response = model.generate_content(prompt)
        print("Gemini API generation call completed.")

        # Process the generation response
        try:
            generated_code = generation_response.text
            if not generated_code.strip(): generated_code = "# Error: AI response was empty."
        except ValueError:
             generated_code = f"# Error: AI response blocked or invalid."
             try: error_message = f"AI Response Feedback: {generation_response.prompt_feedback}"
             except Exception: error_message = "AI response blocked or invalid, feedback unavailable."
        except Exception as resp_err:
             generated_code = f"# Error: Could not parse AI response."
             error_message = f"Error processing AI response: {resp_err}"

    # --- Exception Handling ---
    except ValueError as ve: # Catch missing key/config error
        print(f"Configuration Error: {ve}")
        error_message = str(ve)
    except NameError as ne: # Catch if a required library wasn't imported
         print(f"NameError: {ne}. Required library missing or import failed?")
         error_message = f"Required library not available ({ne}). Please run pip install."
    except Exception as e: # Catch other potential errors
        print(f"Error during generation view: {e}")
        error_message = f"An error occurred: {e}"

    context = {
        'nation': nation,
        'generated_code': generated_code or "# Generation failed.", # Ensure generated_code isn't None
        'error_message': error_message,
        'prompt_used': prompt_used,
        'retrieved_context': retrieved_context, # Pass RAG context/IDs for display
    }
    return render(request, 'nations/nation_generate_dm.html', context)