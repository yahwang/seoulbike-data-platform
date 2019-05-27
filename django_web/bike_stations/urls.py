from django.contrib import admin
from django.urls import path, include

from bike_stations.views import show_bike_locs

urlpatterns = [
    path('', show_bike_locs),
]
