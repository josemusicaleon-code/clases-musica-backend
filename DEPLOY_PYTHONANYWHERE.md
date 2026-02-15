# Deploy en PythonAnywhere

## Paso 1: Preparar el Código

Sube tu código a GitHub si no lo has hecho:
```bash
git add .
git commit -m "Ready for PythonAnywhere"
git push origin main
```

## Paso 2: Configurar PythonAnywhere

1. Ve a https://www.pythonanywhere.com
2. Crea una cuenta (hay plan gratuito)
3. Ve a la pestaña **Files** → **Upload a file** o clona desde GitHub

## Paso 3: Configurar Virtual Environment

En la pestaña **Consoles**, abre una Bash console y ejecuta:
```bash
mkvirtualenv --python=python3.11 venv
workon venv
pip install -r requirements.txt
```

## Paso 4: Configurar WSGI

En la pestaña **Web**, click en **Add a new web app**:
- Selecciona **Manual configuration**
- Selecciona **Python 3.11**
- Click en el archivo **WSGI configuration** link
- Reemplaza el contenido con:

```python
import os
import sys

# Añadir tu proyecto al path
path = '/home/TU_USUARIO/backend'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miapp.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Nota**: Cambia `TU_USUARIO` por tu username de PythonAnywhere y `backend` por el nombre de tu carpeta.

## Paso 5: Configurar Variables de Entorno

En la pestaña **Web**, busca **Environment variables** y agrega:
- `SECRET_KEY`: tu clave secreta
- `DEBUG`: `False`
- `DATABASE_URL`: tu URL de Supabase

## Paso 6: Ejecutar Migraciones

En la consola Bash:
```bash
workon venv
cd ~/backend
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Paso 7: Recargar la App

En la pestaña **Web**, click en el botón **Reload**

## URLs de tu API

- API: `https://TU_USUARIO.pythonanywhere.com/api/estudiantes/`
- Admin: `https://TU_USUARIO.pythonanywhere.com/admin/`

## Notas

- PythonAnywhere usa **MySQL** por defecto (no PostgreSQL)
- Si quieres usar Supabase (PostgreSQL), asegúrate de tener `psycopg2-binary` en requirements.txt (ya lo tienes)
- El dominio gratuito es `tu-usuario.pythonanywhere.com`
