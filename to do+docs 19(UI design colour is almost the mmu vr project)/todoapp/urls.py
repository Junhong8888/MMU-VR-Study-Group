from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<int:id>/', views.DeleteTask, name='delete'),
    path('update/<int:id>/', views.Update, name='update'),
    path('task/<int:id>/', views.TaskDetail, name='task-detail'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('edit/<int:pk>/', views.document_edit, name='document_edit'),
    path('documents/create/', views.document_create, name='document_create'),
    path('documents/delete/<int:pk>/', views.document_delete, name='document_delete'),
    path('documents/', views.document_list, name='document_list'),



]