from django.views.generic import TemplateView

from dashboard.interfaces._event_creation.mixin import EventCreateModalMixin


class DashboardHomeView(EventCreateModalMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context["created_events"] = 0
            return context

        service = self.get_service()
        context["created_events"] = len(service.list_events_by_creator(self.request.user.id))
        context["most_popular_event"] = service.get_most_popular_event(self.request.user.id)
        return context
