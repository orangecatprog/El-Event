from django.urls import include, path

from dashboard.interfaces.event_detail import EventDetailView
from dashboard.interfaces.event_join import EventJoinView, EventLeaveView
from dashboard.interfaces.my_events.my_events import DashboardMyEventsView
from urls.pathfrom import path_from
from .interfaces.home import DashboardHomeView

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="dashboard-home"),
    path("e/<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("e/<int:pk>/join/", EventJoinView.as_view(), name="event-join"),
    path("e/<int:pk>/leave/", EventLeaveView.as_view(), name="event-leave"),
    path_from(include("dashboard.interfaces.my_events.urls")),
    path_from(include("dashboard.interfaces.discover.urls")),
    path_from(include("dashboard.interfaces.calendar.urls")),
]

BASE_URL = 'dashboard/'