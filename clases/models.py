from django.db import models
from estudiantes.models import Estudiante

class Clase(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='clases')
    fecha = models.DateTimeField()
    duracion = models.IntegerField(help_text="Duración en minutos")
    observaciones = models.TextField(blank=True)
    completada = models.BooleanField(default=True)
    tema = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Clase {self.id} - {self.estudiante.nombre}"

    class Meta:
        ordering = ['-fecha']