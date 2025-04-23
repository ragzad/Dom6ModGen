from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import Nation # Import the Nation model
from .forms import NationForm

def nation_list(request):
    """
    View function to display a list of all Nations.
    """
    # 1. Get all Nation objects from the database
    nations = Nation.objects.all().order_by('name') # Get all nations, order by name

    # 2. Create a context dictionary to pass data to the template
    #The key 'nations' will be the variable name used in the template
    context = {
        'nations': nations,
    }

    # 3. Render the HTML template, passing the request and context
    return render(request, 'nations/nation_list.html', context)

def nation_detail(request, pk):

    # 1. Get the specific Nation object using the pk, or raise a 404 error if not found
    nation = get_object_or_404(Nation, pk=pk)

    # 2. Create a context dictionary to pass the single nation object to the template
    context = {
        'nation': nation,
    }

    # 3. Render the HTML template for the detail view
    return render(request, 'nations/nation_detail.html', context)
def nation_create(request):
    """
    View function to handle the creation of a new Nation.
    Shows an empty form on GET, processes submitted data on POST.
    """
    if request.method == 'POST':
        # If the form was submitted, process the data
        form = NationForm(request.POST) # Create form instance with submitted data
        if form.is_valid():
            # Form data is valid, save the new Nation object
            # might use: new_nation = form.save(commit=False); new_nation.creator = request.user; new_nation.save()
            form.save()
            # Redirect to the nation list page after successful creation
            # return redirect('nations:nation_detail', pk=new_nation.pk)
            return redirect('nations:nation_list')
        # If form is NOT valid, execution continues below
    else:
        # If it's a GET request (or form was invalid), show an empty form
        form = NationForm()

    # Prepare the context for the template
    context = {
        'form': form,
    }
    # Render form template
    return render(request, 'nations/nation_form.html', context)
