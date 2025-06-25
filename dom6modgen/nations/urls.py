from django.urls import path
from . import views

app_name = 'nations'

urlpatterns = [
    path('', views.NationListView.as_view(), name='nation_list'),
    path('<int:pk>/', views.NationDetailView.as_view(), name='nation_detail'),
    path('new/', views.NationCreateView.as_view(), name='nation_create'),
    path('<int:pk>/edit/', views.NationUpdateView.as_view(), name='nation_update'),
    path('<int:pk>/delete/', views.NationDeleteView.as_view(), name='nation_delete'),
    
    # New URLs for the segmented generation process
    path('<int:pk>/workshop/', views.nation_workshop_view, name='nation_workshop'),
    path('<int:pk>/workshop/run_step/', views.run_generation_step_view, name='run_generation_step'),
]