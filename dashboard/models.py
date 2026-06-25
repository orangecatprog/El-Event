from django.db import models

# Re-export EventModel so Django can auto-discover it for migrations.
from dashboard.events.infrastructure.eventModel import EventModel
