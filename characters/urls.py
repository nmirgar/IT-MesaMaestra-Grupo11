from django.urls import path
from . import views

app_name = "characters"

urlpatterns = [
    path('', views.CharacterListView.as_view(), name='list'),
    path('crear/', views.CharacterCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CharacterDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.CharacterUpdateView.as_view(), name='update'),
    path('<int:pk>/borrar/', views.CharacterDeleteView.as_view(), name='delete'),
    path('campania/<slug:campaign_slug>/', views.CampaignCharacterListView.as_view(), name='campaign_list'),
]