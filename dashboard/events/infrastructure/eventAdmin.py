from django.contrib import admin
from .eventModel import EventModel

@admin.register(EventModel)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "starts_at", "ends_at", "location_address", "location_city", "status", "max_participants")
    list_filter = ("status",)
    search_fields = ("title", "short_description", "detailed_description")
    ordering = ("starts_at",)
    filter_horizontal = ("participants",)
