from django.views.generic import DetailView
from dashboard.events.infrastructure.eventModel import EventModel
from dashboard.interfaces._base.view_mixin import ViewMixin

class EventDetailView(ViewMixin, DetailView):
    model = EventModel
    template_name = "dashboard/event_detail.html"
    context_object_name = "event"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            domain_event = self.get_service().get_event(self.object.id)
            context["is_participant"] = user.id in domain_event.participants if domain_event else False
            context["is_full"] = (
                domain_event.max_participants > 0
                and len(domain_event.participants) >= domain_event.max_participants
            ) if domain_event else False
        else:
            context["is_participant"] = False
            context["is_full"] = False
        return context