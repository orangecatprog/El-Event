from __future__ import annotations

from uuid import UUID

from django.contrib.auth import get_user_model

from dashboard.events.domain.event import Event
from dashboard.events.domain.eventStatus import EventStatus

from .eventModel import EventModel

UserModel = get_user_model()


class EventRepository:
    def save(self, event: Event) -> Event:
        model, _created = EventModel.objects.update_or_create(
            id=event.id,
            defaults={
                "title": event.title,
                "short_description": event.short_description,
                "detailed_description": event.detailed_description,
                "tags": event.tags,
                "likes": event.likes,
                "creator_id": event.creator_id,
                "starts_at": event.starts_at,
                "ends_at": event.ends_at,
                "location_address": event.location_address,
                "location_city": event.location_city,
                "status": event.status.value,
                "max_participants": event.max_participants,
            },
        )

        # Sync event participants through the M2M relationship.
        participant_ids = [int(participant_id) for participant_id in event.participants]
        participants = UserModel.objects.filter(id__in=participant_ids)
        model.participants.set(participants)

        return self._to_domain(model)

    def get_by_id(self, event_id: int) -> Event | None:
        model = EventModel.objects.prefetch_related("participants").filter(id=event_id).first()
        if model is None:
            return None
        return self._to_domain(model)

    def list_all(self) -> list[Event]:
        models = EventModel.objects.prefetch_related("participants").all().order_by("starts_at")
        return [self._to_domain(model) for model in models]
    
    def list_by_creator(self, creator_id: int) -> list[Event]:
        models = EventModel.objects.filter(creator_id=creator_id).all().order_by("starts_at")
        return [self._to_domain(model) for model in models]

    def list_by_participant(self, participant_id: int) -> list[Event]:
        models = EventModel.objects.prefetch_related("participants").filter(participants=participant_id).order_by("starts_at")
        return [self._to_domain(model) for model in models]

    def delete(self, event_id: int) -> bool:
        deleted_rows, _details = EventModel.objects.filter(id=event_id).delete()
        return deleted_rows > 0

    def _to_domain(self, model: EventModel) -> Event:
        return Event(
            id=model.id,
            title=model.title,
            short_description=model.short_description,
            detailed_description=model.detailed_description,
            tags=model.tags,
            creator_id=model.creator_id,
            likes=model.likes,
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            location_address=model.location_address,
            location_city=model.location_city,
            participants=list(model.participants.values_list("id", flat=True)),
            max_participants=model.max_participants,
            status=EventStatus(model.status),
        )
