# ============================================
# DEPLOY EN SUPABASE + RENDER - GUÍA COMPLETA
# ============================================

## RESUMEN
Esta guía te llevará paso a paso para desplegar el backend de Django en Supabase (PostgreSQL) 
y Render (hosting), conectado a tu frontend en Vercel/Netlify.

## PARTE 1: SUPABASE (Base de Datos)

### 1.1 Crear Proyecto en Supabase
1. Ve a https://supabase.com y crea una cuenta o inicia sesión
2. Click en "New Project"
3. Selecciona tu organización
4. Configura:
   - **Name**: clases-musica-db
   - **Database Password**: [Genera una contraseña segura y GUÁRDALA]
   - **Region**: Selecciona la más cercana a ti (ej: East US)
5. Click en "Create new project"
6. Espera ~2 minutos a que se cree

### 1.2 Obtener DATABASE_URL
1. En el dashboard de Supabase, ve a: **Project Settings** (icono de engranaje) → **Database**
2. Sección "Connection string"
3. Selecciona **URI** del menú desplegable
4. Verás algo como:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxxxxxxxxx.supabase.co:5432/postgres
   ```
5. Reemplaza `[YOUR-PASSWORD]` con tu contraseña real
6. **COPIA ESTA URL COMPLETA** - la necesitarás para Render

### 1.3 Configurar Pool de Conexiones (OPCIONAL PERO RECOMENDADO)
1. En el dashboard de Supabase → **Database** → **Connection Pooling**
2. Asegúrate de que esté habilitado
3. El puerto del pool es usualmente **6543** (diferente del 5432)
4. Si usas el pool, tu URL sería:
   ```
   postgresql://postgres:[PASSWORD]@db.xxxxxxxxxxxxxxxxxxxx.supabase.co:6543/postgres?pgbouncer=true
   ```

---

## PARTE 2: RENDER (Hosting Backend)

### 2.1 Preparar el Repositorio
Asegúrate de que estos archivos estén en tu repo:
- `requirements.txt` ✅ (ya existe)
- `runtime.txt` (crear - ver abajo)
- `build.sh` (crear - ver abajo)
- `.env.example` ✅ (ya existe)
- Todo el código del backend

### 2.2 Crear runtime.txt
```bash
echo "python-3.11.6" > runtime.txt
```

### 2.3 Crear build.sh (Script de Build)
Crea un archivo `build.sh` en la raíz del backend:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "Ejecutando migraciones..."
python manage.py migrate

echo "Creando superusuario si no existe..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('Superusuario ya existe')
EOF

echo "Build completado!"
```

Hazlo ejecutable:
```bash
chmod +x build.sh
```

### 2.4 Subir a GitHub
1. Crea un repositorio en GitHub
2. Sube tu código del backend:
```bash
cd C:\Users\123\Documents\PROYECTOS DE APPs\backend
git init
git add .
git commit -m "Initial commit - ready for deploy"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/clases-musica-backend.git
git push -u origin main
```

### 2.5 Crear Web Service en Render
1. Ve a https://render.com
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Name**: clases-musica-backend
   - **Region**: Ohio (o la más cercana)
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn miapp.wsgi:application`
5. En "Environment Variables", agrega:
   - `SECRET_KEY`: [Genera una clave larga y aleatoria]
   - `DEBUG`: `False`
   - `DATABASE_URL`: [La URL de Supabase del paso 1.2]
6. Click en "Create Web Service"
7. Espera ~5 minutos a que se despliegue

### 2.6 Obtener URL del Backend
1. Una vez desplegado, Render te dará una URL como:
   ```
   https://clases-musica-backend.onrender.com
   ```
2. **GUARDA ESTA URL** - la necesitarás para el frontend

---

## PARTE 3: FRONTEND (Vercel/Netlify)

### 3.1 Actualizar Variables de Entorno del Frontend
En tu proyecto de frontend, crea/actualiza el archivo `.env.production`:

```bash
VITE_API_URL=https://clases-musica-backend.onrender.com/api
```

### 3.2 Actualizar CORS en Backend (settings.py)
Agrega tu dominio de frontend a `CORS_ALLOWED_ORIGINS`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://clases-musica-backend.onrender.com",
    "https://tu-frontend.vercel.app",  # Tu URL de Vercel
]
```

Haz commit y push de este cambio a GitHub - Render se redeplegará automáticamente.

### 3.3 Deploy del Frontend
1. Sube tu frontend a GitHub
2. Importa el repo en Vercel/Netlify
3. Configura la variable de entorno `VITE_API_URL` con la URL de tu backend
4. Deploy!

---

## PARTE 4: VERIFICAR QUE TODO FUNCIONA

### 4.1 Probar API Endpoints
Abre en tu navegador:
- `https://clases-musica-backend.onrender.com/api/estudiantes/` (debe mostrar JSON vacío `[]`)
- `https://clases-musica-backend.onrender.com/admin/` (panel de admin)

### 4.2 Verificar Base de Datos
1. Ve a Supabase Dashboard → Table Editor
2. Deberías ver las tablas:
   - estudiantes_estudiante
   - pagos_pago
   - clases_clase
   - django_migrations
   - auth_user

### 4.3 Probar desde el Frontend
1. Abre tu frontend desplegado
2. Intenta crear un estudiante
3. Debería aparecer en la base de datos de Supabase

---

## PARTE 5: SOLUCIÓN DE PROBLEMAS

### Error: "No module named 'psycopg2'"
**Solución**: Ya está en requirements.txt, pero si persiste:
```bash
pip install psycopg2-binary
```

### Error: "connection refused" o "timeout"
**Causa**: Problema de conexión con Supabase
**Solución**:
1. Verifica que DATABASE_URL esté correcta
2. Asegúrate de que la contraseña no tenga caracteres especiales sin codificar
3. Intenta usar el puerto del pool (6543) en lugar de 5432

### Error: "relation does not exist"
**Causa**: Las migraciones no se ejecutaron
**Solución**:
1. Ve a Render Dashboard → Shell
2. Ejecuta: `python manage.py migrate`

### Error CORS
**Solución**: Agrega tu dominio de frontend a `CORS_ALLOWED_ORIGINS` en settings.py

### Las tablas no se ven en Supabase
**Verificación**:
1. Ve a Supabase → Table Editor
2. Si no ves tablas, las migraciones fallaron
3. Ve a Render Logs y busca errores

---

## COMANDOS ÚTILES

### Ejecutar migraciones manualmente en Render
```bash
# En Render Dashboard, ve a tu servicio → Shell
python manage.py migrate
```

### Crear superusuario manualmente
```bash
python manage.py createsuperuser
```

### Ver logs en Render
1. Ve a Render Dashboard
2. Selecciona tu web service
3. Click en "Logs"

### Hacer backup de la base de datos
```bash
# Desde tu máquina local con pg_dump
pg_dump $DATABASE_URL > backup.sql
```

---

## CHECKLIST FINAL ✅

Antes de decir que está listo, verifica:

- [ ] Proyecto creado en Supabase
- [ ] DATABASE_URL copiada correctamente
- [ ] Repositorio en GitHub con todo el código
- [ ] runtime.txt creado
- [ ] build.sh creado y ejecutable
- [ ] Web Service creado en Render
- [ ] Variables de entorno configuradas en Render
- [ ] Deploy exitoso en Render (sin errores en logs)
- [ ] API responde correctamente (prueba en navegador)
- [ ] Tablas visibles en Supabase Table Editor
- [ ] Frontend conectado al backend correcto
- [ ] CORS configurado para tu dominio frontend
- [ ] Crear estudiante desde frontend funciona
- [ ] Datos aparecen en Supabase

---

## URLs IMPORTANTES

- Supabase Dashboard: https://app.supabase.com
- Render Dashboard: https://dashboard.render.com
- Backend: https://clases-musica-backend.onrender.com
- Admin Django: https://clases-musica-backend.onrender.com/admin
- API: https://clases-musica-backend.onrender.com/api/

---

¿Problemas? Revisa los logs en Render y Supabase. La mayoría de errores son:
1. DATABASE_URL incorrecta
2. Migraciones no ejecutadas
3. CORS no configurado
4. Variables de entorno faltantes
