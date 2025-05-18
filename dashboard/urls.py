from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name="dashboard-index"),
    path('home', views.home, name="dashboard-home"), 
    path('report/', views.reports, name="reports"), 
]
