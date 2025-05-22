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

# Debugging loop
from django.conf import settings 
from django.http import HttpResponse

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

def debug_settings_view(request):
    """A temporary view to inspect crucial Django settings at runtime."""
    debug_info = {
        "DEBUG": settings.DEBUG,
        "SECURE_SSL_REDIRECT": getattr(settings, 'SECURE_SSL_REDIRECT', 'NOT SET'),
        "SECURE_PROXY_SSL_HEADER": getattr(settings, 'SECURE_PROXY_SSL_HEADER', 'NOT SET'),
        "CSRF_COOKIE_SECURE": getattr(settings, 'CSRF_COOKIE_SECURE', 'NOT SET'),
        "SESSION_COOKIE_SECURE": getattr(settings, 'SESSION_COOKIE_SECURE', 'NOT SET'),
        "SECURE_HSTS_SECONDS": getattr(settings, 'SECURE_HSTS_SECONDS', 'NOT SET'),
        "ALLOWED_HOSTS": settings.ALLOWED_HOSTS,
    }
    response_content = "<h1>Django Settings Debug</h1><pre>"
    for key, value in debug_info.items():
        response_content += f"{key}: {value}\n"
    response_content += "</pre>"
    return HttpResponse(response_content)


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
        generation_model = genai.GenerativeModel('gemini-2.0-flash')

        # Build the big prompt with instructions and the retrieved context.
        prompt = f"""You are an expert Dominions 6 modder creating a new nation mod file (.dm format).
Use the following retrieved game data context (Nation Data) and modding guideline context (Guideline Data) to ensure accuracy and correct syntax. If context is missing or doesn't apply, use reasonable defaults based on the Nation Name and Description provided below the context. Prioritize guideline context for syntax questions.

{rag_context_for_prompt}
Task: Generate the entire nation definition block AND 1 paragraph definitions for 8 basic starting units (2 Commander, 1 mage, 1 priest, 4 troops). Start the nation block exactly with '#newnation' and end it exactly with '#end'. Start each unit block exactly with '#newmonster' and end it exactly with '#end'. Do not include explanations or markdown formatting outside the required commands. also add the weapons and armors in if creating new ones instead of using preexisting ones.

Nation Name: {nation.name}
Nation Description: {nation.description}

Output only the raw .dm commands ensuring to query the RAG databases to stay consistent with syntax and proper and contextual ID usage.

Also adhering to the following template

#modname "MyNewNation Mod"
#description "Autogenerated mod for the nation of MyNewNation, based on the description: A description of MyNewNation."
#version 1.0
#domversion 6.28 -- Specify the target Dominions 6 version
#icon "MYNEWNATION_icon.tga" -- Placeholder icon, required for mod visibility in list

-- =============================================================================
-- MONSTER DEFINITIONS (Units & Commanders)
-- ID Range: 5000-8999
-- =============================================================================

-- == Units ==

-- Unit Summary:
-- ID: 5000
-- Name: MyNewNation Militia
-- Role: Basic Chaff Infantry
-- Cost: G:10 R:10 RP:1
-- Stats: HP:10 Prot:2 MR:10 Att:10 Def:10 Mor:10
-- Abilities: Standard Human
#newmonster 5000
#name "MyNewNation Militia"
#descr "Basic militia levied from the populace. Poorly equipped but numerous."
#spr1 "MYNEWNATION_militia_sprite.tga"
#spr2 "MYNEWNATION_militia_attack_sprite.tga"
-- Core Stats
#hp 10
#str 10
#att 10
#def 10
#prec 10
#prot 2 -- Light protection from basic gear
#mr 10
#mor 10
#enc 3 -- Standard enc for light infantry
#mapmove 16
#ap 20 -- Standard combat speed
#size 2
-- Costs
#gcost 10
#rcost 10
#rpcost 1
-- Abilities & Slots
#noleader
#itemslots 6 -- Two hands, head, body, feet, misc
#bodytype human
#standard 10 -- Basic standard bearer effect
-- Equipment
#weapon "Spear" -- Standard militia weapon
#armor "Leather Cap"
#armor "Leather Armor"
#end

-- Unit Summary:
-- ID: 5001
-- Name: MyNewNation Archer
-- Role: Basic Ranged Support
-- Cost: G:12 R:8 RP:1
-- Stats: HP:10 Prot:1 MR:10 Att:9 Def:8 Prec:11 Mor:10
-- Abilities: Standard Human
#newmonster 5001
#name "MyNewNation Archer"
#descr "Archers providing ranged support, lightly armored."
#spr1 "MYNEWNATION_archer_sprite.tga"
#spr2 "MYNEWNATION_archer_attack_sprite.tga"
-- Core Stats
#hp 10
#str 10
#att 9
#def 8
#prec 11 -- Slightly better precision for archers
#prot 1 -- Very light protection
#mr 10
#mor 10
#enc 3
#mapmove 16
#ap 20
#size 2
-- Costs
#gcost 12
#rcost 8
#rpcost 1
-- Abilities & Slots
#noleader
#itemslots 6
#bodytype human
-- Equipment
#weapon "Short Bow"
#weapon "Dagger" -- Melee backup
#armor "Leather Cap"
#end

-- Unit Summary:
-- ID: 5002
-- Name: MyNewNation Heavy Infantry
-- Role: Mainline Heavy Infantry
-- Cost: G:15 R:20 RP:2
-- Stats: HP:12 Prot:10 MR:11 Att:11 Def:11 Mor:12
-- Abilities: Standard Human
#newmonster 5002
#name "MyNewNation Heavy Infantry"
#descr "Well-equipped heavy infantry forming the core of the army."
#spr1 "MYNEWNATION_heavyinf_sprite.tga"
#spr2 "MYNEWNATION_heavyinf_attack_sprite.tga"
-- Core Stats
#hp 12
#str 11
#att 11
#def 11
#prec 10
#prot 10 -- Decent protection
#mr 11
#mor 12
#enc 5 -- Higher enc due to heavier gear
#mapmove 14 -- Slower map move
#ap 22 -- Slightly slower combat speed
#size 2
-- Costs
#gcost 15
#rcost 20
#rpcost 2
-- Abilities & Slots
#noleader
#itemslots 6
#bodytype human
#standard 10
-- Equipment
#weapon "Broad Sword"
#weapon "Medium Shield"
#armor "Helmet"
#armor "Chain Mail Hauberk"
#end

-- Unit Summary:
-- ID: 5003
-- Name: MyNewNation Sacred Guard
-- Role: Elite Sacred Infantry
-- Cost: G:25 R:25 RP:3 Holy:1
-- Stats: HP:14 Prot:12 MR:13 Att:12 Def:12 Mor:14
-- Abilities: Sacred, Standard Human
#newmonster 5003
#name "MyNewNation Sacred Guard"
#descr "Elite warriors dedicated to the nation's god, heavily armed and armored."
#spr1 "MYNEWNATION_sacred_sprite.tga"
#spr2 "MYNEWNATION_sacred_attack_sprite.tga"
-- Core Stats
#hp 14
#str 12
#att 12
#def 12
#prec 10
#prot 12 -- Good protection
#mr 13
#mor 14
#enc 6
#mapmove 14
#ap 24
#size 2
-- Costs
#gcost 25
#rcost 25
#rpcost 3
#holycost 1 -- Cost 1 Holy Point (used in prophet turns)
-- Abilities & Slots
#holy -- Sacred Unit
#noleader
#itemslots 6
#bodytype human
#standard 10
-- Equipment
#weapon "Great Sword"
#armor "Full Helmet"
#armor "Plate Hauberk"
#end

-- == Commanders ==

-- Commander Summary:
-- ID: 5004
-- Name: MyNewNation Scout
-- Role: Basic Scout
-- Cost: G:30 R:5 RP:1
-- Stats: HP:10 Prot:1 MR:10 Att:8 Def:8 Mor:10
-- Abilities: Stealthy, Survival Skills, Poor Leader
#newmonster 5004
#name "MyNewNation Scout"
#descr "A scout used for exploring provinces and spying."
#spr1 "MYNEWNATION_scout_sprite.tga"
#spr2 "MYNEWNATION_scout_attack_sprite.tga"
-- Core Stats
#hp 10
#str 9
#att 8
#def 8
#prec 10
#prot 1
#mr 10
#mor 10
#enc 3
#mapmove 20 -- High map movement
#ap 20
#size 2
-- Costs
#gcost 30
#rcost 5
#rpcost 1
-- Abilities & Slots
#poorleader -- Can lead 10 troops
#itemslots 6
#bodytype human
#stealthy 50 -- Standard stealth
#forestsurvival
#mountainsurvival
#swampsurvival
#spy
-- Equipment
#weapon "Dagger"
#end

-- Commander Summary:
-- ID: 5005
-- Name: MyNewNation Commander
-- Role: Basic Troop Leader
-- Cost: G:50 R:15 RP:1
-- Stats: HP:12 Prot:10 MR:11 Att:11 Def:11 Mor:12
-- Abilities: Standard Human, Good Leader
#newmonster 5005
#name "MyNewNation Commander"
#descr "A standard commander capable of leading troops into battle."
#spr1 "MYNEWNATION_commander_sprite.tga"
#spr2 "MYNEWNATION_commander_attack_sprite.tga"
-- Core Stats
#hp 12
#str 11
#att 11
#def 11
#prec 10
#prot 10
#mr 11
#mor 12
#enc 5
#mapmove 14
#ap 22
#size 2
-- Costs
#gcost 50
#rcost 15
#rpcost 1
-- Abilities & Slots
#goodleader -- Can lead 80 troops
#itemslots 6
#bodytype human
#standard 10
-- Equipment
#weapon "Broad Sword"
#weapon "Medium Shield"
#armor "Helmet"
#armor "Chain Mail Hauberk"
#end

-- Commander Summary:
-- ID: 5006
-- Name: MyNewNation Priest
-- Role: Basic Priest / Holy Caster
-- Cost: G:60 R:10 RP:1
-- Stats: HP:10 Prot:2 MR:12 Att:9 Def:9 Mor:13
-- Abilities: Standard Human, Priest (H1), Ok Leader
#newmonster 5006
#name "MyNewNation Priest"
#descr "A priest spreading the faith and leading sacred troops."
#spr1 "MYNEWNATION_priest_sprite.tga"
#spr2 "MYNEWNATION_priest_attack_sprite.tga"
-- Core Stats
#hp 10
#str 9
#att 9
#def 9
#prec 10
#prot 2
#mr 12
#mor 13
#enc 3
#mapmove 16
#ap 20
#size 2
-- Costs
#gcost 60
#rcost 10
#rpcost 1
-- Abilities & Slots
#okleader -- Can lead 40 troops
#itemslots 6
#bodytype human
#magicskill 9 1 -- Priest Level 1 (Holy Path)
#spreaddom 1 -- Spreads dominion
-- Equipment
#weapon "Mace"
#armor "Leather Armor"
#reqtemple -- Requires a temple to recruit
#end

-- Commander Summary:
-- ID: 5007
-- Name: MyNewNation Mage
-- Role: Basic Research/Battle Mage
-- Cost: G:110 R:10 RP:2
-- Stats: HP:10 Prot:2 MR:13 Att:9 Def:9 Mor:11
-- Abilities: Standard Human, Mage (e.g., F1/A1), Ok Leader
#newmonster 5007
#name "MyNewNation Mage"
#descr "A mage capable of research and casting minor spells."
#spr1 "MYNEWNATION_mage_sprite.tga"
#spr2 "MYNEWNATION_mage_attack_sprite.tga"
-- Core Stats
#hp 10
#str 9
#att 9
#def 9
#prec 10
#prot 2
#mr 13
#mor 11
#enc 3
#mapmove 16
#ap 20
#size 2
-- Costs
#gcost 110 -- Standard cost for a basic 1-path mage
#rcost 10
#rpcost 2
-- Abilities & Slots
#okleader
#itemslots 6
#bodytype human
#magicskill 0 1 -- Example: Fire 1 (Path 0)
#magicskill 1 1 -- Example: Air 1 (Path 1) - Adjust paths based on inferred theme
-- Equipment
#weapon "Quarterstaff"
#armor "Leather Armor"
#reqlab -- Requires a lab to recruit
#end

-- Commander Summary:
-- ID: 5008
-- Name: MyNewNation Sacred Commander
-- Role: Leader of Sacreds, Higher Priest
-- Cost: G:150 R:25 RP:2
-- Stats: HP:14 Prot:12 MR:14 Att:12 Def:12 Mor:15
-- Abilities: Sacred, Standard Human, Priest (H2), Good Leader, Inspirational
#newmonster 5008
#name "MyNewNation Sacred Commander"
#descr "An inspiring leader of sacred troops and a more powerful priest."
#spr1 "MYNEWNATION_sacredcom_sprite.tga"
#spr2 "MYNEWNATION_sacredcom_attack_sprite.tga"
-- Core Stats
#hp 14
#str 12
#att 12
#def 12
#prec 10
#prot 12
#mr 14
#mor 15
#enc 6
#mapmove 14
#ap 24
#size 2
-- Costs
#gcost 150
#rcost 25
#rpcost 2
-- Abilities & Slots
#holy -- Sacred Unit
#goodleader
#inspirational 1 -- +1 Morale to led troops
#itemslots 6
#bodytype human
#magicskill 9 2 -- Priest Level 2 (Holy Path)
#spreaddom 1
-- Equipment
#weapon "Mace" -- Or thematic holy weapon
#armor "Full Helmet"
#armor "Plate Hauberk"
#reqtemple
#end

-- =============================================================================
-- NATION DEFINITION
-- ID Range: 150+
-- =============================================================================

#newnation 150 -- Assigning the first mod nation ID
#name "MyNewNation"
#epithet "The Placeholder Kingdom" -- Generic epithet
#era 2 -- Defaulting to Middle Age (1=EA, 2=MA, 3=LA)
#descr "A description of MyNewNation." -- User provided description
#summary "A generic nation template with basic infantry, archers, and commanders. Features sacred guards and basic mages/priests."
#brief "Generic MA Nation Template"
#color 0.6 0.6 0.6 -- Neutral grey color
#secondarycolor 0.8 0.8 0.8 -- Lighter grey secondary
#flag "MYNEWNATION_flag.tga" -- Placeholder flag
#homerealm 10 -- Defaulting to Magic realm (adjust based on theme)
#likesterr 1 -- Likes Plains (bitmask 1)
#idealcold 0 -- Neutral temperature preference

-- Recruitment List (Linking defined monsters)
#clearrec -- Ensure vanilla units aren't recruitable by default
#addrecunit "MyNewNation Militia" -- ID 5000
#addrecunit "MyNewNation Archer" -- ID 5001
#addrecunit "MyNewNation Heavy Infantry" -- ID 5002
#addrecunit "MyNewNation Sacred Guard" -- ID 5003

#addreccom "MyNewNation Scout" -- ID 5004
#addreccom "MyNewNation Commander" -- ID 5005
#addreccom "MyNewNation Priest" -- ID 5006
#addreccom "MyNewNation Mage" -- ID 5007
#addreccom "MyNewNation Sacred Commander" -- ID 5008

-- Starting Army
#startcom "MyNewNation Commander" -- Start with a basic commander (ID 5005)
#startunit "MyNewNation Militia" 20 -- Start with some basic troops
#startunit "MyNewNation Heavy Infantry" 10 -- Start with some better troops
#startunit "MyNewNation Archer" 10 -- Start with some archers

-- Forts & Buildings (Using defaults unless theme suggests otherwise)
#homefort 1 -- Standard Palisade
#buildfort 1 -- Builds Palisades by default

-- Pretender God List (Add thematic choices based on inference)
#cleargods -- Remove default realm gods
#addgod "Father of Monsters" -- Example: Generic Monster Pretender (ID 24)
#addgod "Arch Mage" -- Example: Generic Mage Pretender (ID 251)
#addgod "Oracle" -- Example: Generic Priest/Astral Pretender (ID 272)
#addgod "Virtue" -- Example: Generic Immobile Pretender (ID 268)
-- #addgod "[Custom Pretender Monster Name/ID]" -- Add custom pretenders here if defined
-- Custom pretenders must have #pathcost and #startdom defined in their monster block.

-- National Settings/Bonuses (Add based on inference)
-- Example: #castleprod 10 -- 10% resource bonus in castles
-- Example: #holyfire -- Priests smite with holy fire

#end -- End of nation definition

-- =============================================================================
-- (Optional) CUSTOM SPELLS / ITEMS / SITES / EVENTS
-- Define below if strongly inferred from description and theme.
-- Remember load order: Spells -> Items -> General -> Poptypes -> Mercs -> Events
-- Ensure spells/items use #restricted [Nation ID] (e.g., #restricted 150)
-- Ensure sites use #nat [Nation ID] for nation-specific recruitment
-- =============================================================================

-- Example Custom Site (if inferred)
-- #newsite 1500 -- Use Site IDs 1500-1999
-- #name "Sacred Grove of MyNewNation"
-- #level 6 1 -- Found by N1 mages
-- #rarity 50
-- #path 6 1 -- Provides 1 Nature Gem
-- #descr "A grove sacred to the people of MyNewNation."
-- #nat 150 -- Link to our nation ID
-- #natcom "MyNewNation Priest" -- Allow recruiting national priest here
-- #end
-- (Remember to add #startsite "Sacred Grove of MyNewNation" in the nation block above)

-- Example Custom Spell (if inferred)
-- #newspell -- Spell IDs automatically assigned or use 1300+
-- #name "Blessing of MyNewNation"
-- #descr "A divine blessing unique to MyNewNation's priests."
-- #school 7 -- Divine School
-- #path 0 9 -- Holy Path
-- #level 1 -- H1 required
-- #fatiguecost 100
-- #range 0 -- Self
-- #aoe 1 -- Caster Only
-- #effect 10 -- Bless effect
-- #restricted 150 -- Make it national
-- #end

-- Example Custom Item (if inferred)
-- #newitem 500 -- Use Item IDs 500+
-- #name "Amulet of MyNewNation"
-- #descr "An amulet granting minor protection, crafted only by MyNewNation."
-- #constlevel 2 -- Construction 2
-- #mainpath 3 -- Earth Path
-- #mainlevel 1 -- E1 required
-- #gems 5 -- Costs 5 Earth gems
-- #type 3 -- Misc Item slot
-- #prot 1 -- Grants +1 protection
-- #restricted 150 -- Make it national
-- #end

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