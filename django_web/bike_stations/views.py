from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from bike_stations.models import BikeLoc
from bike_stations.tables import BikeLocTable
from bike_stations.serializers import BikeLocSerializer

class BikeLocList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'get_BikeLoc.html'

    def get(self, request):
        queryset = BikeLoc.objects.all()
        # 필터를 사용할 경우, 결과가 없을 때 처리
        if queryset.count()==0:
            return render(request, '404_BikeLoc.html', status=status.HTTP_404_NOT_FOUND)

        table = BikeLocTable(queryset)
        RequestConfig(request, paginate={'per_page': 10}).configure(table)
        return Response({'table': table})