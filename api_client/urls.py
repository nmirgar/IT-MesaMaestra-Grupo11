from django.urls import path
from . import views

app_name = "api_client"

urlpatterns = [
    path("", views.bestiario, name="bestiario"),
    path("<path:slug>/", views.detalle_criatura, name="detalle_criatura"),
]
