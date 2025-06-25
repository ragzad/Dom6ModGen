from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Nation, GENERATION_STATUS_CHOICES
from .forms import NationForm
import google.generativeai as genai
import os

# --- Class-Based Views (Required for basic site navigation) ---
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

# This dictionary defines the step-by-step workflow for the AI generation.
GENERATION_WORKFLOW = {
    'not_started': {
        'action_name': 'Expand Idea into a Full Concept',
        'prompt_template': """You are a creative assistant for the game Dominions 6. A user has provided a basic idea for a new nation. Your task is to expand this idea into a detailed design document. This document should be comprehensive enough for a modder to create a complete and thematic faction. Do NOT generate any mod code, only the descriptive plan.

The user's idea is: '{nation_description}'

Please expand on this by describing the following in detail:
1.  **Overall Theme and Lore**: The nation's backstory, culture, and primary motivations.
2.  **National Features**: Key strengths and weaknesses (magic paths, temperature, resources, etc.).
3.  **Commanders**: 3-5 key commander types with thematic descriptions.
4.  **Troops**: 5-7 distinct troop types (infantry, archers, cavalry, sacreds) with equipment and roles.
5.  **Magic**: Common/rare magic paths and ideas for unique spells.
6.  **Heroes/Summons**: Ideas for 1-2 unique heroes and national summons.

Present this as a clear, well-organized document.""",
        'next_status': 'nation_details',
        'output_field': 'expanded_description', # The model field to save the result to
    },
    'nation_details': {
        'action_name': 'Generate Nation Details & Tags',
        'prompt_template': """Based on the following design document, generate ONLY the initial Dominions 6 mod commands for the nation. This includes #newnation, #era, #epithet, #descr, #summary, and relevant nation-level tags like #likespop, #def, #fortcost, etc. Do NOT generate any units, items, or spells yet.

**Design Document:**
{expanded_description}""",
        'next_status': 'commanders',
        'output_field': 'generated_mod_code',
    },
    'commanders': {
        'action_name': 'Generate Commanders',
        'prompt_template': """Based on the design document and previously generated code, generate ONLY the Dominions 6 mod commands for all the COMMANDERS. Do not generate troops. Use the #newmonster command.

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
        'prompt_template': """Based on the design document and previously generated code, generate ONLY the Dominions 6 mod commands for all the TROOPS (non-commanders). Use the #newmonster command.

**Design Document:**
{expanded_description}

**Previously Generated Code:**
```dominions
{generated_mod_code}
```""",
        'next_status': 'weapons',
        'output_field': 'generated_mod_code',
    },
    'weapons': {
        'action_name': 'Generate New Weapons',
        'prompt_template': """Based on the design document and previously generated units, generate ONLY the Dominions 6 mod commands for any NEW WEAPONS needed by those units. If no new weapons are described, output only the comment '-- No new weapons required.'. Use the #newweapon command.

**Design Document:**
{expanded_description}

**Previously Generated Code:**
```dominions
{generated_mod_code}
```""",
        'next_status': 'completed', # Change this to 'armor' when you add that step
        'output_field': 'generated_mod_code',
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
    
    if current_status != 'completed' and current_status != 'failed':
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
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            output_field = step_config['output_field']
            if output_field == 'generated_mod_code' and nation.generated_mod_code:
                # Append to existing code, adding comments to delineate steps
                nation.generated_mod_code += f"\n\n-- Step: {current_status} --\n{response.text}"
            else:
                setattr(nation, output_field, response.text)

            nation.generation_status = step_config['next_status']
            nation.save()

        except Exception as e:
            nation.generation_status = 'failed'
            nation.save()
            print(f"Error during generation step '{current_status}': {e}") # This will print to Heroku logs

    return redirect('nations:nation_workshop', pk=nation.pk)