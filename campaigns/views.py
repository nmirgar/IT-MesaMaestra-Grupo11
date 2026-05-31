from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CampaignForm
from .models import Campaign, Participation
from .permissions import can_view_campaign, is_campaign_director


class CampaignListView(ListView):
    model = Campaign
    template_name = "campaigns/campaign_list.html"
    context_object_name = "campaigns"

    def get_queryset(self):
        queryset = Campaign.objects.all().prefetch_related("tags").select_related("director")

        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(visibility=Campaign.Visibility.PUBLIC)
                | Q(director=self.request.user)
                | Q(participations__user=self.request.user,
                    participations__status=Participation.Status.ACCEPTED)
            ).distinct()
        else:
            queryset = queryset.filter(visibility=Campaign.Visibility.PUBLIC)

        return queryset


class CampaignDetailView(DetailView):
    model = Campaign
    template_name = "campaigns/campaign_detail.html"
    context_object_name = "campaign"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def dispatch(self, request, *args, **kwargs):
        campaign = self.get_object()

        if not can_view_campaign(request.user, campaign):
            messages.error(request, "No tienes permiso para ver esta campaña.")
            return redirect("campaigns:list")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = self.object
        context["is_director"] = is_campaign_director(self.request.user, campaign)
        return context


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"

    def form_valid(self, form):
        form.instance.director = self.request.user
        response = super().form_valid(form)

        Participation.objects.get_or_create(
            user=self.request.user,
            campaign=self.object,
            defaults={
                "role": Participation.Role.DIRECTOR,
                "status": Participation.Status.ACCEPTED,
            }
        )

        messages.success(self.request, "Campaña creada correctamente.")
        return response


class CampaignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def test_func(self):
        campaign = self.get_object()
        return is_campaign_director(self.request.user, campaign)

    def form_valid(self, form):
        messages.success(self.request, "Campaña actualizada correctamente.")
        return super().form_valid(form)


class CampaignDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Campaign
    template_name = "campaigns/campaign_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("campaigns:list")

    def test_func(self):
        campaign = self.get_object()
        return is_campaign_director(self.request.user, campaign)

    def form_valid(self, form):
        messages.success(self.request, "Campaña eliminada correctamente.")
        return super().form_valid(form)