# prison_core/forms.py
from django import forms
from .models import Prisoner

class PrisonerForm(forms.ModelForm):
    class Meta:
        model = Prisoner
        fields = ['first_name', 'last_name', 'prisoner_id', 'date_of_birth', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }