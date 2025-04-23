from django.shortcuts import render
from .models import Nation # Import the Nation model

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