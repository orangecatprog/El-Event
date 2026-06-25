import uuid
from django.conf import settings
from django.db import models
from django.db.models import F, Q

class EventModel(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CANCELLED = "cancelled", "Cancelled"

    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    detailed_description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    likes = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_events",
        null=True,
        blank=True,
    )

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    location_address = models.CharField(max_length=255)
    location_city = models.CharField(max_length=255)

    status = models.CharField(max_length=255, choices=Status.choices, default=Status.DRAFT)

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="joined_events",
    )
    max_participants = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "events"
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_at__isnull=True) | Q(ends_at__gt=F("starts_at")),
                name="ends_after_starts",
            )
        ]
        verbose_name = "Event"
        verbose_name_plural = "Events"
