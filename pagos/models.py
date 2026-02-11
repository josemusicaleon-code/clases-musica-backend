from django.db import models
from estudiantes.models import Estudiante

class Pago(models.Model):
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateField()
    metodo = models.CharField(max_length=20, choices=METODOS_PAGO, default='efectivo')
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def saldo_pendiente(self):
        return self.monto - self.monto_pagado
    
    def __str__(self):
        return f"Pago {self.id} - {self.estudiante.nombre}"
    
    class Meta:
        ordering = ['-fecha']
