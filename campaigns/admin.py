from django.contrib import admin

from .models import Campaign, Participation, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 0


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "director",
        "game_system",
        "status",
        "visibility",
        "created_at",
    ]
    list_filter = [
        "status",
        "visibility",
        "game_system",
        "tags",
        "created_at",
    ]
    search_fields = [
        "title",
        "description",
        "game_system",
    ]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    inlines = [ParticipationInline]


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "campaign",
        "role",
        "status",
        "joined_at",
    ]
    list_filter = [
        "role",
        "status",
        "joined_at",
    ]
    search_fields = [
        "user__username",
        "campaign__title",
    ]