import os
from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here')

JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='tu_clave_secreta')
JWT_ALGORITHM = config('JWT_ALGORITHM', default='HS256')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,ccd-automatically-sharon-marble.trycloudflare.com', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'core',  # Nuestra app principal
    'infrastructure',  # Para los modelos de persistencia
]

MIDDLEWARE = [
    'infrastructure.exception_handlers.middleware.GlobalExceptionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'infrastructure.middleware.clear_scope_middleware.ClearScopeMiddleware',
]

ROOT_URLCONF = 'goScanAPI_django.urls'

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

WSGI_APPLICATION = 'goScanAPI_django.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'money_plus_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Panama'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'infrastructure.middleware.custom_jwt_authentication_middleware.CustomJWTAuthenticationMiddleware',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'infrastructure.exception_handlers.drf_exception_handler.custom_exception_handler',
}

# Configuración de drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'GoScan API',
    'DESCRIPTION': 'API para el sistema GoScan con arquitectura hexagonal',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [{'BearerAuth': []}],
    'COMPONENTS': {
        'securitySchemes': {
            'BearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'Token JWT en formato: Bearer <token>'
            }
        }
    }
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:56633",
    "https://ccd-automatically-sharon-marble.trycloudflare.com",
    "https://sri-observed-derby-focuses.trycloudflare.com",
    "https://sri-observed-derby-focuses.trycloudflare.com",
    "https://handhelds-electoral-equation-affiliation.trycloudflare.com",
    "https://cod-governments-survey-ana.trycloudflare.com",
    "https://friendship-dry-limited-quoted.trycloudflare.com",
    "http://localhost:62448",
    "http://localhost:55250",
    "http://localhost:55250",
    "http://localhost:60312",
    "http://localhost:64179",
    "http://localhost:5000",
    "https://invision-researcher-broad-literary.trycloudflare.com",
    "http://localhost:8080",
    "https://scheduled-exploration-lb-entertaining.trycloudflare.com",
    "https://invision-researcher-broad-literary.trycloudflare.com",
]

# Configuración de migraciones personalizada
MIGRATION_MODULES = {
    'infrastructure': 'infrastructure.persistence.migrations',
}

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_TIMEZONE = 'America/Panama'

CELERY_BEAT_SCHEDULE = {
    'cleanup-expired-password-reset-codes': {
        'task': 'infrastructure.tasks.task.cleanup_expired_password_resets',
        'schedule': timedelta(seconds=10),
    },
}