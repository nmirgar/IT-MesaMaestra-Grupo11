from django.db import models
from campaigns.models import Campaign


class MmSession(models.Model):

    class Status(models.TextChoices):
        PLANNED = 'PLANNED', 'Planificada'
        PLAYED = 'PLAYED', 'Jugada'
        CANCELLED = 'CANCELLED', 'Cancelada'

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name='Campaña',
    )
    title = models.CharField('Título', max_length=200)
    summary = models.TextField('Resumen', blank=True)
    scheduled_at = models.DateTimeField('Fecha programada', null=True, blank=True)
    estimated_duration = models.PositiveIntegerField(
        'Duración estimada (minutos)', null=True, blank=True
    )
    status = models.CharField(
        'Estado', max_length=20, choices=Status.choices, default=Status.PLANNED
    )
    fictional_location = models.CharField('Localización ficticia', max_length=200, blank=True)
    director_notes = models.TextField('Notas del director', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
        ordering = ['scheduled_at', 'created_at']

    def __str__(self):
        return f'{self.campaign.title} — {self.title}'