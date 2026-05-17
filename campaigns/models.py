from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nombre"
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        blank=True,
        verbose_name="Slug"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    class Status(models.TextChoices):
        PREPARING = "PREPARING", "Preparando"
        ACTIVE = "ACTIVE", "Activa"
        FINISHED = "FINISHED", "Finalizada"

    class Visibility(models.TextChoices):
        PUBLIC = "PUBLIC", "Pública"
        PRIVATE = "PRIVATE", "Privada"

    title = models.CharField(
        max_length=150,
        verbose_name="Título"
    )
    slug = models.SlugField(
        max_length=170,
        unique=True,
        blank=True,
        verbose_name="Slug"
    )
    description = models.TextField(
        verbose_name="Descripción"
    )
    game_system = models.CharField(
        max_length=100,
        verbose_name="Sistema de juego"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PREPARING,
        verbose_name="Estado"
    )
    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
        verbose_name="Visibilidad"
    )
    cover = models.ImageField(
        upload_to="campaigns/covers/",
        blank=True,
        null=True,
        verbose_name="Imagen de portada"
    )
    director = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="directed_campaigns",
        verbose_name="Director/a"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="campaigns",
        verbose_name="Etiquetas"
    )
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
        verbose_name = "Campaña"
        verbose_name_plural = "Campañas"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Campaign.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("campaigns:detail", args=[self.slug])

    def __str__(self):
        return self.title


class Participation(models.Model):
    class Role(models.TextChoices):
        DIRECTOR = "DIRECTOR", "Director"
        PLAYER = "PLAYER", "Jugador"
        SPECTATOR = "SPECTATOR", "Espectador"

    class Status(models.TextChoices):
        INVITED = "INVITED", "Invitado"
        ACCEPTED = "ACCEPTED", "Aceptado"
        REJECTED = "REJECTED", "Rechazado"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaign_participations",
        verbose_name="Usuario"
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="participations",
        verbose_name="Campaña"
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PLAYER,
        verbose_name="Rol"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACCEPTED,
        verbose_name="Estado"
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de unión"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "campaign"],
                name="unique_user_campaign_participation"
            )
        ]
        verbose_name = "Participación"
        verbose_name_plural = "Participaciones"

    def __str__(self):
        return f"{self.user.username} en {self.campaign.title} ({self.role})"