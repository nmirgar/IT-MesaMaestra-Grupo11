from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from campaigns.models import Campaign
from .models import Resource
from .forms import ResourceForm


def resource_list(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.visibility == 'PRIVATE':
        if not request.user.is_authenticated:
            raise PermissionDenied
    resources = campaign.resources.all()
    if request.user != campaign.director:
        resources = resources.filter(visible_to_players=True)
    return render(request, 'resources/resource_list.html', {
        'campaign': campaign,
        'resources': resources,
    })


def resource_detail(request, slug, pk):
    resource = get_object_or_404(Resource, pk=pk, campaign__slug=slug)
    if not resource.visible_to_players and request.user != resource.campaign.director:
        raise PermissionDenied
    return render(request, 'resources/resource_detail.html', {'resource': resource})


@login_required
def resource_create(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.director != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.campaign = campaign
            resource.created_by = request.user
            resource.save()
            return redirect('resources:resource_list', slug=slug)
    else:
        form = ResourceForm()
    return render(request, 'resources/resource_form.html', {
        'form': form, 'campaign': campaign
    })


@login_required
def resource_delete(request, slug, pk):
    resource = get_object_or_404(Resource, pk=pk, campaign__slug=slug)
    if resource.campaign.director != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        resource.delete()
        return redirect('resources:resource_list', slug=slug)
    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})