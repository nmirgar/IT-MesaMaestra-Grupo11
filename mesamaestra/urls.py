from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),

    path("accounts/", include("accounts.urls")),
    path("campanias/", include("campaigns.urls")),
    path("personajes/", include("characters.urls")),
    path("sesiones/", include("mm_sessions.urls")),
    path("recursos/", include("resources.urls")),
    path("bestiario/", include("api_client.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)