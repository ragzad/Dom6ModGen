# dom6modgen/urls.py
# Main URL configuration for the Dominions 6 Mod Generator project.

from django.contrib import admin
from django.urls import path, include
# Importing RedirectView for the root redirect.
from django.views.generic.base import RedirectView


urlpatterns = [
    # Defining the path for the site's root URL ('').
    # Using a direct path '/nations/' for the redirect URL.
    path('', RedirectView.as_view(url='/nations/'), name='home'),

    # Standard path for the Django admin interface.
    path('admin/', admin.site.urls),
    # Including URLs from the 'nations' app under the '/nations/' prefix.
    path('nations/', include('nations.urls')),

    # Placeholders for including other app URLs later.
    # path('units/', include('units.urls')),
    # path('spells/', include('spells.urls')),
    # path('items/', include('items.urls')),
]
