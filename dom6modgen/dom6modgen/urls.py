# dom6modgen/urls.py
# Main URL configuration for the Dominions 6 Mod Generator project.

from django.contrib import admin
from django.urls import path, include
# Importing RedirectView for the root redirect.
from django.views.generic.base import RedirectView
# reverse_lazy is no longer needed for this specific redirect.
# from django.urls import reverse_lazy

urlpatterns = [
    # Defining the path for the site's root URL ('').
    # Using a direct path '/nations/' for the redirect URL
    # to avoid the namespace lookup issue encountered with reverse_lazy here.
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
