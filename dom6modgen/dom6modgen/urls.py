# dom6modgen/urls.py
# Main URL configuration for the Dominions 6 Mod Generator project.

from django.contrib import admin
from django.urls import path, include
# Importing RedirectView for the root redirect.
# No longer need reverse_lazy for this specific redirect.
from django.views.generic.base import RedirectView
# from django.urls import reverse_lazy # Can remove if not used elsewhere in this file

urlpatterns = [
    # Defining the path for the site's root URL ('').
    # Using a direct path '/nations/' for the redirect URL
    # instead of reverse_lazy to avoid the namespace lookup issue.
    path('', RedirectView.as_view(url='/nations/'), name='home'), # <-- MODIFIED LINE

    # Standard path for the Django admin interface.
    path('admin/', admin.site.urls),
    # Including URLs from the 'nations' app under the '/nations/' prefix.
    path('nations/', include('nations.urls')),

    # Placeholders for including other app URLs later.
    # path('units/', include('units.urls')),
    # path('spells/', include('spells.urls')),
    # path('items/', include('items.urls')),
]
