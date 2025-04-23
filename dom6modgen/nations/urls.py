from django.urls import path
from . import views # Import views from the current directory (nations app)

app_name = 'nations' 

urlpatterns = [
    path('', views.nation_list, name='nation_list'),
    path('<int:pk>/', views.nation_detail, name='nation_detail'),
    path('new/', views.nation_create, name='nation_create'),
]