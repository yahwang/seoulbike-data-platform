from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

class BikeDashboard(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'dashboard.html'

    def get(self, request):
        return Response({'a':'b'})