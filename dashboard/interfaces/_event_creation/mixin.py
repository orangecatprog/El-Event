from __future__ import annotations

from django.contrib import messages

from dashboard.events.domain.eventStatus import EventStatus
from dashboard.events.infrastructure.eventRepository import EventRepository
from dashboard.events.service.eventService import EventService
from dashboard.interfaces._base.view_mixin import ViewMixin
from .form import EventCreateForm


class EventCreateModalMixin(ViewMixin):
    form_class = EventCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("create_event_form", kwargs.get("create_event_form", self.form_class()))
        context.setdefault("open_create_event_modal", kwargs.get("open_create_event_modal", False))
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            creator_id = request.user.id if request.user.is_authenticated else None
            cleaned = form.cleaned_data
            self.service.create_event(
                title=cleaned["title"],
                short_description=cleaned["short_description"],
                detailed_description=cleaned["detailed_description"],
                tags=cleaned["tags"],
                creator_id=creator_id,
                starts_at=cleaned["starts_at"],
                ends_at=cleaned["ends_at"],
                location_address=cleaned["location_address"],
                location_city=cleaned["location_city"],
                max_participants=cleaned.get("max_participants") or 0,
            )
            messages.success(request, "Event created successfully.")
            return self.get(request, *args, **kwargs)

        messages.error(request, "Please fix the form errors.")
        context = self.get_context_data(create_event_form=form, open_create_event_modal=True)
        return self.render_to_response(context)
