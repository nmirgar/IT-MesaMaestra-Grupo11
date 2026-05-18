from django import forms
from .models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            'title', 'resource_type', 'description',
            'file', 'external_url', 'visible_to_players',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }