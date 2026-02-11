from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from .models import Pago
from .serializers import PagoSerializer
from estudiantes.models import Estudiante

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        mes_actual = timezone.now().month
        
        ingresos_mes = Pago.objects.filter(
            fecha_pago__month=mes_actual,
            estado='completo'
        ).aggregate(total=Sum('monto_pagado'))['total'] or 0
        
        pagos_pendientes = Pago.objects.filter(
            estado__in=['pendiente', 'parcial']
        ).count()
        
        pagos_vencidos = Pago.objects.filter(
            estado__in=['pendiente', 'parcial'],
            fecha_vencimiento__lt=timezone.now().date()
        ).count()
        
        return Response({
            'ingresos_mes': float(ingresos_mes),
            'pagos_pendientes': pagos_pendientes,
            'pagos_vencidos': pagos_vencidos,
            'total_estudiantes': Estudiante.objects.filter(activo=True).count()
        })
