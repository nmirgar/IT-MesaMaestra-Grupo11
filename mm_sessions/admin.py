from django.contrib import admin
from .models import MmSession


@admin.register(MmSession)
class MmSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'campaign', 'status', 'scheduled_at')
    list_filter = ('status', 'campaign')
    search_fields = ('title', 'campaign__title')