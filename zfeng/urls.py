from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'zfeng'


urlpatterns = [
    path('', views.home, name='todolist'),
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'),
    path('update/<str:name>/', views.Update, name='update'),
    path('task/<str:name>/', views.TaskDetail, name='task-detail'),
]