from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "todoapp"

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'),
    path('update/<str:name>/', views.Update, name='update'),
    path('task/<str:name>/', views.TaskDetail, name='task-detail'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('edit/<int:pk>/', views.document_edit, name='document_edit'),
    path('documents/create/', views.document_create, name='document_create'),

]