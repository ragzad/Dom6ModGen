from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

# Import settings and static for development serving
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    # Using a direct path '/nations/' for the redirect URL.
    path('', RedirectView.as_view(url='/nations/'), name='home'),

    # Standard path for the Django admin interface.
    path('admin/', admin.site.urls),
    # Including URLs from the 'nations' app under the '/nations/' prefix.
    path('nations/', include('nations.urls')),
]