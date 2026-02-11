from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from estudiantes.views import EstudianteViewSet
from pagos.views import PagoViewSet
from clases.views import ClaseViewSet

# Crear router principal
router = DefaultRouter()

# Registrar en español (lo que ya tienes)
router.register(r'estudiantes', EstudianteViewSet, basename='estudiante')
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'clases', ClaseViewSet, basename='clase')

# También registrar en inglés
router.register(r'students', EstudianteViewSet, basename='student')
router.register(r'payments', PagoViewSet, basename='payment')
router.register(r'classes', ClaseViewSet, basename='class')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]