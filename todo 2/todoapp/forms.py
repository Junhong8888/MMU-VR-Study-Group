from django import forms
from .models import todo
from django.contrib.auth.models import User

class TodoForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['todo_name', 'assigned_to', 'due_date', 'status']
