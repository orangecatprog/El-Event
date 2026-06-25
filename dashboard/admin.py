from django.contrib import admin

# Register your models here.
from .events.infrastructure.eventModel import EventModel

admin.site.register(EventModel)