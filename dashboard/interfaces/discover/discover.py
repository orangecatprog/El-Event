from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from dashboard.interfaces._base.view_mixin import ViewMixin


class DashboardDiscoverView(ViewMixin, TemplateView):
    template_name = "dashboard/discover.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            context["event_cards"] = []
            return context

        service = self.get_service()
        events = service.discover_events(self.request.user.id, tags=None)

        user_ids: set[int] = set()
        for event in events:
            if event.creator_id is not None:
                user_ids.add(event.creator_id)
            user_ids.update(event.participants)

        user_model = get_user_model()
        usernames_by_id = {
            user.id: user.username
            for user in user_model.objects.filter(id__in=user_ids).only("id", "username")
        }

        context["event_cards"] = [
            {
                "event": event,
                "creator_username": usernames_by_id.get(event.creator_id, "Unknown"),
                "participant_usernames": [
                    usernames_by_id.get(participant_id, f"User #{participant_id}")
                    for participant_id in event.participants
                ],
            }
            for event in events
        ]

        return context