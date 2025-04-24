# nations/views.py
# --- Keep standard imports ---
from django.shortcuts import render, get_object_or_404, redirect
from .models import Nation
from .forms import NationForm
# --- Keep Gemini imports ---
import google.generativeai as genai
from decouple import config
import os

# --- Keep Gemini API Key Configuration ---
try:
    GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        print("Gemini API Key configured.")
    else:
        print("WARN: GEMINI_API_KEY not found...")
except NameError:
    print("WARN: google-generativeai library not found...")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

# --- Keep CRUD Views (nation_list, nation_detail, etc.) ---
# ... (paste your existing list, detail, create, update, delete views here) ...

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


# --- Simplified AI Generation View (NO RAG) ---
def nation_generate_dm(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    generated_code = "# Generation failed or prerequisites missing."
    error_message = None
    prompt_used = ""
    # No 'retrieved_context' needed here

    try:
        # Check for API Key
        loaded_api_key = config('GEMINI_API_KEY', default=None)
        if not loaded_api_key:
            raise ValueError("Gemini API Key not found in environment variables.")

        # Select the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Construct the prompt WITHOUT RAG context placeholder
        prompt = f"""You are an expert Dominions 6 modder creating a new nation mod file (.dm format).
Your task is to generate ONLY the core nation definition block AND definitions for 3 basic starting units (1 Commander, 1 Infantry, 1 Ranged/Other). Start the nation block exactly with '#newnation' and end it exactly with '#end'. Start each unit block exactly with '#newmonster' and end it exactly with '#end'. Do not include explanations or markdown formatting outside the required commands. Use reasonable defaults based on the Nation Name and Description.

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
    except ValueError as ve: # Catch missing key error
        print(f"Configuration Error: {ve}")
        error_message = str(ve)
        generated_code = f"Error: Configuration problem ({ve})."
    except NameError as ne: # Catch if 'genai' not defined (library install issue)
         print(f"NameError: {ne}. Is google-generativeai installed?")
         error_message = "AI generation library not available."
         generated_code = "Error: AI library missing."
    except Exception as e: # Catch other errors (API call, etc.)
        print(f"Error during generation view: {e}")
        error_message = f"An error occurred: {e}"
        generated_code = f"Error: Could not generate code ({e})."

    context = {
        'nation': nation,
        'generated_code': generated_code,
        'error_message': error_message,
        'prompt_used': prompt_used,
        # No 'retrieved_context' passed to template
    }
    # Render the *same* results template, it will just show no retrieved context
    return render(request, 'nations/nation_generate_dm.html', context)
