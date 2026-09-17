"""
Django settings for localfix_backend project.
"""

from pathlib import Path
from datetime import timedelta
import os
import dj_database_url
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-development-key-change-this'
)

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'


# Render automatically provides RENDER_EXTERNAL_HOSTNAME.
render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

if render_host:
    ALLOWED_HOSTS.append(render_host)


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'accounts',
    'services',
    'bookings',
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise serves static files in production
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'localfix_backend.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'localfix_backend.wsgi.application'


# =========================================================
# DATABASE
# =========================================================

# Production: Render PostgreSQL
# Local development: MySQL

if os.environ.get('DATABASE_URL'):

    DATABASES = {
        'default': dj_database_url.parse(
            os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get(
                'MYSQL_DATABASE',
                'localfix_db'
            ),
            'USER': os.environ.get(
                'MYSQL_USER',
                'root'
            ),
            'PASSWORD': os.environ.get(
                'MYSQL_PASSWORD',
                ''
            ),
            'HOST': os.environ.get(
                'MYSQL_HOST',
                'localhost'
            ),
            'PORT': os.environ.get(
                'MYSQL_PORT',
                '3306'
            ),
        }
    }


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND':
            'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


# =========================================================
# EMAIL
# =========================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# =========================================================
# CUSTOM USER
# =========================================================

AUTH_USER_MODEL = 'accounts.User'


# =========================================================
# REST FRAMEWORK
# =========================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# =========================================================
# JWT
# =========================================================

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


# =========================================================
# CORS
# =========================================================

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
]

frontend_url = os.environ.get('FRONTEND_URL')

if frontend_url:
    CORS_ALLOWED_ORIGINS.append(frontend_url)


# =========================================================
# CSRF
# =========================================================

CSRF_TRUSTED_ORIGINS = []

if frontend_url:
    CSRF_TRUSTED_ORIGINS.append(frontend_url)


# =========================================================
# PRODUCTION SECURITY
# =========================================================

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https'
    )

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True