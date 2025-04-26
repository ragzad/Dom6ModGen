# dom6modgen/urls.py
# Located at: D:\OllamaUI\Dom6ModGen\dom6modgen\dom6modgen\urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

urlpatterns = [
    # When a user visits '/', redirect them to the URL named 'nations:nation_list'
    # reverse_lazy finds the actual path (e.g., '/nations/') from the URL name
    path('', RedirectView.as_view(url=reverse_lazy('nations:nation_list')), name='home'),

    path('admin/', admin.site.urls),
    path('nations/', include('nations.urls')),

    # --- Add includes for other apps later ---
    # path('units/', include('units.urls')),
    # path('spells/', include('spells.urls')),
    # path('items/', include('items.urls')),
]