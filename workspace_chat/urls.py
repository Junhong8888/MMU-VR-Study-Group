from django.urls import path
from . import views

urlpatterns = [
    path('api/chat/<int:workspace_id>/messages/', views.load_messages, name='load_messages'),
]
