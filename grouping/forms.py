from django import forms
from .models import Room

class GroupForm(forms.ModelForm):
    
    class Meta:
        fields =  ['roomname', 'description', 'topic']
        model = Room