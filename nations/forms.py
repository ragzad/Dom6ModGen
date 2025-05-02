from django import forms
from .models import Nation

class NationForm(forms.ModelForm):
    class Meta:
        model = Nation
        # Specify which fields from the Nation model should be included in the form
        fields = ['name', 'description']
        # We exclude 'creator', 'created_at', 'updated_at' as they
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows': 4}),
        # }