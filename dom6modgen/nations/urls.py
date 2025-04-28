# dom6modgen/urls.py
# Main URL configuration for the Dominions 6 Mod Generator project.

from django.contrib import admin
from django.urls import path, include
# Importing RedirectView and reverse_lazy to handle the root URL redirect.
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

urlpatterns = [
    # Defining the path for the site's root URL ('').
    # This redirects users directly to the nation list page for convenience,
    # using reverse_lazy to find the URL associated with the 'nations:nation_list' name.
    path('', RedirectView.as_view(url=reverse_lazy('nations:nation_list')), name='home'),

    # Standard path for the Django admin interface.
    path('admin/', admin.site.urls),
    # Including URLs from the 'nations' app under the '/nations/' prefix.
    path('nations/', include('nations.urls')),

    # Placeholders for including other app URLs later.
    # path('units/', include('units.urls')),
    # path('spells/', include('spells.urls')),
    # path('items/', include('items.urls')),
]
