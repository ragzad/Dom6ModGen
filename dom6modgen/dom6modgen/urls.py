# nations/urls.py
from django.urls import path
from . import views # Import views from the current app

# Define the namespace for this app's URLs
app_name = 'nations'

urlpatterns = [
    # URL for the list of nations (e.g., /nations/)
    path('', views.nation_list, name='nation_list'),
    # URL for viewing a single nation's details (e.g., /nations/5/)
    path('<int:pk>/', views.nation_detail, name='nation_detail'),
    # URL for creating a new nation (e.g., /nations/new/)
    path('new/', views.nation_create, name='nation_create'),
    # URL for updating an existing nation (e.g., /nations/5/edit/)
    path('<int:pk>/edit/', views.nation_update, name='nation_update'),
    # URL for deleting a nation (e.g., /nations/5/delete/)
    path('<int:pk>/delete/', views.nation_delete, name='nation_delete'),
    # URL for generating the DM file (e.g., /nations/5/generate/)
    path('<int:pk>/generate/', views.nation_generate_dm, name='nation_generate_dm'),
]