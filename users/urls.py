from django.urls import path 
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('main/', views.main,name="main"),
    path('logout/',views.user_logout,name='logout'),
    path('login_signup',views.login_signup,name='login_signup')
]