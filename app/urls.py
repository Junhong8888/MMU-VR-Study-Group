from django.urls import path 
from . import views 


urlpatterns = [
    path("",views.index, name="app-index"),
    path("dashboard", views.index, name="app-dashboard"),
    path("home", views.home, name="home"),
      path('dashboard/', views.index, name='dashboard'),
]