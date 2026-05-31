from django.urls import path
from . import views

app_name = 'mm_sessions'

urlpatterns = [
    path('<slug:slug>/', views.session_list, name='session_list'),
    path('<slug:slug>/crear/', views.session_create, name='session_create'),
    path('<slug:slug>/detalle/<int:pk>/', views.session_detail, name='session_detail'),
    path('<slug:slug>/detalle/<int:pk>/editar/', views.session_update, name='session_update'),
    path('<slug:slug>/detalle/<int:pk>/borrar/', views.session_delete, name='session_delete'),
]