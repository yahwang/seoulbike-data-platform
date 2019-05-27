import django_tables2 as tables
from .models import BikeLoc

class BikeLocTable(tables.Table):
    class Meta:
        model = BikeLoc
        template_name = 'django_tables2/table.html'
        attrs={'class':'highlight centered'}
