# Dom6ModGen/dom6modgen/nations/urls.py
from django.urls import path
from . import views # Your existing views import

app_name = 'nations' # Important for namespacing URLs

urlpatterns = [
    # Your existing CRUD URLs for Nations
    path('', views.nation_list, name='nation_list'),
    path('create/', views.nation_create, name='nation_create'),
    path('<int:pk>/', views.nation_detail, name='nation_detail'),
    path('<int:pk>/update/', views.nation_update, name='nation_update'),
    path('<int:pk>/delete/', views.nation_delete, name='nation_delete'),

    # URL for the page that will host the JavaScript-driven interactive generation
    path('<int:pk>/generate/', views.nation_generate_interactive_page, name='nation_generate_interactive_page'),

    # API-like endpoints for the client-side JavaScript to call
    path('api/<int:nation_pk>/initiate_generation/', views.initiate_mod_generation, name='initiate_mod_generation_api'),
    path('api/generate_component/', views.generate_component_view, name='generate_component_api'), # Note: No PK here, job_id in POST body
    path('api/compile_mod/<int:job_id>/', views.compile_mod_file_view, name='compile_mod_api'),
    
    # URL for downloading the final compiled .dm file
    path('download_mod/<int:job_id>/', views.download_mod_file_view, name='download_mod_file'),
]
