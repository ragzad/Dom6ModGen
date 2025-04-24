# nations/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Nation
from .forms import NationForm
import google.generativeai as genai
from decouple import config
import os

try:
    GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        print("Gemini API Key configured.")
    else:
        print("WARN: GEMINI_API_KEY not found in environment. AI generation may fail.")
except NameError:
    print("WARN: google-generativeai library not found. Install it to use AI features.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")


def nation_list(request):
    nations = Nation.objects.all().order_by('name')
    context = {
        'nations': nations,
    }
    return render(request, 'nations/nation_list.html', context)


def nation_detail(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    context = {
        'nation': nation,
    }
    return render(request, 'nations/nation_detail.html', context)


def nation_create(request):
    if request.method == 'POST':
        form = NationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nations:nation_list')
    else:
        form = NationForm()

    context = {
        'form': form,
    }
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

    context = {
        'form': form,
        'nation': nation,
    }
    return render(request, 'nations/nation_form.html', context)


def nation_delete(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    if request.method == 'POST':
        nation.delete()
        return redirect('nations:nation_list')

    context = {
        'nation': nation,
    }
    return render(request, 'nations/nation_confirm_delete.html', context)


def nation_generate_dm(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    generated_code = "# Generation has not run yet or failed."
    error_message = None
    prompt_used = ""

    try:
        loaded_api_key = config('GEMINI_API_KEY', default=None)
        if not loaded_api_key:
            raise ValueError("Gemini API Key not found in environment variables during view execution.")

        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""You are an expert Dominions 6 modder creating a new nation mod file (.dm format).
Your task is to generate ONLY the core nation definition block AND definitions for 3 basic starting units (1 Commander, 1 Infantry, 1 Ranged/Other).

PART 1: NATION DEFINITION
Generate the core nation definition block, starting exactly with '#newnation' and ending exactly with '#end'.
Do not include '#selectnation', '#modname', '#description', or anything before '#newnation'. Do not include any comments or explanations outside the required mod commands.
Base the generated commands on the provided Nation Name and Description. Be creative but consistent with Dominions themes.

Nation Name: {nation.name}
Nation Description: {nation.description}

Generate the following nation commands specifically, inferring reasonable values or placeholders:
- #name "{nation.name}"
- #epithet "..." (Suggest a suitable epithet)
- #era <number> (Assume 2 for Middle Era - MA - unless description strongly implies Early Era=1 or Late Era=3)
- #descr "{nation.description}"
- #summary "..." (Write a brief 1-2 sentence summary)
- #brief "..." (Write a very short, evocative phrase)
- #flag "PLACEHOLDER/{nation.name}_flag.tga"
- #color <r> <g> <b> (Suggest thematic RGB values 0.0-1.0)
- #secondarycolor <r> <g> <b> (Suggest thematic RGB values 0.0-1.0)
- #idealcold <number> (Suggest 0, or -1/1)
- #startsite "..." (Suggest one simple, thematic starting site name)
- #startcom "{nation.name} Commander" (Use this generic name)
- #startunittype1 "{nation.name} Infantry" (Use this generic name)
- #startunittype2 "{nation.name} Skirmisher" (Use this generic name)
- #dominionstr <number> (Suggest 4 or 5)
- #castleprod <number> (Suggest 0 or 1)
(Include other common nation flags like #forestrec ONLY if strongly implied by the description)
Ensure this block ends precisely with '#end'.

PART 2: BASIC UNIT DEFINITIONS
Immediately after the nation's '#end' command, generate three separate '#newmonster' blocks for the starting units mentioned above: '{nation.name} Commander', '{nation.name} Infantry', '{nation.name} Skirmisher'.
For each '#newmonster' block:
- Start it with '#newmonster'.
- Include '#name "<Unit Name>"'.
- Include '#descr "..."' (Suggest a brief description based on the unit name and nation description).
- Include basic combat stats (#hp, #str, #att, #def, #prec, #mor, #mr - suggest plausible low-to-mid values for basic units/commander).
- Include basic movement stats (#move, #ap - suggest standard values).
- Include basic costs (#recruitcost, #resourcecost, #upkeep - suggest plausible low costs).
- Suggest a basic #weapon (use name like 'Spear' or 'Short Sword' or 'Bow').
- Suggest basic #armor (use name like 'Leather Armor' or 'Shield').
- Add '#commander' for the commander unit, '#infantry' for the infantry, '#archer' or '#humanoid' for the skirmisher.
- Add '#startunit' for all three.
- End each block with '#end'.

Output ONLY the raw .dm commands for both PART 1 and PART 2, with no extra text, comments, or formatting.
"""
        prompt_used = prompt # Store the prompt


        print("Attempting to call Gemini API...")
        response = model.generate_content(prompt)
        print("Gemini API call completed.")

        try:
            generated_code = response.text
            if not generated_code.strip():
                 generated_code = "# Error: AI response was empty."
                 print("WARN: AI response was empty.")
        except ValueError:
             generated_code = f"# Error: AI response blocked or invalid."
             error_message = f"AI Response Feedback: {response.prompt_feedback}"
             print(f"WARN: AI response blocked or invalid. Feedback: {response.prompt_feedback}")
        except Exception as resp_err:
             generated_code = f"# Error: Could not parse AI response."
             error_message = f"Error processing AI response: {resp_err}"
             print(f"ERROR: Processing AI response: {resp_err}")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        error_message = str(ve)
        generated_code = f"Error: Configuration problem."
    except NameError as ne:
         print(f"NameError: {ne}. Is google-generativeai installed?")
         error_message = "AI generation library (google-generativeai) not available or not imported correctly."
         generated_code = "Error: AI library not installed."
    except Exception as e:
        print(f"Error during AI generation structure: {e}")
        error_message = f"An error occurred while preparing/making the AI request: {e}"
        generated_code = f"Error: Could not generate code due to application error."

    context = {
        'nation': nation,
        'generated_code': generated_code,
        'error_message': error_message,
        'prompt_used': prompt_used,
    }
    return render(request, 'nations/nation_generate_dm.html', context)