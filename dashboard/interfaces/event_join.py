from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from dashboard.interfaces._base.view_mixin import ViewMixin


class EventJoinView(ViewMixin, View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to join an event.")
            return redirect(reverse("event-detail", args=[pk]))

        try:
            self.get_service().join_event(pk, request.user.id)
            messages.success(request, "You have joined the event.")
        except ValueError as e:
            messages.error(request, str(e))

        return redirect(reverse("event-detail", args=[pk]))


class EventLeaveView(ViewMixin, View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to leave an event.")
            return redirect(reverse("event-detail", args=[pk]))

        self.get_service().leave_event(pk, request.user.id)
        messages.success(request, "You have left the event.")

        return redirect(reverse("event-detail", args=[pk]))
