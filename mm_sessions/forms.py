from django import forms
from .models import MmSession


class MmSessionForm(forms.ModelForm):
    class Meta:
        model = MmSession
        fields = [
            'title', 'summary', 'scheduled_at',
            'estimated_duration', 'status',
            'fictional_location', 'director_notes',
        ]
        widgets = {
            'scheduled_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
            ),
            'summary': forms.Textarea(attrs={'rows': 3}),
            'director_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheduled_at'].input_formats = ['%Y-%m-%dT%H:%M']