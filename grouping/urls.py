from django.urls import path
from . import views

urlpatterns = [
    path('',views.group,name='group'),
    path('create-room/',views.createRoom,name='create_room'),
    path('join_group/', views.join_group, name='join_group'),
    path('grouping/workspace/<str:Room_join_code>/', views.workspace, name='workspace'),
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'),
    path('update/<str:name>/', views.Update, name='update'),
    path('task/<str:name>/', views.TaskDetail, name='task-detail'),
]