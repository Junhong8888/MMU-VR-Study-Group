from django.urls import path
from . import views  # ✅ Import the views module

urlpatterns = [
    path('load_messages/<int:workspace_id>/', views.load_messages, name='load_messages'),
]
