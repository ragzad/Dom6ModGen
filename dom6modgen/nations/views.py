# Dom6ModGen/dom6modgen/nations/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt # Using for simplicity in example. For production, ensure CSRF token is handled correctly by JS.
import json
import logging # For better server-side logging.
import os # For API keys from environment

# Your existing models and forms
from .models import Nation, ModGenerationJob # Import ModGenerationJob
from .forms import NationForm

# AI library imports
import google.generativeai as genai
from google.cloud import aiplatform # If you're still using Vertex AI for RAG
from decouple import config # If you use python-decouple for env vars

# --- Initialize a logger for this module ---
logger = logging.getLogger(__name__)

# --- AI Model Configuration & Initialization ---
# It's good practice to configure your API keys once, ideally when the app starts.
# Your original views.py had this logic spread out, so centralizing parts of it.

# Attempt to configure Gemini API Key from environment variables.
try:
    GEMINI_API_KEY = config('GEMINI_API_KEY', default=os.environ.get('GEMINI_API_KEY')) # Try decouple then os.environ
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("Gemini API Key configured successfully.")
    else:
        logger.warning("GEMINI_API_KEY not found in environment. AI generation features will likely fail.")
except Exception as e:
    logger.error(f"Error configuring Gemini API: {e}")

# Define preferred models for different tasks.
# Using "latest" can be good for updates but might introduce unexpected changes.
# Consider pinning to specific versions for more stability, e.g., 'gemini-1.5-flash-001'
PLANNING_MODEL_NAME = 'gemini-1.5-flash-latest' 
COMPONENT_MODEL_NAME = 'gemini-1.5-flash-latest' 

# Standard safety settings for Gemini. Adjust as needed.
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# --- Vertex AI RAG Setup (from your original file, keep if needed for RAG) ---
# GCP_PROJECT_ID = config('GCP_PROJECT_ID', default=None)
# ... (rest of your Vertex AI setup if you intend to use it for RAG with components)
# For this client-side example, RAG within each component call is simplified/omitted
# in the `generate_component_view` prompt for brevity, but you can re-integrate it there.

def get_gemini_model(model_name_str):
    """Helper to get a configured Gemini model instance."""
    if not genai.API_KEY: # Check if API key was configured
        logger.error("Gemini API Key not configured. Cannot get model.")
        raise ValueError("Gemini API Key not found or not configured.")
    return genai.GenerativeModel(model_name_str)

def generate_with_gemini(model_name, prompt_text, is_json_output=False):
    """
    Handles interaction with the Gemini API for content generation.
    This is a key function where you ask the AI to do its magic.
    It includes basic error handling and an option for JSON output.
    """
    try:
        model = get_gemini_model(model_name)
        # Log a snippet of the prompt to help with debugging.
        logger.info(f"Sending prompt to Gemini model {model_name} (JSON output: {is_json_output}). Prompt snippet:\n{prompt_text[:500]}...")
        
        generation_config = None
        if is_json_output:
            # Newer Gemini versions support a direct JSON response mode.
            try:
                 generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
                 logger.info("Attempting to use response_mime_type='application/json'.")
            except Exception as e:
                logger.warning(f"Could not set response_mime_type to application/json for model {model_name}: {e}. Will proceed with text and parse.")

        response = model.generate_content(
            prompt_text,
            generation_config=generation_config,
            safety_settings=SAFETY_SETTINGS # Apply safety settings
        )

        # It's crucial to check if the response was blocked or empty.
        if not response.parts:
             logger.warning(f"Gemini response for model {model_name} was empty or blocked. Feedback: {response.prompt_feedback}")
             if response.prompt_feedback and response.prompt_feedback.block_reason:
                 # Provide a more user-friendly message if blocked.
                 raise ValueError(f"AI content generation blocked: {response.prompt_feedback.block_reason_message or response.prompt_feedback.block_reason.name}")
             raise ValueError("AI returned an empty response (no parts).")

        generated_text = response.text # Get the text content.
        logger.info(f"Received response from Gemini model {model_name}. Text snippet:\n{generated_text[:500]}...")

        if is_json_output:
            # If we asked for JSON, try to parse it.
            # Sometimes the model might still wrap JSON in markdown even with mime_type.
            if generated_text.strip().startswith("```json"):
                logger.info("Detected JSON wrapped in markdown, attempting to strip.")
                generated_text = generated_text.strip()[7:] # Remove ```json
                if generated_text.strip().endswith("```"):
                    generated_text = generated_text.strip()[:-3] # Remove ```
            return json.loads(generated_text.strip()) # Parse the cleaned text.
        return generated_text.strip() # For non-JSON, just return the stripped text.

    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError for model {model_name} when expecting JSON: {e}. Raw text received: {generated_text}")
        raise ValueError(f"AI did not return valid JSON. Error: {e}. Check logs for raw output.")
    except ValueError as ve: # Catch our specific ValueErrors or those from Gemini library
        logger.error(f"ValueError during Gemini call with model {model_name}: {ve}")
        raise # Re-raise to be caught by the calling view.
    except Exception as e:
        # Catch-all for other unexpected issues during the API call.
        logger.error(f"Generic exception during Gemini call with model {model_name}: {e}", exc_info=True)
        # Try to get more detailed error from response if it exists (e.g. safety blocks not caught above)
        if 'response' in locals() and hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
             raise ValueError(f"AI content generation failed or was blocked: {response.prompt_feedback.block_reason_message or response.prompt_feedback.block_reason.name}")
        raise ValueError(f"An unexpected error occurred with the AI model: {e}")

# --- Standard Django Views (List, Detail, Create, Update, Delete) ---
# These are your existing views for managing Nations.
def nation_list(request):
    nations = Nation.objects.all().order_by('name')
    context = { 'nations': nations }
    return render(request, 'nations/nation_list.html', context)

def nation_detail(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    # For the detail page, you might want to show existing generation jobs for this nation
    jobs = ModGenerationJob.objects.filter(nation=nation).order_by('-created_at')
    context = { 'nation': nation, 'mod_jobs': jobs }
    return render(request, 'nations/nation_detail.html', context) # Assuming nation_detail.html can show jobs

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

# --- Views for Interactive, Client-Side Orchestrated Mod Generation ---

def nation_generate_interactive_page(request, pk):
    """
    Renders the HTML page that contains the JavaScript for interactive generation.
    This page will be the main interface for the user to start and monitor the process.
    """
    nation = get_object_or_404(Nation, pk=pk)
    context = {
        'nation': nation,
    }
    logger.info(f"Rendering interactive generation page for Nation PK {pk}: {nation.name}")
    return render(request, 'nations/nation_generate_interactive.html', context)

@require_POST
@csrf_exempt # For production, ensure your JS sends the CSRF token with AJAX.
def initiate_mod_generation(request, nation_pk):
    """
    API Endpoint: Phase 1 - Create a ModGenerationJob and get the AI to generate a "plan".
    The plan is a JSON structure outlining all components to be generated.
    This is called once by the client's JavaScript when the user clicks "Start Generation".
    """
    nation = get_object_or_404(Nation, pk=nation_pk)
    # Create a new job record for this nation.
    job = ModGenerationJob.objects.create(nation=nation, status='PENDING_PLAN')
    logger.info(f"Initiating mod generation (API) for Nation PK {nation_pk}, created Job ID {job.id}")

    try:
        job.status = 'PLANNING' # Update status to show we're working on it.
        job.save()

        # This prompt is crucial! It needs to guide the AI to return a reliable JSON plan.
        plan_prompt = f"""
        You are a planning assistant for a Dominions 6 mod generator.
        Based on the nation named '{nation.name}' with the description: '{nation.description}',
        generate a detailed plan as a JSON object for all components required to create a complete and functional mod.

        The JSON object MUST have top-level keys: "nation_meta", "commanders", "mages", "priests", "troops".
        Each key should map to an object or an array of objects.
        
        - "nation_meta": An object with:
            - "id": "nation_block" (fixed string, this is the component's unique ID in the plan)
            - "component_type": "nation_meta" (fixed string)
            - "name_hint": "{nation.name} Main Details" (for UI display)
            - "concept": "Overall theme, era (EA, MA, LA), visual style, core gameplay ideas. For example: 'A militaristic MA nation of desert nomads, focusing on cavalry and fire magic.'"
            - "epithet_suggestion": "e.g., The Sunken Kingdom"
            - "era_suggestion": "MA" (must be EA, MA, or LA)
            - "summary_suggestion": "A brief summary for the mod file's #description line."
            - "color_suggestions": {{ "primary_rgb": [0.8, 0.2, 0.1], "secondary_rgb": [0.5, 0.5, 0.5] }} (RGB values 0.0-1.0)

        - "commanders": An array of 2 objects, each representing a non-magic military commander. Each object with:
            - "id": "commander_1", "commander_2" (unique ID for this component in the plan)
            - "component_type": "commander" (fixed string)
            - "name_hint": "e.g., Desert Captain, Dune Warlord" (for UI display)
            - "concept": "Brief concept (e.g., 'Standard troop leader, good morale.', 'Scout, stealthy, fast map move.')."

        - "mages": An array of 1-2 objects (you decide if 1 or 2 is more appropriate based on nation concept). Each object with:
            - "id": "mage_1", "mage_2" (if two)
            - "component_type": "mage" (fixed string)
            - "name_hint": "e.g., Sand Sorcerer, Oasis Seer"
            - "concept": "Brief concept including potential magic paths/themes (e.g., 'Fire & Air mage, good researcher.', 'Nature & Water utility mage focusing on summons and site searching.')."

        - "priests": An array of 1 object. Each object with:
            - "id": "priest_1"
            - "component_type": "priest" (fixed string)
            - "name_hint": "e.g., Sun Disciple, Oracle of the Sands"
            - "concept": "Brief concept (e.g., 'Standard H1 priest, good for spreading dominion and leading sacreds.')."
        
        - "troops": An array of 3-4 objects (you decide number based on nation concept). Each object with:
            - "id": "troop_1", "troop_2", "troop_3", "troop_4" (if four)
            - "component_type": "troop" (fixed string)
            - "name_hint": "e.g., Nomad Spearman, Dune Archer, Sand Stalker (Sacred)"
            - "concept": "Brief concept including role (e.g., 'Basic spear infantry, cheap and numerous.', 'Light archer unit.', 'Elite sacred cavalry unit, expensive but powerful.'). Specify if it should be sacred."

        Assign unique "id" strings for each component within the plan (e.g., "commander_1", "troop_3"). These IDs are critical.
        The output MUST be ONLY the JSON object. Do not include any other text, explanations, or markdown formatting like ```json.
        Adhere strictly to the requested JSON structure.
        """
        
        # Call the AI to get the plan. We expect JSON output.
        parsed_plan = generate_with_gemini(PLANNING_MODEL_NAME, plan_prompt, is_json_output=True)
        
        job.plan_details = parsed_plan
        job.status = 'PLAN_GENERATED' # Plan is successfully created.
        
        # Initialize component_statuses based on the plan for UI tracking by the client.
        # All components start as 'pending'.
        statuses = {}
        # Helper to add components to the statuses dict
        def add_to_statuses(component_item):
            if isinstance(component_item, dict) and "id" in component_item:
                statuses[component_item["id"]] = "pending"
            else:
                logger.warning(f"Malformed component item in plan for Job ID {job.id}: {component_item}")


        if "nation_meta" in parsed_plan and isinstance(parsed_plan["nation_meta"], dict):
             add_to_statuses(parsed_plan["nation_meta"])
        else:
            logger.error(f"Plan for job {job.id} is missing 'nation_meta' or it's not a dict.")
            raise ValueError("AI plan generation failed: 'nation_meta' is missing or malformed.")

        for component_type_key in ["commanders", "mages", "priests", "troops"]:
            if component_type_key in parsed_plan and isinstance(parsed_plan[component_type_key], list):
                for comp in parsed_plan[component_type_key]:
                    add_to_statuses(comp)
            else:
                logger.warning(f"Plan for job {job.id} is missing '{component_type_key}' or it's not a list.")
                # Depending on requirements, you might want to raise an error here if certain lists are mandatory.
                # For now, we'll allow them to be potentially missing from the AI's plan.

        job.component_statuses = statuses
        job.save()

        logger.info(f"Plan successfully generated and saved for Job ID {job.id}.")
        # Return the job ID and the plan to the client.
        return JsonResponse({'job_id': job.id, 'plan': job.plan_details, 'component_statuses': job.component_statuses})

    except ValueError as ve: # Catch errors from generate_with_gemini or other ValueErrors
        job.status = 'FAILED_PLANNING'
        job.error_message = str(ve)
        job.save()
        logger.error(f"Planning phase failed for Job ID {job.id}: {ve}", exc_info=True)
        return JsonResponse({'error': str(ve), 'job_id': job.id}, status=500)
    except Exception as e:
        job.status = 'FAILED_PLANNING'
        job.error_message = f"An unexpected error occurred during planning: {e}"
        job.save()
        logger.error(f"Unexpected planning failure for Job ID {job.id}: {e}", exc_info=True)
        return JsonResponse({'error': job.error_message, 'job_id': job.id}, status=500)

@require_POST
@csrf_exempt # For production, ensure your JS sends the CSRF token with AJAX.
def generate_component_view(request):
    """
    API Endpoint: Phase 2 - Generate the .dm code for a single component.
    This is called iteratively by the client's JavaScript for each item in the plan.
    It takes the job_id and the specific component_id (from the plan) to generate.
    """
    try:
        data = json.loads(request.body)
        job_id = data.get('job_id')
        component_id_from_request = data.get('component_id') # This is the unique ID like "commander_1" or "nation_block"
        
        if not all([job_id, component_id_from_request]):
            logger.warning("generate_component_view called with missing job_id or component_id.")
            return JsonResponse({'error': 'Missing job_id or component_id in request.'}, status=400)

        job = get_object_or_404(ModGenerationJob, id=job_id)
        logger.info(f"Received request to generate component '{component_id_from_request}' for Job ID {job.id}")

        # Check if the job is in a state where component generation is allowed.
        if job.status not in ['PLAN_GENERATED', 'GENERATING_COMPONENTS', 'FAILED_COMPONENT']:
             logger.warning(f"Job {job.id} is in status '{job.status}', not ready for component generation.")
             return JsonResponse({'error': f'Job not in a valid state for component generation. Current status: {job.status}'}, status=400)

        # If this is the first component being generated for this job, update the overall job status.
        if job.status == 'PLAN_GENERATED':
            job.status = 'GENERATING_COMPONENTS'
            # No need to save yet, will be saved after component attempt.

        # Find the specific component's details from the stored plan in the job.
        component_plan_details = None
        component_type_from_plan = None # e.g., "commander", "troop", "nation_meta"

        # Look for the component_id_from_request within the job.plan_details
        if job.plan_details.get("nation_meta", {}).get("id") == component_id_from_request:
            component_plan_details = job.plan_details["nation_meta"]
        else:
            for type_key in ["commanders", "mages", "priests", "troops"]:
                if type_key in job.plan_details: # Check if the key exists in the plan
                    for item in job.plan_details[type_key]:
                        if isinstance(item, dict) and item.get("id") == component_id_from_request:
                            component_plan_details = item
                            break
                if component_plan_details:
                    break
        
        if not component_plan_details:
            error_msg = f"Component ID '{component_id_from_request}' not found in the plan for Job ID {job.id}."
            job.component_statuses[component_id_from_request] = "error" # Mark as error in job's tracking
            job.error_message = (job.error_message + "\n" + error_msg) if job.error_message else error_msg
            job.status = 'FAILED_COMPONENT' # Update overall job status
            job.save()
            logger.error(error_msg)
            return JsonResponse({'error': error_msg, 'job_id': job.id, 'component_id': component_id_from_request}, status=404)

        component_type_from_plan = component_plan_details.get("component_type", "unknown")
        job.component_statuses[component_id_from_request] = "processing" # Mark as processing
        job.save(update_fields=['status', 'component_statuses']) # Save current state before AI call

        # Construct a focused prompt for the AI to generate *only this component*.
        # This prompt needs to be carefully engineered for each component type.
        nation_overall_concept = job.plan_details.get("nation_meta", {}).get("concept", job.nation.description)
        
        # Base prompt structure
        prompt_lines = [
            f"You are an expert Dominions 6 modder generating a specific component for the nation '{job.nation.name}'.",
            f"Overall Nation Concept: \"{nation_overall_concept}\"",
            f"Nation's original user-provided description: \"{job.nation.description}\"\n",
            f"You are generating the component with ID: '{component_id_from_request}'",
            f"Component Type: \"{component_type_from_plan.capitalize()}\"",
            f"Component Name Hint (for #name tag if applicable): \"{component_plan_details.get('name_hint', 'N/A')}\"",
            f"Component Concept/Instructions: \"{component_plan_details.get('concept', 'N/A')}\"\n",
            "Task: Generate ONLY the raw Dominions 6 .dm code block for this specific component.",
            "- Start with the appropriate command (e.g., '#newnation', '#newmonster').",
            "- For monsters (#newmonster), DO NOT assign a numeric ID; use the exact placeholder 'TEMP_ID_PLACEHOLDER' (e.g., '#newmonster TEMP_ID_PLACEHOLDER').",
            "- For the nation block ('#newnation'), DO NOT assign a numeric ID; use the exact placeholder 'TEMP_NATION_ID_PLACEHOLDER'.",
            "- Ensure all necessary attributes, stats, and commands are included for a functional component based on its type and concept.",
            f"- If this component uses a #name tag, use: #name \"{component_plan_details.get('name_hint', 'Unnamed Component')}\"",
            "- Use placeholder sprite names like \"PLACEHOLDER_SPR1.TGA\" and \"PLACEHOLDER_SPR2.TGA\" for monsters.",
            "- Do NOT include any explanations, markdown, or any text outside the .dm code block itself.",
            "- The output must be ONLY the .dm code block, starting with the relevant command and ending with #end (if applicable)."
        ]

        # Add type-specific instructions
        if component_type_from_plan == "nation_meta":
            prompt_lines.extend([
                "\nSpecific instructions for '#newnation' block:",
                f"  - Use #epithet \"{job.plan_details.get('nation_meta', {}).get('epithet_suggestion', 'The Placeholder Kingdom')}\"",
                f"  - Use #era {job.plan_details.get('nation_meta', {}).get('era_suggestion', '2')} (1=EA, 2=MA, 3=LA)",
                f"  - Use #summary \"{job.plan_details.get('nation_meta', {}).get('summary_suggestion', 'A generated nation.')}\"",
                f"  - Use #color {job.plan_details.get('nation_meta', {}).get('color_suggestions', {}).get('primary_rgb', [0.5,0.5,0.5])}".replace('[','').replace(']','').replace(',',''), # Format as "0.5 0.5 0.5"
                f"  - Use #secondarycolor {job.plan_details.get('nation_meta', {}).get('color_suggestions', {}).get('secondary_rgb', [0.7,0.7,0.7])}".replace('[','').replace(']','').replace(',',''),
                f"  - Use #flag \"{job.nation.name.upper().replace(' ','_')}_FLAG.TGA\" (Placeholder)",
                "  - Do NOT add #addrecunit, #addreccom, or #start[...] commands; these are added during final compilation.",
                "  - Include basic site/fort settings like #homerealm 10, #likesterr 1, #idealcold 0, #homefort 1, #buildfort 1 unless the concept strongly implies otherwise."
            ])
        elif component_type_from_plan in ["commander", "mage", "priest", "troop"]:
            prompt_lines.extend([
                "\nSpecific instructions for '#newmonster' block:",
                "  - Include reasonable stats: #hp, #prot, #mr, #att, #def, #prec, #str, #mor, #enc, #mapmove, #ap, #size.",
                "  - Include costs: #gcost, #rcost, #rpcost.",
                "  - Include #itemslots (usually 6 for humanoids) and #bodytype (e.g., human, animal).",
                "  - If a commander type: add #noleader, #poorleader (10), #okleader (40), or #goodleader (80).",
                "  - If a mage: add relevant #magicskill (e.g., #magicskill 0 1 for F1) based on its concept.",
                "  - If a priest: add #magicskill 9 1 (for H1). Higher levels if concept implies.",
                "  - Consider #holy, #sacredrec (if troop), #reqlab (if mage), #reqtemple (if priest) based on concept.",
                "  - If the concept mentions 'sacred', ensure the unit has the #holy tag."
            ])
        
        final_prompt = "\n".join(prompt_lines)
        
        generated_dm_snippet = generate_with_gemini(COMPONENT_MODEL_NAME, final_prompt)

        if not generated_dm_snippet or not generated_dm_snippet.strip().startswith(("#newnation", "#newmonster")):
            # Basic validation: does it start with an expected command?
            logger.error(f"AI returned an invalid or empty snippet for component {component_id_from_request}, Job {job.id}. Snippet: '{generated_dm_snippet}'")
            raise ValueError(f"AI returned an invalid or empty snippet for '{component_plan_details.get('name_hint', component_id_from_request)}'. It did not start with a recognized command.")
        
        # Store the successfully generated snippet.
        job.generated_snippets[component_id_from_request] = generated_dm_snippet
        job.component_statuses[component_id_from_request] = "done"
        
        # Check if all components planned are now marked as 'done' or 'error'.
        all_components_attempted = all(
            status in ["done", "error"] for status in job.component_statuses.values()
        )
        if all_components_attempted and len(job.component_statuses) == sum(len(v) if isinstance(v,list) else 1 for k,v in job.plan_details.items()): # Ensure all planned items have a status
            job.status = 'COMPONENTS_GENERATED' # Mark that this phase is complete.
        
        job.save() # Save snippet, component status, and potentially overall job status.

        logger.info(f"Component '{component_id_from_request}' generated successfully for Job ID {job.id}.")
        return JsonResponse({
            'message': f"Component '{component_plan_details.get('name_hint', component_id_from_request)}' generated successfully.",
            'job_id': job.id,
            'component_id': component_id_from_request,
            'snippet': generated_dm_snippet, # Send snippet back to JS for display.
            'component_statuses': job.component_statuses, # Send updated statuses.
            'overall_status': job.status # Send updated overall job status.
        })

    except ModGenerationJob.DoesNotExist:
        logger.error(f"Generate component request for non-existent Job ID: {data.get('job_id') if data else 'N/A'}")
        return JsonResponse({'error': 'Job not found.'}, status=404)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in generate_component_view request body: {request.body}", exc_info=True)
        return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)
    except ValueError as ve: # Catch errors from generate_with_gemini or other ValueErrors
        error_msg = str(ve)
        logger.error(f"Component generation failed for Job ID {job_id if 'job_id' in locals() else 'N/A'}, Component ID {component_id_from_request if 'component_id_from_request' in locals() else 'N/A'}: {error_msg}", exc_info=True)
        # Ensure job and component_id_from_request are defined before trying to update status
        if 'job' in locals() and job and 'component_id_from_request' in locals() and component_id_from_request:
             job.component_statuses[component_id_from_request] = "error"
             job.error_message = (job.error_message + f"\nError generating '{component_plan_details.get('name_hint', component_id_from_request)}': {error_msg}") if job.error_message else f"Error generating '{component_plan_details.get('name_hint', component_id_from_request)}': {error_msg}"
             job.status = 'FAILED_COMPONENT' # Mark that at least one component failed.
             job.save()
        return JsonResponse({'error': error_msg, 'job_id': job_id if 'job_id' in locals() else None, 'component_id': component_id_from_request if 'component_id_from_request' in locals() else None}, status=500)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        logger.error(f"Unexpected component generation failure for Job ID {job_id if 'job_id' in locals() else 'N/A'}, Component ID {component_id_from_request if 'component_id_from_request' in locals() else 'N/A'}: {error_msg}", exc_info=True)
        if 'job' in locals() and job and 'component_id_from_request' in locals() and component_id_from_request:
             job.component_statuses[component_id_from_request] = "error"
             job.error_message = (job.error_message + f"\nUnexpected error for '{component_plan_details.get('name_hint', component_id_from_request)}': {error_msg}") if job.error_message else f"Unexpected error for '{component_plan_details.get('name_hint', component_id_from_request)}': {error_msg}"
             job.status = 'FAILED_COMPONENT'
             job.save()
        return JsonResponse({'error': error_msg, 'job_id': job_id if 'job_id' in locals() else None, 'component_id': component_id_from_request if 'component_id_from_request' in locals() else None}, status=500)

@require_POST # Or GET, depending on how client triggers it. POST is fine.
@csrf_exempt # For production, ensure your JS sends the CSRF token with AJAX.
def compile_mod_file_view(request, job_id):
    """
    API Endpoint: Phase 3 - Compile all generated snippets into a single .dm file string.
    This is called by the client's JavaScript after all components have been attempted.
    It assembles the mod header, monster blocks, and the nation block with recruitment lists.
    """
    job = get_object_or_404(ModGenerationJob, id=job_id)
    logger.info(f"Compile request received for Job ID {job.id}. Current status: {job.status}")

    # Allow compilation even if some components failed, so user can get partial results.
    if job.status not in ['COMPONENTS_GENERATED', 'GENERATING_COMPONENTS', 'FAILED_COMPONENT']: # GENERATING_COMPONENTS if user forces compile early
        logger.warning(f"Job {job.id} not in a suitable state for compilation. Status: {job.status}")
        return JsonResponse({'error': f'Job not ready for compilation. Current status: {job.status}'}, status=400)

    try:
        original_job_status_before_compile = job.status
        job.status = 'COMPILING' # Update status to show work in progress.
        job.save(update_fields=['status'])

        nation_name_sanitized = "".join(c if c.isalnum() else "_" for c in job.nation.name)
        mod_name = f"{nation_name_sanitized}ModByAI" # Make it clear it's AI generated
        
        nation_meta_plan = job.plan_details.get("nation_meta", {})
        mod_description_from_plan = nation_meta_plan.get("summary_suggestion", f"AI-generated mod for the nation of {job.nation.name}, based on the description: {job.nation.description}")

        # Start building the .dm file content.
        compiled_lines = [
            f'#modname "{mod_name}"',
            f'#description "{mod_description_from_plan}"',
            '#version "1.0.0"',
            '#domversion "6.28" -- Dominions 6 Target Version', # Specify target game version
            f'#icon "{nation_name_sanitized.upper()}_ICON.TGA" -- Placeholder icon (user needs to create this)\n',
            '-- Generated by Dom6ModGen AI Assistant --\n',
        ]

        # Systematically assign IDs. These are starting points.
        # For a real application, you might want these to be configurable or from a central sequence manager
        # to avoid clashes if multiple mods are used.
        current_monster_id_counter = 5000 
        current_nation_id_value = 150 # Default starting ID for mod nations

        # --- Assemble Monster Blocks (Commanders, Mages, Priests, Troops) ---
        monster_dm_snippets = []
        # Store names of generated monsters for the nation's recruitment list.
        recruitable_units_actual_names = []
        recruitable_commanders_actual_names = []

        # Define the order for processing monster types, which can be important for .dm file structure or preference.
        monster_component_types_in_order = ["commanders", "mages", "priests", "troops"]
        
        for comp_type_key in monster_component_types_in_order:
            if comp_type_key in job.plan_details and isinstance(job.plan_details[comp_type_key], list):
                for component_definition_in_plan in job.plan_details[comp_type_key]:
                    if not isinstance(component_definition_in_plan, dict): continue # Skip malformed plan items

                    component_id_from_plan = component_definition_in_plan.get("id")
                    component_name_hint = component_definition_in_plan.get("name_hint", component_id_from_plan)
                    
                    snippet_text = job.generated_snippets.get(component_id_from_plan)
                    
                    if snippet_text and job.component_statuses.get(component_id_from_plan) == "done":
                        # Replace the placeholder ID with an actual, incremented ID.
                        processed_snippet = snippet_text.replace("TEMP_ID_PLACEHOLDER", str(current_monster_id_counter))
                        monster_dm_snippets.append(f"\n-- Component: {comp_type_key.capitalize()} - {component_name_hint} (Generated ID: {current_monster_id_counter}) --")
                        monster_dm_snippets.append(processed_snippet)
                        
                        # Attempt to extract the actual #name from the snippet for the recruitment list.
                        unit_actual_name_in_snippet = None
                        for line in processed_snippet.splitlines():
                            if line.strip().startswith("#name"):
                                try:
                                    # Extracts content between the first pair of double quotes.
                                    unit_actual_name_in_snippet = line.split('"', 1)[1].rsplit('"', 1)[0]
                                    break
                                except IndexError:
                                    logger.warning(f"Could not parse #name from snippet for {component_id_from_plan}, Job {job.id}")
                        
                        if unit_actual_name_in_snippet:
                            if comp_type_key == "commanders" or comp_type_key == "mages" or comp_type_key == "priests": # Mages/Priests are usually commanders
                                recruitable_commanders_actual_names.append(unit_actual_name_in_snippet)
                            elif comp_type_key == "troops":
                                recruitable_units_actual_names.append(unit_actual_name_in_snippet)
                        else:
                            logger.warning(f"No #name found in snippet for {component_id_from_plan} (Job {job.id}), cannot add to recruitment list by name.")

                        current_monster_id_counter += 1 # Increment for the next monster.
                    else:
                         monster_dm_snippets.append(f"\n-- SKIPPED Monster Component (Not Generated or Error): {comp_type_key.capitalize()} - {component_name_hint} --")

        if monster_dm_snippets:
            compiled_lines.append('-- =============================================================================')
            compiled_lines.append('-- MONSTER DEFINITIONS (Units & Commanders)')
            compiled_lines.append(f'-- Assigned ID Range: 5000 - {current_monster_id_counter -1}') # Show the range used
            compiled_lines.append('-- =============================================================================')
            compiled_lines.extend(monster_dm_snippets)
            compiled_lines.append('\n-- == END MONSTERS == --\n')

        # --- Assemble Nation Block ---
        nation_block_id_in_plan = job.plan_details.get("nation_meta", {}).get("id")
        nation_block_snippet_text = job.generated_snippets.get(nation_block_id_in_plan)

        if nation_block_snippet_text and job.component_statuses.get(nation_block_id_in_plan) == "done":
            # Replace placeholder nation ID.
            processed_nation_block = nation_block_snippet_text.replace("TEMP_NATION_ID_PLACEHOLDER", str(current_nation_id_value))
            
            # Inject recruitment commands (#addrecunit, #addreccom) and starting army before the nation's #end tag.
            nation_block_lines = processed_nation_block.splitlines()
            final_nation_block_lines = []
            end_tag_found_and_processed = False

            for line in nation_block_lines:
                if line.strip().lower() == "#end" and not end_tag_found_and_processed:
                    # This is where we inject recruitment before the final #end of the nation block.
                    final_nation_block_lines.append("\n-- Recruitment and Starting Army --")
                    final_nation_block_lines.append("#clearrec -- Ensures only mod units are available by default")
                    for unit_name in recruitable_units_actual_names:
                        final_nation_block_lines.append(f'#addrecunit "{unit_name}"')
                    for com_name in recruitable_commanders_actual_names:
                        final_nation_block_lines.append(f'#addreccom "{com_name}"')
                    
                    # Add a basic starting army (can be made more intelligent based on plan/concepts).
                    if recruitable_commanders_actual_names:
                        final_nation_block_lines.append(f'#startcom "{recruitable_commanders_actual_names[0]}"')
                    if recruitable_units_actual_names:
                        # Add a couple of different starting units if available
                        final_nation_block_lines.append(f'#startunit "{recruitable_units_actual_names[0]}" 15') 
                        if len(recruitable_units_actual_names) > 1:
                             final_nation_block_lines.append(f'#startunit "{recruitable_units_actual_names[1]}" 10')
                    
                    final_nation_block_lines.append(line) # Add the original #end tag
                    end_tag_found_and_processed = True
                else:
                    final_nation_block_lines.append(line)
            
            # If #end was somehow not found, append recruitment and a new #end.
            if not end_tag_found_and_processed:
                logger.warning(f"No #end tag found in nation block for Job {job.id}. Appending recruitment and #end.")
                # (Same recruitment logic as above)
                final_nation_block_lines.append("\n-- Recruitment and Starting Army (appended due to missing #end) --")
                final_nation_block_lines.append("#clearrec")
                for unit_name in recruitable_units_actual_names: final_nation_block_lines.append(f'#addrecunit "{unit_name}"')
                for com_name in recruitable_commanders_actual_names: final_nation_block_lines.append(f'#addreccom "{com_name}"')
                if recruitable_commanders_actual_names: final_nation_block_lines.append(f'#startcom "{recruitable_commanders_actual_names[0]}"')
                if recruitable_units_actual_names: final_nation_block_lines.append(f'#startunit "{recruitable_units_actual_names[0]}" 15')
                final_nation_block_lines.append("#end")


            compiled_lines.append('-- =============================================================================')
            compiled_lines.append(f'-- NATION DEFINITION (Generated ID: {current_nation_id_value})')
            compiled_lines.append('-- =============================================================================')
            compiled_lines.append("\n".join(final_nation_block_lines))
            compiled_lines.append('\n-- == END NATION DEFINITION == --\n')
        else:
            compiled_lines.append('-- ERROR: Nation Block ("nation_meta") was not generated or had an error. Cannot complete mod. --')

        # (Future: Add sections for custom weapons, armors, spells if they were part of the plan and generated)

        final_dm_content_str = "\n".join(compiled_lines)
        job.final_mod_content = final_dm_content_str
        
        # Determine final status based on component generation success.
        if any(status == "error" for status in job.component_statuses.values()) or \
           original_job_status_before_compile == 'FAILED_COMPONENT':
            job.status = 'COMPLETED_WITH_ERRORS'
            if not job.error_message or "Compilation completed" not in job.error_message : # Avoid duplicate messages
                 job.error_message = (job.error_message or "") + "\nCompilation completed, but some components may be missing or faulty. Please review the output."
        else:
            job.status = 'COMPLETED'
        job.save()

        logger.info(f"Mod file compiled for Job ID {job.id}. Final status: {job.status}.")
        return JsonResponse({
            'message': f'Mod file compiled! Status: {job.get_status_display()}', 
            'job_id': job.id, 
            'status': job.status, # Send back the final status
            'dm_content_preview': final_dm_content_str[:1500] # Send a preview of the compiled content.
        })
        
    except Exception as e:
        job.status = 'FAILED_COMPILATION'
        error_msg = f"An unexpected error occurred during mod file compilation: {e}"
        job.error_message = (job.error_message + "\n" + error_msg) if job.error_message else error_msg
        job.save()
        logger.error(f"Mod compilation failed critically for Job ID {job.id}: {e}", exc_info=True)
        return JsonResponse({'error': error_msg, 'job_id': job.id}, status=500)

@require_GET 
def download_mod_file_view(request, job_id):
    """
    Serves the compiled .dm file for download.
    This is called by the client after successful compilation.
    """
    job = get_object_or_404(ModGenerationJob, id=job_id)
    
    # Only allow download if compilation was completed (even with errors) and content exists.
    if job.status not in ['COMPLETED', 'COMPLETED_WITH_ERRORS'] or not job.final_mod_content:
        logger.warning(f"Download attempt for Job ID {job.id}, but it's not completed or has no content. Status: {job.status}")
        raise Http404("Mod file content is not available or the job did not complete compilation successfully.")

    nation_name_sanitized = "".join(c if c.isalnum() else "_" for c in job.nation.name)
    filename = f"{nation_name_sanitized}_job{job.id}.dm" # Unique filename for the download.
    
    # Dominions .dm files are typically plain text. UTF-8 is a safe bet for web and modern systems.
    # If Dominions requires a specific encoding (like ANSI/Windows-1252), adjust 'charset' accordingly.
    response = HttpResponse(job.final_mod_content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"' # Prompts browser to download.
    logger.info(f"Serving .dm file for download: Job ID {job.id}, Filename {filename}")
    return response

# Your original nation_generate_dm view (the one that times out) can be kept for reference,
# or removed if this new interactive approach replaces it entirely.
# def nation_generate_dm(request, pk): ...
