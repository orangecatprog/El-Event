from dataclasses import dataclass, field
from datetime import datetime 
from .eventStatus import EventStatus

@dataclass
class Event:    
    # Text
    title: str
    short_description: str
    detailed_description: str
    tags: list[str]
    creator_id: int | None
    likes: int

    # Datetime
    starts_at: datetime
    ends_at: datetime

    # Location
    location_address: str
    location_city: str

    # Participants
    max_participants: int = 0
    participants: list[int] = field(default_factory=list)

    status: EventStatus = EventStatus.DRAFT
    id: int | None = None

