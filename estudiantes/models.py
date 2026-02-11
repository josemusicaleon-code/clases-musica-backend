from django.db import models

class Estudiante(models.Model):
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miércoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sábado', 'Sábado'),
    ]
    
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('parcial', 'Parcial'),
        ('pagado', 'Pagado'),
    ]
    
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    monto_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dia_semana = models.CharField(max_length=20, choices=DIAS_SEMANA, default='lunes')
    hora_clase = models.TimeField(default='18:00')
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['nombre']
