from django.contrib import admin
from django.urls import path, include

from bike_stations.views import BikeLocList, BikeLocEdit, BikeLocDelete, BikeLocCreate

urlpatterns = [
    path('', BikeLocList.as_view(), name="st_list"),
    path('edit/<int:pk>', BikeLocEdit.as_view(), name="st_list_edit"),
    path('delete/<int:pk>', BikeLocDelete.as_view(), name="st_list_delete"),
    path('create/', BikeLocCreate.as_view(), name="st_list_create"),
]
