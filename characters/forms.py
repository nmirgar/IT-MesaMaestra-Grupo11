from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = [
            'name', 'character_class', 'race', 'level', 
            'background', 'hit_points', 'avatar', 'campaign', 'sheet'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del personaje'}),
            'character_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Bárbaro, Mago...'}),
            'race': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Humano, Elfo...'}),
            'level': forms.NumberInput(attrs={'class': 'form-control'}),
            'background': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hit_points': forms.NumberInput(attrs={'class': 'form-control'}),
            'campaign': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'sheet': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }