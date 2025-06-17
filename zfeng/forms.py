from django import forms
from .models import todo
from django.contrib.auth.models import User
from grouping.models import Document

class TodoForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['todo_name',  'due_date', 'status']


class TaskForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['todo_name', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content']