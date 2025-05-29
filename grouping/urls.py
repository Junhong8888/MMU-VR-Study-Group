from django.urls import path
from . import views

app_name = "grouping"

urlpatterns = [
    path('',views.group,name='group'),
    path('create-room/',views.createRoom,name='create_room'),
    path('join_group/', views.join_group, name='join_group'),
    path('workspace/<str:Room_join_code>/', views.workspace, name='workspace'),
    path('delete-task/<int:id>/', views.DeleteTask, name='delete'),
    path('update/<int:id>/', views.Update, name='update'),
    path('task/<int:id>/', views.TaskDetail, name='task-detail'),
     path('ranking/<str:Room_join_code>/', views.ranking, name='ranking'),

]