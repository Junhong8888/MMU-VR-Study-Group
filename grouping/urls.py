from django.urls import path
from . import views

urlpatterns = [
    path('',views.group,name='group'),
    path('create-room/',views.createRoom,name='create_room'),
    path('join_group/', views.join_group, name='join_group'),
    path('workspace/', views.host_workspace, name='host_workspace'),
]