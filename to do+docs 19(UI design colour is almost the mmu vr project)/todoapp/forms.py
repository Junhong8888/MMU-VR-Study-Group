from django import forms
from .models import todo
from django.contrib.auth.models import User
from .models import Document

class TodoForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['todo_name', 'assigned_to', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),  # calendar
        }

    assigned_to = forms.CharField(required=False)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content']