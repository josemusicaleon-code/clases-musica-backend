from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from .models import Clase
from .serializers import ClaseSerializer

class ClaseViewSet(viewsets.ModelViewSet):
    queryset = Clase.objects.all().order_by('-fecha')
    serializer_class = ClaseSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['fecha', 'created_at']