from django import forms
from .models import Room

class GroupForm(forms.ModelForm):
    
    class Meta:
        fields =  ['roomname', 'description', 'topic']
        model = Room

class JoinCodeForm(forms.Form):
    join_code = forms.CharField(max_length=10, required=True)

    def clean_join_code(self):
        data = self.cleaned_data['join_code']
        if not Room.objects.filter(join_code=data).exists():
            raise forms.ValidationError("Invalid join code.")
        return data