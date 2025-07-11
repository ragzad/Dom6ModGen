# dom6modgen/nations/views.py

import os
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Nation
from .forms import NationForm
from gamedata.models import GameEntity, ModExample
import google.generativeai as genai

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


# --- Generation Logic & Workflow ---

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
5.  **Unit Roster (Troops): Privilege 5-7 thematic troops. Include their role (e.g., basic infantry, archer, elite sacred), a physical description, and their equipment.
6.  **Unique Heroes:** Describe 1-2 unique national heroes that could appear, including their backstory and special abilities.
7.  **Unique Spells/Items:** Propose 1-2 ideas for national spells or forgeable items that fit the nation's theme.

Present this as a clear, well-organized document. This is a creative planning step, not a code generation step.""",
        'next_status': 'nation_details',
        'output_field': 'expanded_description',
    },
    'nation_details': {
        'action_name': 'Generate Nation Details & Tags',
        'prompt_template': """You are an expert Dominions 6 modder. Based *only* on the 'National Features' section of the Design Document, generate the initial Dominions 6 mod commands.

**CRITICAL INSTRUCTIONS:**
1.  Your output MUST EXACTLY follow the syntax of a real Dominions 6 mod file.
2.  Every `#selectnation` block MUST be closed with `#end`.
3.  Do NOT include comments within command arguments (e.g., `#copyweapon 108` is correct, NOT `#copyweapon 108 -- comment`).
4.  Only use commands relevant to nation definition. Do NOT include commands for units, spells, items, or obscure internal attributes like #costmult, #domsize, #base, etc.

--- MOD COMMAND REFERENCE START ---
{mod_commands_list}
--- MOD COMMAND REFERENCE END ---

--- FULL MOD EXAMPLE START ---
{mod_example}
--- FULL MOD EXAMPLE END ---

**Design Document:**
{expanded_description}

Generate ONLY the mod commands for the nation details. Do NOT generate any units, spells, or items in this step.""",
        'next_status': 'commanders',
        'output_field': 'generated_mod_code',
    },
    'commanders': {
        'action_name': 'Generate Commanders',
        'prompt_template': """You are an expert Dominions 6 modder. Generate the mod commands for the COMMANDERS described in the Design Document.

**CRITICAL INSTRUCTIONS:**
1.  Generate a `#newmonster` block for EACH commander, and EACH block MUST be closed with `#end`.
2.  Your output MUST EXACTLY follow the syntax of a real Dominions 6 mod file. Study the Full Mod Example provided.
3.  Use commands **only** from the provided Mod Command Reference list.
4.  Use numeric IDs from the provided Weapon/Armor Reference Data.
5.  Do NOT include comments within command arguments (e.g., `#copyweapon 108` is correct, NOT `#copyweapon 108 -- comment`).
6.  For `#resist` commands, remember it takes THREE arguments: `#resist <value> <resist_type_id> <path_id>` (e.g., `#resist 100 5 100` for disease resistance).
7.  For `#spell` commands on units, ensure the spell name is in quotes.
8.  Do NOT regenerate any previously generated mod code. Generate ONLY the new commander blocks.

--- MOD COMMAND REFERENCE START ---
{mod_commands_list}
--- MOD COMMAND REFERENCE END ---

--- WEAPON/ARMOR REFERENCE DATA START ---
**Valid Vanilla Weapons (Sample):**
{weapon_list}
**Valid Vanilla Armors (Sample):**
{armor_list}
--- WEAPON/ARMOR REFERENCE DATA END ---

--- FULL MOD EXAMPLE START ---
{mod_example}
--- FULL MOD EXAMPLE END ---

**Design Document (relevant sections for Commanders):**
{expanded_description}""",
        'next_status': 'troops',
        'output_field': 'generated_mod_code',
    },
    'troops': {
        'action_name': 'Generate Troops',
        'prompt_template': """You are an expert Dominions 6 modder. Generate the mod commands for the standard TROOPS described in the Design Document.

**CRITICAL INSTRUCTIONS:**
1.  Generate a `#newmonster` block for EACH troop, and EACH block MUST be closed with `#end`.
2.  Your output MUST EXACTLY follow the syntax of a real Dominions 6 mod file. Study the Full Mod Example provided.
3.  Use commands **only** from the provided Mod Command Reference list.
4.  Use numeric IDs from the provided Weapon/Armor Reference Data.
5.  Do NOT include comments within command arguments (e.g., `#copyweapon 108` is correct, NOT `#copyweapon 108 -- comment`).
6.  If a new item is required for a unit, use the `#newweapon` or `#newarmor` command with an ID > 8000 BEFORE defining the unit that uses it in the *same output block*. Ensure these new item blocks are also closed with `#end`.
7.  For `#resist` commands, remember it takes THREE arguments: `#resist <value> <resist_type_id> <path_id>` (e.g., `#resist 100 5 100` for disease resistance).
8.  Do NOT regenerate any previously generated mod code. Generate ONLY the new troop blocks.

--- MOD COMMAND REFERENCE START ---
{mod_commands_list}
--- MOD COMMAND REFERENCE END ---

--- WEAPON/ARMOR REFERENCE DATA START ---
**Valid Vanilla Weapons (Sample):**
{weapon_list}
**Valid Vanilla Armors (Sample):**
{armor_list}
--- WEAPON/ARMOR REFERENCE DATA END ---

--- FULL MOD EXAMPLE START ---
{mod_example}
--- FULL MOD EXAMPLE END ---

**Design Document (relevant sections for Troops):**
{expanded_description}""",
        'next_status': 'heroes',
        'output_field': 'generated_mod_code',
    },
    'heroes': {
        'action_name': 'Generate National Heroes',
        'prompt_template': """You are an expert Dominions 6 modder. Based on the 'Unique Heroes' section of the Design Document, generate the Dominions 6 mod commands for the HEROES.

**CRITICAL INSTRUCTIONS:**
1.  Generate a `#newmonster` block for EACH hero, and EACH block MUST be closed with `#end`.
2.  Remember to include the `#hero` and `#unique` commands.
3.  Your output MUST EXACTLY follow the syntax of a real Dominions 6 mod file. Study the Full Mod Example provided.
4.  Use commands **only** from the provided Mod Command Reference list.
5.  Use numeric IDs from the provided Weapon/Armor Reference Data.
6.  Do NOT include comments within command arguments (e.g., `#copyweapon 108` is correct, NOT `#copyweapon 108 -- comment`).
7.  For `#resist` commands, remember it takes THREE arguments: `#resist <value> <resist_type_id> <path_id>` (e.g., `#resist 100 5 100` for disease resistance).
8.  Do NOT regenerate any previously generated mod code. Generate ONLY the new hero blocks.

--- MOD COMMAND REFERENCE START ---
{mod_commands_list}
--- MOD COMMAND REFERENCE END ---

--- WEAPON/ARMOR REFERENCE DATA START ---
**Valid Vanilla Weapons (Sample):**
{weapon_list}
**Valid Vanilla Armors (Sample):**
{armor_list}
--- WEAPON/ARMOR REFERENCE DATA END ---

--- FULL MOD EXAMPLE START ---
{mod_example}
--- FULL MOD EXAMPLE END ---

**Design Document (relevant sections for Heroes):**
{expanded_description}""",
        'next_status': 'spells',
        'output_field': 'generated_mod_code',
    },
    'spells': {
        'action_name': 'Generate National Spells',
        'prompt_template': """You are an expert Dominions 6 modder. Based on the 'Unique Spells/Items' section of the Design Document, generate the Dominions 6 mod commands for any unique national spells.

**CRITICAL INSTRUCTIONS:**
1.  Generate a `#newspell` block for EACH spell, and EACH block MUST be closed with `#end`.
2.  Your output MUST EXACTLY follow the syntax of a real Dominions 6 mod file. Study the Full Mod Example provided.
3.  To restrict a spell to a nation, use `#nations <nation_id>` or `#restrictednation`. Do NOT use `#restricted`.
4.  For `#effect` commands, use a valid effect ID (e.g., `10021` for summon unit) or provide the specific effect commands (e.g., `#damage <value>`, `#aoe <value>`). Do NOT use placeholder IDs like `10000`.
5.  Do NOT regenerate any previously generated mod code. Generate ONLY the new spell blocks.
6.  If no spells were described, output only the comment '-- No new spells required by design document.'.

--- FULL MOD EXAMPLE START ---
{mod_example}
--- FULL MOD EXAMPLE END ---

**Design Document (relevant sections for Spells):**
{expanded_description}""",
        'next_status': 'items',
        'output_field': 'generated_mod_code',
    },
    'items': {
        'action_name': 'Generate Weapons & Armor',
        'prompt_template': """You are an expert Dominions 6 modder. Based on the 'Unique Spells/Items' section and any placeholder equipment mentioned for troops/commanders in the Design Document, generate the Dominions 6 mod commands for any NEW WEAPONS, ARMOR, or MISCELLANEOUS ITEMS.

**CRITICAL INSTRUCTIONS:**
1.  Generate a `#newweapon`, `#newarmor`, or `#newitem` block for EACH item, and EACH block MUST be closed with `#end`.
2.  Use IDs above 8000 for new items to avoid conflicts with vanilla IDs.
3.  Your output MUST EXACTLY follow the syntax of a real Dominions 6 mod file. Study the Full Mod Example provided.
4.  Do NOT include comments within command arguments (e.g., `#copyweapon 108` is correct, NOT `#copyweapon 108 -- comment`).
5.  Do NOT regenerate any previously generated mod code. Generate ONLY the new item blocks.
6.  If no new gear is needed, output only the comment '-- No new items required by design document.'.

--- FULL MOD EXAMPLE START ---
{mod_example}
--- FULL MOD EXAMPLE END ---

**Design Document (relevant sections for Items):**
{expanded_description}""",
        'next_status': 'validation',
        'output_field': 'generated_mod_code',
    },
    'validation': {
        'action_name': 'Validate Mod File Syntax',
        'prompt_template': """You are a meticulous Dominions 6 mod syntax validator. Your task is to analyze the following completed mod file and identify any technical errors that would cause it to fail loading in the game. You must be strict and follow the modding manual precisely.

**Validation Checklist:**
1.  **Block Integrity:** Does every `#newmonster`, `#newweapon`, `#newarmor`, `#newitem`, `#newspell`, and `#selectnation` block have a corresponding `#end` command?
2.  **Command Spelling:** Are all commands (e.g., `#name`, `#hp`, `#magicskill`) spelled correctly? Check for common mistakes like `#strength` instead of `#str`.
3.  **Argument Validity:** Does each command have the correct number and type of arguments? For example, `#hp` takes one number, `#weapon` takes one number, `#magicskill` takes a path letter and a number.
4.  **String Formatting:** Are all string arguments, like in `#name` and `#descr`, enclosed in double quotes?
5.  **No Comments in Arguments:** Ensure no comments are embedded within command arguments (e.g., `#copyweapon 108` is correct, NOT `#copyweapon 108 -- comment`).
6.  **Correct Spell Restriction:** For spells, ensure `#nations` or `#restrictednation` is used, not `#restricted`.
7.  **Valid Effect IDs:** Ensure `#effect` commands use valid IDs or specific effect commands, not placeholders.
8.  **No Duplicate Definitions:** Ensure no `#new...` block is defined more than once with the same ID.

Please review the following mod code against this checklist:
```dominions
{generated_mod_code}
```

Provide your feedback as a concise, bulleted list of specific errors found (e.g., "ERROR: Missing #end for monster 'Clan Chieftain'", "ERROR: The `#strength` command should be `#str`"). If no errors are found, respond with ONLY the phrase: 'Syntax validation passed. The mod appears to be structured correctly and is ready for in-game testing.'""",
        'next_status': 'completed', # Always transitions to completed after validation
        'output_field': 'last_validation_report', # Output of validation goes here
    },
}

def nation_workshop_view(request, pk):
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
    nation = get_object_or_404(Nation, pk=pk)
    current_status = nation.generation_status

    if request.method == 'POST' and current_status in GENERATION_WORKFLOW:
        step_config = GENERATION_WORKFLOW[current_status]
        prompt_template = step_config['prompt_template'] 

        # Initialize all data variables to empty strings
        weapon_data = ""
        armor_data = ""
        mod_commands_data = ""
        mod_example_text = ""
        
        # Conditionally load data based on what the current prompt_template requires
        if "{mod_commands_list}" in prompt_template:
            # Special handling for 'nation_details' step to provide a curated list of commands
            if current_status == 'nation_details':
                # Curated list of common nation-level commands
                curated_nation_commands = [
                    "selectnation", "name", "epithet", "era", "brief", "summary",
                    "color", "flag", "templepic", "idealcold", "idealheat",
                    "idealsorder", "idealdomination", "idealproductivity",
                    "idealgrowth", "idealmisfortune", "idealmagic", "idealfortune",
                    "idealdrain", "idealluck", "idealturmoil", "idealsloth",
                    "idealdeath", "idealunrest", "idealfreshwater", "idealpollution",
                    "spreadheat", "spreadcold", "spreaddeath", "spreadgrowth",
                    "spreadmagic", "spreadfortune", "spreaddrain", "spreadluck",
                    "spreadturmoil", "spreadsloth", "spreadmisfortune", "spreadorder",
                    "nodeathsupply", "halfdeathinc", "halfdeathpop",
                    "labcost", "templecost", "fortcost", "def", "researchbonus",
                    "coastnation", "forestnation", "mountainnation", "swampnation",
                    "wastelandnation", "underwaternation", "caveonly", "nounderwater",
                    "recruitnodeathsupply", "recruitlevel", "homebase",
                    "indisc", "army", "command", "fear", "stealthy", "cavalry",
                    "flying", "firepower", "coldpower", "earthpower", "airpower",
                    "waterpower", "astralpower", "deathpower", "naturepower",
                    "undead", "demon", "god", "magical", "invulnerable", "poisonres",
                    "diseaseres", "wastesurvival", "mountainsurvival", "forestsurvival",
                    "snowsurvival", "desertsurvival", "underwatersurvival", "swampsurvival",
                    "nomad", "hidden", "humanlike", "dragon", "giant", "indie",
                    "mageladder", "barrackscost", "recruitment", "buildcost",
                    "recruitmentcost", "provincetax", "recruitfromall",
                    "recruitchancemult", "recruitfromanywhere", "recruitcap",
                    "recruitmentcap", "militia", "basearmy", "baserecruit", "base",
                    "basemil", "baseint", "basesam", "baseage", "basecommand",
                    "basefear", "baseinspire", "basehp", "baseprot", "basemr",
                    "basemor", "basestrtemp", "baseatt", "basedef", "baseprec",
                    "baseap", "basemapmove", "baseenc", "baseweapon", "basearmor",
                    "basefirepower", "basecoldpower", "baseearthpower", "baseairpower",
                    "basewaterpower", "baseastralpower", "basedeathpower",
                    "basenaturepower", "baseundead", "basedemon", "basegod",
                    "basemagical", "baseinvulnerable", "basepoisonres",
                    "basediseaseres", "basewastesurvival", "basemountainsurvival",
                    "baseforestsurvival", "basesnowsurvival", "basedesertsurvival",
                    "baseunderwatersurvival", "baseswampsurvival", "basenomad",
                    "basehidden", "basehumanlike", "basedragon", "basegiant", "baseindie",
                    "domsize", "domcost", # Keep these two as they are general dominion commands
                ]
                mod_commands_data = "\\n".join([f"#{cmd}" for cmd in curated_nation_commands])
            else:
                # For other steps, use the existing sampling logic for attribute_keys
                mod_commands_queryset = GameEntity.objects.filter(entity_type='attribute_keys').order_by('?').values_list('name', flat=True)
                mod_commands_data = "\\n".join([f"#{cmd}" for cmd in mod_commands_queryset[:200]]) 

        if "{weapon_list}" in prompt_template:
            weapon_queryset = GameEntity.objects.filter(entity_type='weapons').order_by('?').values_list('reference_text', flat=True)
            weapon_data = "\\n".join(weapon_queryset[:50]) 

        if "{armor_list}" in prompt_template:
            armor_queryset = GameEntity.objects.filter(entity_type='armors').order_by('?').values_list('reference_text', flat=True)
            armor_data = "\\n".join(armor_queryset[:50]) 
        
        if "{mod_example}" in prompt_template:
            specific_example_name = "Comprehensive Mod Example" # Always use this one now
            try:
                mod_example_text = ModExample.objects.get(name=specific_example_name).mod_text
            except ModExample.DoesNotExist:
                example_count = ModExample.objects.count()
                if example_count > 0:
                    random_index = random.randint(0, example_count - 1)
                    mod_example_text = ModExample.objects.all()[random_index].mod_text
        
        # Build prompt_context conditionally based on what the *current* prompt_template needs
        prompt_context = {
            "nation_description": nation.description or "",
            "expanded_description": nation.expanded_description or "",
            "weapon_list": weapon_data,
            "armor_list": armor_data,
            "mod_commands_list": mod_commands_data,
            "mod_example": mod_example_text,
        }

        # Only add generated_mod_code and last_validation_report if the template explicitly asks for them
        if "{generated_mod_code}" in prompt_template:
            prompt_context["generated_mod_code"] = nation.generated_mod_code or ""
        
        if "{last_validation_report}" in prompt_template:
            prompt_context["last_validation_report"] = nation.last_validation_report or ""

        prompt = prompt_template.format(**prompt_context)
        
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables.")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')
            response = model.generate_content(prompt)
            
            output_field = step_config['output_field']
            
            if output_field == 'generated_mod_code':
                # Always append for generation steps (no fixing_errors branch)
                header = f"\\n\\n--//-- STEP: {current_status.upper()} --//--"
                new_content = f"{header}\\n{response.text.strip()}"
                
                if nation.generated_mod_code is None or current_status == 'nation_details':
                    nation.generated_mod_code = new_content
                else:
                    nation.generated_mod_code += new_content
                
                # After any code generation, clear the last validation report
                nation.last_validation_report = None 

            elif output_field == 'last_validation_report':
                # This is the validation step's output
                validation_output = response.text.strip()
                nation.last_validation_report = validation_output

                # Always set to 'completed' after validation, regardless of errors
                nation.generation_status = 'completed' 
                
                # Clear report only if validation passed (original phrase)
                if "Syntax validation passed." in validation_output:
                    nation.last_validation_report = None 
            else: # This handles 'expanded_description' for 'not_started'
                # Check if the response text is empty or only whitespace
                if not response.text.strip():
                    nation.generation_status = 'failed' # Only fail if AI returns empty content
                    nation.last_validation_report = "AI failed to generate expanded description. Response was empty or invalid."
                else:
                    setattr(nation, output_field, response.text)

            # Set next status for all non-validation steps, and only if not already failed by empty response
            if current_status != 'validation' and nation.generation_status != 'failed':
                nation.generation_status = step_config['next_status']
            
            nation.save()

        except Exception as e:
            nation.generation_status = 'failed'
            nation.last_validation_report = f"An unexpected error occurred during generation: {e}" # Store error for debugging
            nation.save()

    return redirect('nations:nation_workshop', pk=nation.pk)
