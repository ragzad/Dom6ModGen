from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Nation
from .forms import NationForm
from gamedata.models import GameEntity
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


# --- New Segmented Generation Logic with Full Command Reference ---

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
        'prompt_template': """Based on the 'National Features' section of the Design Document, generate the initial Dominions 6 mod commands. Use commands from the reference list that apply at a national level (e.g., #era, #epithet, #idealcold, #fortcost, #def, #researchbonus).

--- MOD COMMAND REFERENCE START ---
{mod_commands_list}
--- MOD COMMAND REFERENCE END ---

**Design Document:**
{expanded_description}""",
        'next_status': 'commanders',
        'output_field': 'generated_mod_code',
    },
    'commanders': {
        'action_name': 'Generate Commanders',
        'prompt_template': """You are an expert Dominions 6 modder. Generate the mod commands for the COMMANDERS described in the Design Document.

**CRITICAL INSTRUCTIONS:**
1.  Generate a `#newmonster` block for EACH commander, ending it with `#end`.
2.  Use commands **only** from the provided Mod Command Reference list. This is your complete toolbox.
3.  Use numeric IDs from the provided Weapon/Armor Reference Data.

--- MOD COMMAND REFERENCE START ---
{mod_commands_list}
--- MOD COMMAND REFERENCE END ---

--- WEAPON/ARMOR REFERENCE DATA START ---
**Valid Vanilla Weapons:**
{weapon_list}
**Valid Vanilla Armors:**
{armor_list}
--- WEAPON/ARMOR REFERENCE DATA END ---

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
        'prompt_template': """You are an expert Dominions 6 modder. Generate the mod commands for the standard TROOPS described in the Design Document.

**CRITICAL INSTRUCTIONS:**
1.  Generate a `#newmonster` block for EACH troop, ending it with `#end`.
2.  Use commands **only** from the provided Mod Command Reference list. This is your complete toolbox.
3.  Use numeric IDs from the provided Weapon/Armor Reference Data.
4.  If a new item is required, use the `#newweapon` or `#newarmor` command with an ID > 8000 BEFORE defining the unit that uses it.

--- MOD COMMAND REFERENCE START ---
{mod_commands_list}
--- MOD COMMAND REFERENCE END ---

--- WEAPON/ARMOR REFERENCE DATA START ---
**Valid Vanilla Weapons:**
{weapon_list}
**Valid Vanilla Armors:**
{armor_list}
--- WEAPON/ARMOR REFERENCE DATA END ---

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
        'prompt_template': """Based on the 'Unique Heroes' section of the Design Document, generate the Dominions 6 mod commands for the HEROES.

**CRITICAL INSTRUCTIONS:**
1. Generate a `#newmonster` block for EACH hero, ending it with `#end`.
2. Remember to include the `#hero` and `#unique` commands from the reference list.
3. Use commands **only** from the provided Mod Command Reference list.
4. Use numeric IDs from the provided Weapon/Armor Reference Data.

--- MOD COMMAND REFERENCE START ---
{mod_commands_list}
--- MOD COMMAND REFERENCE END ---

--- WEAPON/ARMOR REFERENCE DATA START ---
**Valid Vanilla Weapons:**
{weapon_list}
**Valid Vanilla Armors:**
{armor_list}
--- WEAPON/ARMOR REFERENCE DATA END ---

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
        'prompt_template': """Based on the 'Unique Spells/Items' section of the Design Document, generate the Dominions 6 mod commands for any unique national spells. Use the #newspell command and follow the correct syntax. If no spells were described, output only the comment '-- No new spells required by design document.'.

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
        'prompt_template': """Based on the 'Unique Spells/Items' section and any placeholder equipment mentioned for troops/commanders in the Design Document, generate the Dominions 6 mod commands for any NEW WEAPONS or ARMOR. Use #newweapon and #newarmor with IDs above 8000. Follow the syntax exactly. If no new gear is needed, output only the comment '-- No new items required by design document.'.

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
        'prompt_template': """You are a meticulous Dominions 6 mod syntax validator. Your task is to analyze the following completed mod file and identify any technical errors that would cause it to fail loading in the game. You must be strict and follow the modding manual precisely.

**Validation Checklist:**
1.  **Block Integrity:** Does every `#newmonster`, `#newweapon`, `#newarmor`, and `#newspell` block have a corresponding `#end` command?
2.  **Command Spelling:** Are all commands (e.g., `#name`, `#hp`, `#magicskill`) spelled correctly? Check for common mistakes like `#strength` instead of `#str`.
3.  **Argument Validity:** Does each command have the correct number and type of arguments? For example, `#hp` takes one number, `#weapon` takes one number, `#magicskill` takes a path letter and a number.
4.  **String Formatting:** Are all string arguments, like in `#name` and `#descr`, enclosed in double quotes?

Please review the following mod code against this checklist:
```dominions
{generated_mod_code}
```

Provide your feedback as a concise, bulleted list of specific errors found (e.g., "ERROR: Missing #end for monster 'Clan Chieftain'", "ERROR: The `#strength` command should be `#str`"). If no errors are found, respond with ONLY the phrase: 'Syntax validation passed. The mod appears to be structured correctly and is ready for in-game testing.'""",
        'next_status': 'completed',
        'output_field': 'generated_mod_code',
    },
}

def run_generation_step_view(request, pk):
    nation = get_object_or_404(Nation, pk=pk)
    current_status = nation.generation_status

    if request.method == 'POST' and current_status in GENERATION_WORKFLOW:
        step_config = GENERATION_WORKFLOW[current_status]

        # Fetch and format all reference data from the database
        weapon_data = "\\n".join(
            list(GameEntity.objects.filter(entity_type='weapons').values_list('reference_text', flat=True))
        )
        armor_data = "\\n".join(
            list(GameEntity.objects.filter(entity_type='armors').values_list('reference_text', flat=True))
        )
        # --- NEW ---
        # Get the full list of all possible mod commands to use as a reference.
        mod_commands_data = "\\n".join(
            [f"#{cmd}" for cmd in GameEntity.objects.filter(entity_type='attribute_keys').values_list('name', flat=True)]
        )
        # -----------
        
        prompt_context = {
            "nation_description": nation.description,
            "expanded_description": nation.expanded_description,
            "generated_mod_code": nation.generated_mod_code or "",
            "weapon_list": weapon_data,
            "armor_list": armor_data,
            "mod_commands_list": mod_commands_data, # Add the new list to the context
        }
        prompt = step_config['prompt_template'].format(**prompt_context)
        
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables.")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            output_field = step_config['output_field']
            
            if output_field == 'generated_mod_code':
                header = f"\\n\\n--//-- STEP: {current_status.upper()} --//--"
                new_content = f"{header}\\n{response.text.strip()}"
                
                if nation.generated_mod_code is None or current_status == 'nation_details':
                    nation.generated_mod_code = new_content
                else:
                    nation.generated_mod_code += new_content
            else:
                setattr(nation, output_field, response.text)

            nation.generation_status = step_config['next_status']
            nation.save()

        except Exception as e:
            nation.generation_status = 'failed'
            print(f"Error during generation step '{current_status}': {e}")
            nation.save()

    return redirect('nations:nation_workshop', pk=nation.pk)
