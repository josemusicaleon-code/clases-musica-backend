"""
Django settings for miapp project.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# ========== SEGURIDAD ==========
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY no está configurada en variables de entorno")

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ========== APLICACIONES ==========
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

# ========== BASE DE DATOS ==========
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ========== VALIDACIÓN CONTRASEÑAS ==========
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========== INTERNACIONALIZACIÓN ==========
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ========== ARCHIVOS ESTÁTICOS Y MEDIA ==========
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========== CORS ==========
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if os.getenv('CORS_ALLOWED_ORIGINS'):
    extra = os.getenv('CORS_ALLOWED_ORIGINS').split(',')
    CORS_ALLOWED_ORIGINS.extend([o.strip() for o in extra if o.strip()])

CORS_ALLOW_CREDENTIALS = True

# ========== REST FRAMEWORK ==========
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}

# ========== SEGURIDAD PRODUCCIÓN (COMENTADO PARA DIAGNÓSTICO) ==========
# if not DEBUG:
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_HSTS_SECONDS = 0
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = False
#     SECURE_HSTS_PRELOAD = False
#     
#     CSRF_TRUSTED_ORIGINS = [
#         o.strip() for o in CORS_ALLOWED_ORIGINS 
#         if o.strip().startswith(('http://', 'https://'))
#     ]