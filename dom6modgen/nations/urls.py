from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views

# Import settings and static for development serving
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.nation_list, name='nation_list'),
    path('<int:pk>/', views.nation_detail, name='nation_detail'),
    path('new/', views.nation_create, name='nation_create'),
    path('<int:pk>/edit/', views.nation_update, name='nation_update'),
    path('<int:pk>/delete/', views.nation_delete, name='nation_delete'),
    path('<int:pk>/generate_dm/', views.nation_generate_dm, name='nation_generate_dm'),
    path('debug-settings/', views.debug_settings_view, name='debug_settings'), # Add this line
]