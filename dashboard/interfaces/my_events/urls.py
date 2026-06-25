from django.contrib import admin
from django.urls import path

from .my_events import DashboardMyEventsView

urlpatterns = [
    path("", DashboardMyEventsView.as_view(), name="dashboard-my-events"),
]

BASE_URL = 'my-events/'