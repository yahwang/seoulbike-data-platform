from django.shortcuts import render
from bike_stations.models import BikeLoc
from bike_stations.tables import BikeLocTable
from django_tables2 import RequestConfig

# Create your views here.
def show_bike_locs(request):
    table = BikeLocTable(BikeLoc.objects.all())
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(request, 'show_bike_locs.html',{'table':table})

