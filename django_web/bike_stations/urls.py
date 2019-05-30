from django.contrib import admin
from django.urls import path, include

from bike_stations.views import BikeLocList

urlpatterns = [
    path('', BikeLocList.as_view(), name="st_list"),
]
