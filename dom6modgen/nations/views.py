# nations/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Nation
from .forms import NationForm
# Imports needed for AI and RAG
import google.generativeai as genai
from decouple import config
import os
# Make sure these are installed: pip install chromadb sentence-transformers
import chromadb
from sentence_transformers import SentenceTransformer

# --- Configuration Section ---
DB_PATH = "C:/Users/Ethan/chroma_db_dom6" # IMPORTANT: Verify this is the correct path to your DB folder!
COLLECTION_NAME = "dominions_data"
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2' # Must match the model used to create the DB

# Configure Gemini API Key
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

# Configure RAG Components (Embedding Model and ChromaDB Client)
embedding_model_rag = None
rag_collection = None
try:
    print(f"Loading embedding model for RAG: {EMBEDDING_MODEL_NAME}...")
    # Ensure sentence-transformers is installed: pip install sentence-transformers
    embedding_model_rag = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("RAG Embedding model loaded.")
    print(f"Connecting to ChromaDB at: {DB_PATH}")
    # Ensure chromadb is installed: pip install chromadb
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    rag_collection = chroma_client.get_collection(name=COLLECTION_NAME)
    print(f"Connected to ChromaDB collection '{COLLECTION_NAME}'. Count: {rag_collection.count()}")
except ImportError:
    print(f"ERROR: Required library not found. Please run: pip install chromadb sentence-transformers")
except Exception as e:
    print(f"ERROR initializing ChromaDB or RAG embedding model: {e}")
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

# --- RAG-Integrated AI Generation View ---

def nation_generate_dm(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    generated_code = "# Generation failed or prerequisites missing."
    error_message = None
    prompt_used = ""
    retrieved_context = "RAG system inactive or failed." # Default

    try:
        # --- RAG Retrieval Step ---
        rag_context_for_prompt = ""
        if rag_collection and embedding_model_rag: # Check if DB/model initialized okay
            try:
                print("Performing RAG query...")
                query_text = f"{nation.name} {nation.description}"
                query_embedding = embedding_model_rag.encode([query_text]).tolist()
                results = rag_collection.query(
                    query_embeddings=query_embedding,
                    n_results=5 # Number of context chunks to retrieve
                )
                if results and results.get('documents'):
                    retrieved_docs = results['documents'][0]
                    retrieved_context = "\n---\n".join(retrieved_docs) # Join chunks for display
                    rag_context_for_prompt = f"Relevant Game Data Context:\n```\n{retrieved_context}\n```\n\n" # Format for prompt
                    print(f"Retrieved {len(retrieved_docs)} context chunks.")
                else:
                     retrieved_context = "No relevant documents found in vector DB."
                     print("WARN: No relevant docs found in RAG query.")

            except Exception as rag_e:
                print(f"Error during RAG retrieval: {rag_e}")
                retrieved_context = f"Error during RAG retrieval: {rag_e}"
                error_message = "Failed to retrieve context from Vector DB."
        else:
             retrieved_context = "RAG components (DB/Embedding Model) not initialized correctly."
             error_message = retrieved_context # Pass initialization error to template
             print("WARN: Skipping RAG query due to initialization failure.")
        # --- End RAG Retrieval ---

        # Check for API Key again, in case it failed silently before
        loaded_api_key = config('GEMINI_API_KEY', default=None)
        if not loaded_api_key:
            raise ValueError("Gemini API Key not found in environment variables.")

        # Select the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Construct the prompt WITH RAG CONTEXT
        prompt = f"""You are an expert Dominions 6 modder creating a new nation mod file (.dm format).
Use the following retrieved game data context to ensure accuracy for stats, names, and abilities where relevant. If context is missing or doesn't apply, use reasonable defaults based on the Nation Name and Description.

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
- #startunittype1 "{nation.name} Infantry"
- #startunittype2 "{nation.name} Skirmisher"
- #dominionstr <number>
- #castleprod <number>
Also generate the '#newmonster' blocks for the 3 starting units mentioned above, including basic stats (#hp, #str, #att, #def, #prec, #mor, #mr, #move, #ap), costs (#recruitcost, #resourcecost, #upkeep), basic #weapon/#armor suggestions (using names), and appropriate tags (#commander, #infantry, #startunit etc.).

Output only the raw .dm commands.
"""
        prompt_used = prompt

        # Make the API call
        print("Attempting to call Gemini API...")
        response = model.generate_content(prompt)
        print("Gemini API call completed.")

        # Process the response
        try:
            generated_code = response.text
            if not generated_code.strip(): generated_code = "# Error: AI response was empty."
        except ValueError:
             generated_code = f"# Error: AI response blocked or invalid."
             error_message = f"AI Response Feedback: {response.prompt_feedback}"
        except Exception as resp_err:
             generated_code = f"# Error: Could not parse AI response."
             error_message = f"Error processing AI response: {resp_err}"

    # --- Exception Handling ---
    except ValueError as ve: # Catch missing key error specifically
        print(f"Configuration Error: {ve}")
        error_message = str(ve)
        generated_code = f"Error: Configuration problem ({ve}). Check .env file."
    except NameError as ne: # Catch error if 'genai', 'chromadb', or 'SentenceTransformer' is not defined (library not installed/imported)
         print(f"NameError: {ne}. Required library missing or import failed?")
         error_message = f"Required library not available ({ne}). Please run pip install."
         generated_code = "Error: Required library missing."
    except Exception as e: # Catch other potential errors (API call errors, network issues, ChromaDB errors during query etc.)
        print(f"Error during generation view: {e}")
        error_message = f"An error occurred: {e}"
        generated_code = f"Error: Could not generate code ({e})."

    context = {
        'nation': nation,
        'generated_code': generated_code,
        'error_message': error_message,
        'prompt_used': prompt_used,
        'retrieved_context': retrieved_context, # Pass RAG context to template
    }
    return render(request, 'nations/nation_generate_dm.html', context)