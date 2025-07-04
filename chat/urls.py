from django.urls import path 
from . import views

app_name = 'chat'

urlpatterns = [
    path('',views.index,name='chat'),
    path('<str:room_name>/',views.room,name='room'),
    path('etherpad/<str:room_name>/', views.etherpad, name='etherpad')
]