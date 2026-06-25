from calendar import Calendar
from collections import defaultdict
from datetime import date

from django.views.generic import TemplateView

from dashboard.interfaces._base.view_mixin import ViewMixin


class DashboardCalendarView(ViewMixin, TemplateView):
    template_name = "dashboard/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()
        year = today.year
        month = today.month

        events_by_date = defaultdict(list)

        if self.request.user.is_authenticated:
            service = self.get_service()
            created = service.list_events_by_creator(self.request.user.id)
            joined = service.list_events_by_participant(self.request.user.id)

            seen = set()
            for event in created + joined:
                if event.id not in seen:
                    seen.add(event.id)
                    events_by_date[event.starts_at.date()].append(event)

        calendar_weeks = []

        cal = Calendar(firstweekday=0)  # lunes

        for week in cal.monthdatescalendar(year, month):
            calendar_weeks.append([
                {
                    "date": day,
                    "is_current_month": day.month == month,
                    "is_today": day == today,
                    "events": events_by_date.get(day, []),
                }
                for day in week
            ])

        context.update({
            "year": year,
            "month": month,
            "weeks": calendar_weeks,
        })

        return context