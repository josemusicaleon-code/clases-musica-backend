from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from django.utils import timezone
from .models import Pago
from .serializers import PagoSerializer
from estudiantes.models import Estudiante

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        from datetime import datetime
        
        mes_actual = timezone.now().month
        anio_actual = timezone.now().year
        
        # Ingresos del mes actual (pagos donde monto_pagado > 0)
        ingresos_mes = Pago.objects.filter(
            fecha__month=mes_actual,
            fecha__year=anio_actual,
            monto_pagado__gt=0
        ).aggregate(total=Sum('monto_pagado'))['total'] or 0
        
        # Pagos pendientes (donde saldo_pendiente > 0)
        pagos_pendientes = Pago.objects.filter(
            monto_pagado__lt=models.F('monto')
        ).count()
        
        # Calcular saldo total pendiente
        pagos_con_saldo = Pago.objects.filter(monto_pagado__lt=models.F('monto'))
        saldo_pendiente_total = sum(p.saldo_pendiente for p in pagos_con_saldo)
        
        # Estudiantes con pagos pendientes
        estudiantes_con_deuda = Estudiante.objects.filter(
            pagos__monto_pagado__lt=models.F('pagos__monto')
        ).distinct().count()
        
        return Response({
            'ingresos_mes': float(ingresos_mes),
            'pagos_pendientes': pagos_pendientes,
            'saldo_pendiente_total': float(saldo_pendiente_total),
            'estudiantes_con_deuda': estudiantes_con_deuda,
            'total_estudiantes': Estudiante.objects.filter(activo=True).count(),
            'total_pagos_registrados': Pago.objects.count(),
            'pagos_recientes': PagoSerializer(
                Pago.objects.order_by('-created_at')[:5], many=True
            ).data
        })
