from __future__ import annotations

from datetime import datetime

from dashboard.events.domain.event import Event
from dashboard.events.domain.eventStatus import EventStatus
from dashboard.events.infrastructure.eventRepository import EventRepository


class EventService:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    def create_event(
        self,
        *,
        title: str,
        short_description: str,
        detailed_description: str,
        tags: list[str],
        creator_id: int | None,
        starts_at: datetime,
        ends_at: datetime,
        location_address: str,
        location_city: str,
        max_participants: int = 0,
    ) -> Event:
        if ends_at <= starts_at:
            raise ValueError("ends_at must be greater than starts_at")

        event = Event(
            title=title,
            short_description=short_description,
            detailed_description=detailed_description,
            tags=tags,
            likes=0,
            creator_id=creator_id,
            starts_at=starts_at,
            ends_at=ends_at,
            location_address=location_address,
            location_city=location_city,
            max_participants=max_participants,
            participants=[],
            status=EventStatus.PUBLISHED,
        )
        return self._repository.save(event)

    def join_event(self, event_id: int, user_id: int) -> Event:
        event = self._require_event(event_id)

        if user_id in event.participants:
            return event

        if event.max_participants > 0 and len(event.participants) >= event.max_participants:
            raise ValueError("Event is full")

        event.participants.append(user_id)
        return self._repository.save(event)

    def leave_event(self, event_id: int, user_id: int) -> Event:
        event = self._require_event(event_id)

        if user_id in event.participants:
            event.participants.remove(user_id)

        return self._repository.save(event)

    def get_event(self, event_id: int) -> Event | None:
        return self._repository.get_by_id(event_id)

    def list_events(self) -> list[Event]:
        return self._repository.list_all()

    def list_events_by_creator(self, creator_id: int) -> list[Event]:
        return self._repository.list_by_creator(creator_id)

    def list_events_by_participant(self, participant_id: int) -> list[Event]:
        return self._repository.list_by_participant(participant_id)

    def _require_event(self, event_id: int) -> Event:
        event = self._repository.get_by_id(event_id)
        if event is None:
            raise ValueError(f"Event {event_id} not found")
        return event

    def discover_events(self, user_id: int | None, tags: list[str] | None) -> list[Event]:
        events = self._repository.list_all()

        events = filter(lambda e: e.status == EventStatus.PUBLISHED, events)
        events = filter(lambda e: tags is None or any(tag in e.tags for tag in tags), events)
        events = filter(lambda e: user_id is None or e.creator_id != user_id, events)

        events = list(events)
        events.sort(key=lambda e: e.likes, reverse=True)

        return events
    
    def get_most_popular_event(self, user_id: int | None) -> Event | None:
        events = self.discover_events(user_id, None)
        if not events:
            return None

        return max(events, key=lambda e: len(e.participants))
