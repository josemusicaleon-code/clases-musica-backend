"""
Django settings for miapp project.
DIAGNÓSTICO: Versión con hardcode y prints masivos
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# ========== DIAGNÓSTICO INICIAL ==========
print("🚨🚨🚨 INICIANDO SETTINGS.PY - MODO DIAGNÓSTICO 🚨🚨🚨")
print(f"🔧 DEBUG raw: '{os.getenv('DEBUG')}'")
print(f"🔧 ALLOWED_HOSTS raw: '{os.getenv('ALLOWED_HOSTS')}'")
print(f"🔧 SECRET_KEY existe: {bool(os.getenv('SECRET_KEY'))}")
print(f"🔧 DATABASE_URL existe: {bool(os.getenv('DATABASE_URL'))}")
sys.stdout.flush()
# ==========================================

# SECRET KEY - Hardcode temporal para diagnóstico
SECRET_KEY = 'django-insecure-diagnostico-1234567890-temporal-no-usar-en-produccion'
# ⚠️ COMENTADO: SECRET_KEY = os.getenv('SECRET_KEY')
# if not SECRET_KEY:
#     raise ValueError("❌ SECRET_KEY no está configurada")

# DEBUG - Forzado a True
DEBUG = True
# ⚠️ COMENTADO: DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS - HARCODEADO como ['*']
ALLOWED_HOSTS = ['*']  # <-- TEMPORAL PARA DIAGNÓSTICO
print(f"🔧 ALLOWED_HOSTS final: {ALLOWED_HOSTS}")
sys.stdout.flush()
# ⚠️ COMENTADO: ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
# ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]
# if not ALLOWED_HOSTS:
#     ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'estudiantes',
    'pagos',
    'clases',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'miapp.urls'
WSGI_APPLICATION = 'miapp.wsgi.application'

# Database - Solo SQLite para diagnóstico
print("🔧 Usando SQLite para diagnóstico")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# ⚠️ COMENTADO: Toda la lógica de PostgreSQL/DATABASE_URL
# if os.getenv('DATABASE_URL'):
#     DATABASES = {
#         'default': dj_database_url.config(
#             default=os.getenv('DATABASE_URL'),
#             conn_max_age=600,
#             ssl_require=True,
#         )
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS - Máxima apertura para diagnóstico
CORS_ALLOW_ALL_ORIGINS = True  # <-- TEMPORAL
CORS_ALLOW_CREDENTIALS = True
# ⚠️ COMENTADO: CORS_ALLOWED_ORIGINS y toda su lógica

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}

# ========== SEGURIDAD COMPLETAMENTE DESHABILITADA ==========
# TODO EL BLOQUE DE PRODUCCIÓN COMENTADO
# if not DEBUG:
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_HSTS_SECONDS = 0
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = False
#     SECURE_HSTS_PRELOAD = False
#     CSRF_TRUSTED_ORIGINS = []
# ==========================================================

print("🚨🚨🚨 SETTINGS.PY CARGADO COMPLETAMENTE 🚨🚨🚨")
sys.stdout.flush()