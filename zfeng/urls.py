from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'zfeng'


urlpatterns = [
    path('', views.home, name='todolist'),
    path('delete-task/<int:id>/', views.DeleteTask, name='delete'),
    path('update/<int:id>/', views.Update, name='update'),
    path('task/<int:id>/', views.TaskDetail, name='task-detail'),
]