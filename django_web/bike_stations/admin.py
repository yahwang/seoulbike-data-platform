from django.contrib import admin
from bike_stations.models import BikeLoc


@admin.register(BikeLoc)
class BikeLocAdmin(admin.ModelAdmin):
    pass