from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Character
from .forms import CharacterForm
from campaigns.models import Campaign

from campaigns.permissions import is_campaign_director, is_campaign_participant

class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    template_name = "characters/character_list.html"
    context_object_name = "characters"

    def get_queryset(self):
        # Cada usuario solo ve sus propios personajes
        return Character.objects.filter(owner=self.request.user)

class CharacterDetailView(UserPassesTestMixin, DetailView):
    model = Character
    template_name = "characters/character_detail.html"

    def test_func(self):
        character = self.get_object()
        
        # Si el personaje pertenece a una campaña pública, cualquiera puede verlo
        if character.campaign and character.campaign.visibility == 'PUBLIC':
            return True
        # Si el personaje no es público, solo el dueño, el director de la campaña o los participantes pueden verlo
        if not self.request.user.is_authenticated:
            return False
        # El dueño y participantes del personaje siempre puede verlo
        if character.owner == self.request.user:
            return True
        if character.campaign:
            if is_campaign_director(self.request.user, character.campaign):
                return True
            if is_campaign_participant(self.request.user, character.campaign):
                return True
        return False
    
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para ver la ficha de este personaje.")
        return redirect('characters:list')

class CharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = "characters/character_form.html"
    success_url = reverse_lazy('characters:list')

    def form_valid(self, form):
        # Asignamos automáticamente el usuario autenticado como propietario
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CharacterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = "characters/character_form.html"

    def test_func(self):
        # Solo el dueño puede editar
        return self.get_object().owner == self.request.user

    def handle_no_permission(self):
        # Mensaje si intenta editar algo que no es suyo
        messages.error(self.request, "¡Alto ahí! No puedes editar un personaje que no es tuyo.")
        return redirect('characters:list')

    def get_success_url(self):
        return reverse_lazy('characters:detail', kwargs={'pk': self.object.pk})

class CharacterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Character
    template_name = "characters/character_confirm_delete.html"
    success_url = reverse_lazy('characters:list')

    def test_func(self):
        # Solo el dueño puede borrar
        return self.get_object().owner == self.request.user

    def handle_no_permission(self):
        # Mensaje si intenta borrar algo que no es suyo
        messages.error(self.request, "¡Alto ahí! No puedes borrar un personaje que no es tuyo.")
        return redirect('characters:list')

class CampaignCharacterListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Character
    template_name = "characters/campaign_character_list.html"
    context_object_name = "characters"

    def test_func(self):
        campaign = get_object_or_404(Campaign, slug=self.kwargs['campaign_slug'])
        
        # Si la campaña es pública, dejamos pasar
        if campaign.visibility == 'PUBLIC':
            return True
        # Si no es pública, comprobamos si es director o participante
        if is_campaign_director(self.request.user, campaign):
            return True
        if is_campaign_participant(self.request.user, campaign):
            return True
            
        # Si es privada y no eres nadie de la partida, acceso denegado
        return False

    def get_queryset(self):
        # Filtramos para que solo salgan los de esta campaña
        return Character.objects.filter(campaign__slug=self.kwargs['campaign_slug'])

    def get_context_data(self, **kwargs):
        # Pasamos la campaña a la plantilla HTML para poder poner el título
        context = super().get_context_data(**kwargs)
        context['campaign'] = get_object_or_404(Campaign, slug=self.kwargs['campaign_slug'])
        return context
