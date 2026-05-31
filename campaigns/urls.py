from django.urls import path

from . import views

app_name = "campaigns"

urlpatterns = [
    path("", views.CampaignListView.as_view(), name="list"),
    path("crear/", views.CampaignCreateView.as_view(), name="create"),
    path("<slug:slug>/", views.CampaignDetailView.as_view(), name="detail"),
    path("<slug:slug>/editar/", views.CampaignUpdateView.as_view(), name="update"),
    path("<slug:slug>/borrar/", views.CampaignDeleteView.as_view(), name="delete"),
]