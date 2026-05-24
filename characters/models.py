from django.db import models
from django.conf import settings
from campaigns.models import Campaign

class Character(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name="Nombre"
    )
    character_class = models.CharField(
        max_length=50, 
        verbose_name="Clase"
    )
    race = models.CharField(
        max_length=50, 
        verbose_name="Raza"
    )
    level = models.PositiveIntegerField(
        default=1, 
        verbose_name="Nivel"
    )
    background = models.TextField(
        blank=True, 
        verbose_name="Trasfondo"
    )
    hit_points = models.PositiveIntegerField(
        default=10, 
        verbose_name="Puntos de Golpe (HP)"
    )
    avatar = models.ImageField(
        upload_to="characters/avatars/", 
        blank=True, 
        null=True, 
        verbose_name="Avatar"
    )
    
    # Relaciones principales
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="characters",
        verbose_name="Propietario"
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.SET_NULL,  # Si se borra la campaña, el personaje no se borra, solo se desvincula
        null=True,
        blank=True,
        related_name="characters",
        verbose_name="Campaña"
    )
    
    # Trazabilidad
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última actualización"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Personaje"
        verbose_name_plural = "Personajes"

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

