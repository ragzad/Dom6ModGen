# nations/views.py
# Handles web requests related to Nations, including triggering AI generation tasks.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages # For user feedback via Django messages framework

from .models import Nation, NationGenerationStatus # Nation model and status choices
from .forms import NationForm # Form for creating/editing nations
from .tasks import generate_nation_dm_task # The Celery task for background generation

# Note: Vertex AI client setup is now handled in vertex_client.py
# Note: Gemini API setup is handled where it's used (in tasks.py)

# --- Standard Django Views ---

def nation_list(request):
    """Displays a list of all nations."""
    nations = Nation.objects.all().order_by('name')
    context = { 'nations': nations }
    return render(request, 'nations/nation_list.html', context)

def nation_detail(request, pk):
    """Displays the details of a specific nation."""
    nation = get_object_or_404(Nation, pk=pk)
    context = { 'nation': nation }
    return render(request, 'nations/nation_detail.html', context)

def nation_create(request):
    """Handles the creation of a new nation via a form."""
    if request.method == 'POST':
        form = NationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Nation '{form.cleaned_data['name']}' created successfully.")
            return redirect('nations:nation_list')
    else:
        form = NationForm()
    context = { 'form': form }
    return render(request, 'nations/nation_form.html', context)

def nation_update(request, pk):
    """Handles updating an existing nation via a form."""
    nation = get_object_or_404(Nation, pk=pk)
    if request.method == 'POST':
        form = NationForm(request.POST, instance=nation)
        if form.is_valid():
            form.save()
            messages.success(request, f"Nation '{nation.name}' updated successfully.")
            return redirect('nations:nation_detail', pk=nation.pk)
    else:
        form = NationForm(instance=nation)
    context = { 'form': form, 'nation': nation }
    return render(request, 'nations/nation_form.html', context)

def nation_delete(request, pk):
    """Handles the confirmation and deletion of a nation."""
    nation = get_object_or_404(Nation, pk=pk)
    if request.method == 'POST':
        nation_name = nation.name
        nation.delete()
        messages.success(request, f"Nation '{nation_name}' deleted successfully.")
        return redirect('nations:nation_list')
    context = { 'nation': nation }
    return render(request, 'nations/nation_confirm_delete.html', context)


# --- AI Generation Trigger View ---

def nation_generate_dm(request, pk):
    """
    Handles POST requests to trigger the background Celery task for generating
    Dominions 6 mod code for a specific nation.
    Redirects GET requests back to the nation detail page.
    """
    nation = get_object_or_404(Nation, pk=pk)

    if request.method == 'POST':
        # Prevent starting a new task if one is already running or queued.
        if nation.generation_status in [NationGenerationStatus.PENDING, NationGenerationStatus.GENERATING]:
             messages.warning(request, f"Generation for '{nation.name}' is already in progress (Task ID: {nation.generation_task_id}). Please wait.")
        else:
            # Dispatch the background task using Celery.
            print(f"Dispatching generation task for Nation ID: {pk}")
            try:
                # .delay() is a shortcut to send the task to the queue.
                task = generate_nation_dm_task.delay(nation_id=pk)
                print(f"Task {task.id} dispatched for Nation ID: {pk}")

                # Update the nation's status to show it's pending.
                nation.generation_status = NationGenerationStatus.PENDING
                nation.generation_task_id = task.id
                nation.generated_dm_code = None # Clear previous results
                nation.generation_error = None # Clear previous error
                nation.save(update_fields=['generation_status', 'generation_task_id', 'generated_dm_code', 'generation_error'])

                messages.success(request, f"Generation started for '{nation.name}' (Task ID: {task.id}). Results will appear on the nation detail page when complete.")
            except Exception as e:
                # Handle errors during the task dispatch process itself.
                print(f"Error dispatching task for Nation ID {pk}: {e}")
                messages.error(request, f"Could not start generation task for '{nation.name}'. Error: {e}")
                nation.generation_status = NationGenerationStatus.FAILURE
                nation.generation_error = f"Failed to dispatch task: {e}"[:1024] # Store error, truncate if needed
                nation.save(update_fields=['generation_status', 'generation_error'])

        # Always redirect back to the detail page after a POST attempt.
        return redirect('nations:nation_detail', pk=nation.pk)

    # If it's a GET request, just redirect back to the detail page.
    # Optionally add a message explaining how to trigger generation.
    # messages.info(request, "Click the 'Generate DM Code' button to start generation.")
    return redirect('nations:nation_detail', pk=nation.pk)

