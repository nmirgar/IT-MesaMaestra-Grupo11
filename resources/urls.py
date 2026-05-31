from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('<slug:slug>/', views.resource_list, name='resource_list'),
    path('<slug:slug>/crear/', views.resource_create, name='resource_create'),
    path('<slug:slug>/detalle/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('<slug:slug>/detalle/<int:pk>/editar/', views.resource_update, name='resource_update'),
    path('<slug:slug>/detalle/<int:pk>/borrar/', views.resource_delete, name='resource_delete'),
]