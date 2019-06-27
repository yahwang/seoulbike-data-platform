from django.contrib import admin
from django.urls import path, include

from dashboard.views import BikeDashboard

urlpatterns = [
    path('', BikeDashboard.as_view(), name="bike_dashboard"),
]
