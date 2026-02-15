#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=========================================="
echo "Iniciando build del backend Django"
echo "=========================================="

echo "Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo ""
echo "Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

echo ""
echo "Verificando superusuario..."
python manage.py shell << PYEOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

# Crear superusuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superusuario creado: admin/admin123')
else:
    print('✅ Superusuario ya existe')
PYEOF

echo ""
echo "=========================================="
echo "✅ Build completado exitosamente!"
echo "=========================================="
