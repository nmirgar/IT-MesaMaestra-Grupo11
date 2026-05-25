from django.db import models
from django.conf import settings
from campaigns.models import Campaign


class Resource(models.Model):

    class ResourceType(models.TextChoices):
        MAP = 'MAP', 'Mapa'
        IMAGE = 'IMAGE', 'Imagen'
        LINK = 'LINK', 'Enlace'
        DOCUMENT = 'DOCUMENT', 'Documento'
        NOTE = 'NOTE', 'Nota'

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='resources',
        verbose_name='Campaña',
    )
    title = models.CharField('Título', max_length=200)
    resource_type = models.CharField(
        'Tipo', max_length=20, choices=ResourceType.choices, default=ResourceType.NOTE
    )
    description = models.TextField('Descripción', blank=True)
    file = models.FileField('Archivo', upload_to='resources/', blank=True, null=True)
    external_url = models.URLField('URL externa', blank=True)
    visible_to_players = models.BooleanField('Visible para jugadores', default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resources',
        verbose_name='Creado por',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.campaign.title})'