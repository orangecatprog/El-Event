from django.contrib import admin
from django.urls import path

from .calendar import DashboardCalendarView

urlpatterns = [
    path("", DashboardCalendarView.as_view(), name="dashboard-calendar"),
]

BASE_URL = 'calendar/'