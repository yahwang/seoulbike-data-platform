from rest_framework.serializers import ModelSerializer
from bike_stations.models import BikeLoc

# serializers class converts python objects to Json

class BikeLocSerializer(ModelSerializer):
    class Meta:
        model = BikeLoc
        fields = "__all__"