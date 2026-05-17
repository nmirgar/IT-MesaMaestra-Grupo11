from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cuenta creada correctamente. Has iniciado sesión.")
            return redirect("campaigns:list")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})