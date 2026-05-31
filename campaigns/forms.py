from django import forms

from .models import Campaign


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            "title",
            "description",
            "game_system",
            "status",
            "visibility",
            "cover",
            "tags",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "tags": forms.CheckboxSelectMultiple(),
        }