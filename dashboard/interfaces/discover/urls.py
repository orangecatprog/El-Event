from django.contrib import admin
from django.urls import path

from .discover import DashboardDiscoverView

urlpatterns = [
    path("", DashboardDiscoverView.as_view(), name="dashboard-discover"),
]

BASE_URL = 'discover/'