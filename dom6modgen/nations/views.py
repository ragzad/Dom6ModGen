# dom6modgen/nations/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Nation, GENERATION_STATUS_CHOICES
from .forms import NationForm
import google.generativeai as genai
import os

# --- Class-Based Views (Unchanged) ---
class NationListView(ListView):
    model = Nation
    template_name = 'nations/nation_list.html'
    context_object_name = 'nations'

class NationDetailView(DetailView):
    model = Nation
    template_name = 'nations/nation_detail.html'
    context_object_name = 'nation'

class NationCreateView(CreateView):
    model = Nation
    form_class = NationForm
    template_name = 'nations/nation_form.html'
    success_url = reverse_lazy('nations:nation_list')

class NationUpdateView(UpdateView):
    model = Nation
    form_class = NationForm
    template_name = 'nations/nation_form.html'
    def get_success_url(self):
        return reverse('nations:nation_detail', kwargs={'pk': self.object.pk})

class NationDeleteView(DeleteView):
    model = Nation
    template_name = 'nations/nation_confirm_delete.html'
    success_url = reverse_lazy('nations:nation_list')


# --- New Segmented Generation Logic ---

# This dictionary defines the full, expanded workflow for AI generation,
# informed by the structure of the Dominions 6 Modding Manual.
GENERATION_WORKFLOW = {
    'not_started': {
        'action_name': 'Expand Idea into a Full Concept',
        'prompt_template': """You are a creative assistant and expert for the strategy game Dominions 6. A user has provided a basic idea for a new nation. Your first task is to expand this idea into a detailed Design Document. This document will serve as the master plan for all subsequent mod generation steps. It should be comprehensive, thematic, and provide enough detail for a complete and functional mod. Do NOT generate any mod code (#newnation, etc.) yet, only the descriptive plan.

Based on the user's idea of: '{nation_description}'

Please expand this into a structured Design Document covering the following sections:
1.  **High Concept:** A one-paragraph summary of the nation's core identity, playstyle, and flavor.
2.  **Lore & Backstory:** The nation's history, culture, and primary motivations.
3.  **National Features:**
    * **Military:** Strengths (e.g., heavy infantry, sacred cavalry, skilled archers) and weaknesses (e.g., poor crossbows, no cavalry).
    * **Magic:** Primary magic paths (e.g., Fire, Earth), secondary paths, and weaknesses. Mention any affinities for specific schools of magic.
    * **Dominion & Scales:** Describe their ideal scales (e.g., Order 3, Production 1, Heat 2, etc.) and any special Dominion effects.
    * **Recruitment:** Mention any special recruitment rules (e.g., can only recruit mages in capital, gets special units in forests).
4.  **Unit Roster (Commanders):** Describe 3-5 thematic commanders. Include their role (e.g., mage, scout, basic leader, heavy leader), a physical description, and key abilities (e.g., "Adept Fire Mage with Fire 2", "Leads 80 troops").
5.  **Unit Roster (Troops):** Describe 5-7 thematic troops. Include their role (e.g., basic infantry, archer, elite sacred), a physical description, and their equipment.
6.  **Unique Heroes:** Describe 1-2 unique national heroes that could appear, including their backstory and special abilities.
7.  **Unique Spells/Items:** Propose 1-2 ideas for national spells or forgeable items that fit the nation's theme.

Present this as a clear, well-organized document. This is a creative planning step, not a code generation step.""",
        'next_status': 'nation_details',
        'output_field': 'expanded_description',
    },
    'nation_details': {
        'action_name': 'Generate Nation Details & Tags',
        'prompt_template': """Based *only* on the 'National Features' section of the following Design Document, generate the initial Dominions 6 mod commands for the nation. This includes only #newnation, #era, #epithet, #descr, #summary, and all relevant nation-level tags (e.g., #idealcold, #fortcost, #def, #researchbonus, #unresthalf, etc.). Do not generate any units, items, or spells yet.

**Design Document:**
{expanded_description}""",
        'next_status': 'commanders',
        'output_field': 'generated_mod_code',
    },
    'commanders': {
        'action_name': 'Generate Commanders',
        'prompt_template': """Based on the 'Unit Roster (Commanders)' section of the Design Document, generate the Dominions 6 mod commands for all COMMANDERS. Use the #newmonster command for each. Ensure you include relevant stats like leadership, magic paths, and special abilities mentioned in the document.

**Design Document:**
{expanded_description}

**Previously Generated Code:**
```dominions
{generated_mod_code}
```""",
        'next_status': 'troops',
        'output_field': 'generated_mod_code',
    },
    'troops': {
        'action_name': 'Generate Troops',
        'prompt_template': """Based on the 'Unit Roster (Troops)' section of the Design Document, generate the Dominions 6 mod commands for all standard TROOPS (non-commanders). Use the #newmonster command for each. Define their weapons and armor using existing game items or placeholder names for new ones (e.g., #weapon "My New Sword").

**Design Document:**
{expanded_description}

**Previously Generated Code:**
```dominions
{generated_mod_code}
```""",
        'next_status': 'heroes',
        'output_field': 'generated_mod_code',
    },
    'heroes': {
        'action_name': 'Generate National Heroes',
        'prompt_template': """Based on the 'Unique Heroes' section of the Design Document, generate the Dominions 6 mod commands for the nation's HEROES. Use the #newmonster command, and remember to include the #hero and #unique tags for each.

**Design Document:**
{expanded_description}

**Previously Generated Code:**
```dominions
{generated_mod_code}
```""",
        'next_status': 'spells',
        'output_field': 'generated_mod_code',
    },
    'spells': {
        'action_name': 'Generate National Spells',
        'prompt_template': """Based on the 'Unique Spells/Items' section of the Design Document, generate the Dominions 6 mod commands for any unique national RITUALS or COMBAT SPELLS. Use the #newspell command. If no spells were described, output only the comment '-- No new spells required by design document.'.

**Design Document:**
{expanded_description}

**Previously Generated Code:**
```dominions
{generated_mod_code}
```""",
        'next_status': 'items',
        'output_field': 'generated_mod_code',
    },
    'items': {
        'action_name': 'Generate Weapons & Armor',
        'prompt_template': """Based on the 'Unique Spells/Items' section and any placeholder equipment mentioned for troops/commanders in the Design Document, generate the Dominions 6 mod commands for any NEW WEAPONS or ARMOR. Use #newweapon and #newarmor. If no new gear is needed, output only the comment '-- No new items required by design document.'.

**Design Document:**
{expanded_description}

**Previously Generated Code:**
```dominions
{generated_mod_code}
```""",
        'next_status': 'validation',
        'output_field': 'generated_mod_code',
    },
    'validation': {
        'action_name': 'Validate Mod File Syntax',
        'prompt_template': """You are a Dominions 6 modding expert. Your task is to review the following completed mod file for syntax errors, logical inconsistencies, or missing commands that would prevent it from working in the game. Do NOT provide creative feedback. Only identify technical errors.

Your review should check for:
- Correct command names (e.g., #newmonster, #end).
- Correct number and type of arguments for each command.
- Mismatched IDs (e.g., defining a weapon with one ID but assigning a different ID to a unit).
- Missing #end tags.
- Any other common syntax errors according to the Dominions 6 modding manual.

Review the following mod code:
```dominions
{generated_mod_code}
```

Provide your feedback as a simple list of potential errors. If the file appears syntactically correct and ready for testing, respond with only the phrase: 'Syntax validation passed. The mod appears to be structured correctly and is ready for in-game testing.'""",
        'next_status': 'completed',
        'output_field': 'generated_mod_code', # Append the validation result to the code
    },
}

def nation_workshop_view(request, pk):
    """
    Displays the main workshop page for a nation, showing progress
    and the next available action.
    """
    nation = get_object_or_404(Nation, pk=pk)
    
    current_status = nation.generation_status
    next_action = None
    
    if current_status not in ['completed', 'failed']:
        next_action = GENERATION_WORKFLOW.get(current_status)

    context = {
        'nation': nation,
        'next_action': next_action,
        'is_completed': current_status == 'completed'
    }
    return render(request, 'nations/nation_workshop.html', context)


def run_generation_step_view(request, pk):
    """
    Executes the current generation step for a nation.
    """
    nation = get_object_or_404(Nation, pk=pk)
    current_status = nation.generation_status

    if request.method == 'POST' and current_status in GENERATION_WORKFLOW:
        step_config = GENERATION_WORKFLOW[current_status]
        
        prompt = step_config['prompt_template'].format(
            nation_description=nation.description,
            expanded_description=nation.expanded_description,
            generated_mod_code=nation.generated_mod_code or ""
        ).strip()
        
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables.")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            
            output_field = step_config['output_field']
            
            # For code-generation steps, append the new code.
            # For the first step and validation, overwrite or append as needed.
            if output_field == 'generated_mod_code':
                # Add comments to delineate steps clearly in the final file
                header = f"\n\n--//-- STEP: {current_status.upper()} --//--"
                new_content = f"{header}\n{response.text.strip()}"
                
                # If it's the very first code step, initialize the field. Otherwise, append.
                if nation.generated_mod_code is None or current_status == 'nation_details':
                    nation.generated_mod_code = new_content
                else:
                    nation.generated_mod_code += new_content
            else:
                # This handles the initial 'expanded_description' step
                setattr(nation, output_field, response.text)

            nation.generation_status = step_config['next_status']
            nation.save()

        except Exception as e:
            nation.generation_status = 'failed'
            print(f"Error during generation step '{current_status}': {e}")
            nation.save()

    return redirect('nations:nation_workshop', pk=nation.pk)

