from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from campaigns.models import Campaign
from campaigns.permissions import can_view_campaign, is_campaign_director

from .forms import ResourceForm
from .models import Resource


def resource_list(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)

    if not can_view_campaign(request.user, campaign):
        raise PermissionDenied

    resources = campaign.resources.all()

    if not is_campaign_director(request.user, campaign):
        resources = resources.filter(visible_to_players=True)

    return render(request, "resources/resource_list.html", {
        "campaign": campaign,
        "resources": resources,
        "is_director": is_campaign_director(request.user, campaign),
    })


def resource_detail(request, slug, pk):
    resource = get_object_or_404(Resource, pk=pk, campaign__slug=slug)
    campaign = resource.campaign

    if not can_view_campaign(request.user, campaign):
        raise PermissionDenied

    if not resource.visible_to_players and not is_campaign_director(request.user, campaign):
        raise PermissionDenied

    return render(request, "resources/resource_detail.html", {
        "resource": resource,
        "is_director": is_campaign_director(request.user, campaign),
    })


@login_required
def resource_create(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)

    if not is_campaign_director(request.user, campaign):
        raise PermissionDenied

    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.campaign = campaign
            resource.created_by = request.user
            resource.save()
            return redirect("resources:resource_list", slug=slug)
    else:
        form = ResourceForm()

    return render(request, "resources/resource_form.html", {
        "form": form,
        "campaign": campaign,
    })


@login_required
def resource_delete(request, slug, pk):
    resource = get_object_or_404(Resource, pk=pk, campaign__slug=slug)

    if not is_campaign_director(request.user, resource.campaign):
        raise PermissionDenied

    if request.method == "POST":
        resource.delete()
        return redirect("resources:resource_list", slug=slug)

    return render(request, "resources/resource_confirm_delete.html", {
        "resource": resource,
    })