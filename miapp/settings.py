"""
Django settings for miapp project.
Configuración definitiva para producción con Supabase
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# ========== SEGURIDAD ==========
# SECRET_KEY con valor por defecto para producción (NO DEPENDE DE ENV VAR)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-produccion-definitiva-2026')

# DEBUG forzado a False en producción (se puede override por env var)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS - Acepta cualquier host en producción (ajustable por env var)
ALLOWED_HOSTS = ['clases-musica-backend.onrender.com', '.render.com', 'joseLeonLanau.pythonanywhere.com', '.pythonanywhere.com']
# Si quieres restringir, usa: ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

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

# ========== BASE DE DATOS - SUPABASE ==========
# SOLO usa DATABASE_URL. NADA más.
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Fallback a SQLite para desarrollo local sin Supabase
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

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
    "https://clases-musica-backend.onrender.com",
    "https://joseLeonLanau.pythonanywhere.com",
    "https://clases-musica-frontend.vercel.app",
]

if os.getenv('CORS_ALLOWED_ORIGINS'):
    extra = os.getenv('CORS_ALLOWED_ORIGINS')
    if extra:
        extra_origins = extra.split(',')
        CORS_ALLOWED_ORIGINS.extend([o.strip() for o in extra_origins if o.strip()])

CORS_ALLOW_CREDENTIALS = True

# Cookie settings para producción
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 semana
SESSION_COOKIE_NAME = 'sessionid'
CSRF_COOKIE_NAME = 'csrftoken'

# ========== REST FRAMEWORK ==========
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Token authentication
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append('rest_framework.authentication.TokenAuthentication')

# ========== SEGURIDAD PRODUCCIÓN ==========
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = False
    
    # Cookie settings para cross-origin
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # SameSite=None para permitir cookies en cross-origin requests
    SESSION_COOKIE_SAMESITE = 'None'
    CSRF_COOKIE_SAMESITE = 'None'
    
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    
    # CSRF Trusted Origins
    CSRF_TRUSTED_ORIGINS = [
        'https://clases-musica-frontend.vercel.app',
        'https://joseleonlanau.pythonanywhere.com',
    ]