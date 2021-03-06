from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import RequestConfig
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_filters import rest_framework as filters
from django.core.exceptions import ObjectDoesNotExist
from .models import BikeLoc
from .tables import BikeLocTable
from .serializers import BikeLocSerializer
from .forms import BikeLocForm

class BikeLocFilter(filters.FilterSet):
    st_cradle_gte = filters.NumberFilter(field_name="st_cradle", lookup_expr='gte')
    st_cradle_lte = filters.NumberFilter(field_name="st_cradle", lookup_expr='lte')
    st_gu = filters.CharFilter(field_name="st_gu", lookup_expr='iexact')
    class Meta:
        model = BikeLoc
        fields = ('st_cradle_gte','st_cradle_lte', 'st_gu') # params와 일치해야 함
        # fields의 이름이 변수의 이름이 된다.

class BikeLocFilterBackend(filters.DjangoFilterBackend):
    pass

class BikeLocList(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'get_BikeLoc.html'
    filterset_class = BikeLocFilter
    #filterset_fields = ('st_gu','st_cradle')

    def get(self, request):
        queryset = BikeLoc.objects.all()
        
        filtered_queryset = BikeLocFilterBackend().filter_queryset(request, queryset, self)

        # 결과가 없을 때 처리
        if not filtered_queryset.exists():
            return render(request, '404_BikeLoc.html', status=status.HTTP_404_NOT_FOUND)
        
        table = BikeLocTable(filtered_queryset)
        RequestConfig(request, paginate={'per_page': 10}).configure(table)
        return Response({'rows':filtered_queryset.count(), 'table': table, 'filters': request.query_params})

class BikeLocEdit(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'edit_BikeLoc.html'

    def get(self, request, pk):
        bikeloc = get_object_or_404(BikeLoc, st_id=pk)
        form = BikeLocForm(instance=bikeloc)
        return Response({'form':form})
        
    def post(self, request, pk):
        bikeloc = get_object_or_404(BikeLoc, st_id=pk)
        form = BikeLocForm(request.POST or None, instance=bikeloc) # 여기서 수정된 내용 반영
        if form.is_valid():
            form.save()
            return redirect('st_list')

class BikeLocDelete(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, pk):
        bikeloc= get_object_or_404(BikeLoc, st_id=pk)    
        bikeloc.delete()
        return redirect('st_list')

class BikeLocCreate(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'create_BikeLoc.html'

    def get(self, request):
        form = BikeLocForm()
        return Response({'form':form})
    
    def post(self, request):
        form = BikeLocForm(request.POST or None)
        if form.is_valid(): # pk 존재여부 체크도 가능
            form.save()
            return redirect('st_list')
        else:
            return Response({'form':form})

