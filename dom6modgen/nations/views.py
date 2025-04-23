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

        prompt = f"""You are an expert Dominions 6 modder. Generate the Dominions 6 modding commands (.dm file format) for a new nation based ONLY on the following information. Output ONLY the raw .dm commands starting with #newnation and ending with #end. Do not include explanations or markdown formatting. Be creative but stay consistent with Dominions themes.

        Nation Name: {nation.name}
        Nation Description: {nation.description}

        Generate the necessary commands like #name, #descr, #epithet, #era (assume Middle Era - MA - unless description strongly implies otherwise), #summary, #flag (placeholder path), #startunit/s (suggest one basic national infantry and one national commander), #homerealm (suggest one), #startsite (suggest one basic site), #idealcold (suggest 0, 1, -1), #castleprod (suggest 0 or 1), #dominionstr (suggest 4 or 5) etc., based on the name and description provided."""
        prompt_used = prompt

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