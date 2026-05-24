from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from campaigns.models import Campaign
from .models import MmSession
from .forms import MmSessionForm


def session_list(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    sessions = campaign.sessions.all()
    return render(request, 'mm_sessions/session_list.html', {
        'campaign': campaign,
        'sessions': sessions,
    })


def session_detail(request, slug, pk):
    session = get_object_or_404(MmSession, pk=pk, campaign__slug=slug)
    return render(request, 'mm_sessions/session_detail.html', {'session': session})

@login_required
def session_create(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    if campaign.director != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = MmSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.campaign = campaign
            session.save()
            return redirect('mm_sessions:session_list', slug=slug)  # cambia esto
    else:
        form = MmSessionForm()
    return render(request, 'mm_sessions/session_form.html', {
        'form': form, 'campaign': campaign, 'action': 'Crear'
    })

@login_required
def session_update(request, slug, pk):
    session = get_object_or_404(MmSession, pk=pk, campaign__slug=slug)
    if session.campaign.director != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = MmSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('mm_sessions:session_detail', slug=slug, pk=session.pk)
    else:
        form = MmSessionForm(instance=session)
    return render(request, 'mm_sessions/session_form.html', {
        'form': form, 'campaign': session.campaign, 'action': 'Editar'
    })


@login_required
def session_delete(request, slug, pk):
    session = get_object_or_404(MmSession, pk=pk, campaign__slug=slug)
    if session.campaign.director != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        session.delete()
        return redirect('mm_sessions:session_list', slug=slug)
    return render(request, 'mm_sessions/session_confirm_delete.html', {'session': session})