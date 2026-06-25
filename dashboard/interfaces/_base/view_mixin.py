from dashboard.events.infrastructure.eventRepository import EventRepository
from dashboard.events.service.eventService import EventService

class ViewMixin():
    service = EventService(EventRepository())

    get_service = lambda self: self.service