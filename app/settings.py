"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from pathlib import Path

import environ
from ocpp.v16.enums import Action

from app.fields import ConnectionStatus

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

env = environ.Env()
environ.Env.read_env('./.env')

SECRET_KEY = env('SECRET_KEY', default=None)

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

INTERNAL_IPS = env.list(
    'INTERNAL_IPS',
    default=[
        '127.0.0.1',
    ],
)

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'corsheaders',
    'debug_toolbar',
    'djangoql',
    'manager',
]

if not DEBUG:
    INSTALLED_APPS.remove('debug_toolbar')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

if not DEBUG:
    MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')

X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS',
    default=[
        'http://localhost:8000',
        'http://127.0.0.1:8000',
    ],
)
CSRF_TRUSTED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS',
    default=[
        'http://localhost:8000',
        'http://127.0.0.1:8000',
    ],
)

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'
LANGUAGES = [
    ('ru', '🇷🇺 Русский'),
    ('en', '🇺🇸 English'),
]

LANGUAGE_CODE = 'ru-ru'

USE_I18N = True

USE_L10N = True

LOCALE_PATHS = [BASE_DIR / 'locale']
for path in LOCALE_PATHS:
    path.mkdir(parents=True, exist_ok=True)

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S %Z'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('DATABASE_HOST', default='postgres'),
        'PORT': env.int('DATABASE_PORT', default=5432),
        'CONN_MAX_AGE': env.int('DATABASE_CONN_MAX_AGE', default=30),
        'NAME': env('DATABASE_NAME', default='postgres'),
        'USER': env('DATABASE_USER', default='postgres'),
        'PASSWORD': env('DATABASE_PASSWORD', default='postgres'),
        'OPTIONS': {
            'sslmode': env('DATABASE_SSL_MODE', default='prefer'),
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/


TIME_ZONE = 'UTC'

USE_TZ = True

MEDIA_URL = 'media/'
MEDIA_ROOT = Path(BASE_DIR) / 'media'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = Path(BASE_DIR) / 'static'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

# Telegram bot settings
RABBITMQ_PORT = env.int('RABBITMQ_PORT', default=5672)
RABBITMQ_UI_PORT = env.int('RABBITMQ_UI_PORT', default=15672)
RABBITMQ_USER = env('RABBITMQ_USER', default='guest')
RABBITMQ_PASS = env('RABBITMQ_PASS', default='guest')
RABBITMQ_HOST = env('RABBITMQ_HOST', default='rabbitmq')

EVENTS_EXCHANGE_NAME = env('EVENTS_EXCHANGE_NAME', default='events')
TASKS_EXCHANGE_NAME = env('TASKS_EXCHANGE_NAME', default='tasks')

MAX_MESSAGE_PRIORITY = 10
REGULAR_MESSAGE_PRIORITY = 5
LOW_MESSAGE_PRIORITY = 1

WS_SERVER_PORT = env.int('WS_SERVER_PORT', default=8001)

HTTP_SERVER_HOST = env('HTTP_SERVER_HOST', default='http://localhost')
HTTP_SERVER_PORT = env.int('HTTP_SERVER_PORT', default=8000)

ALLOWED_SERVER_SENT_EVENTS = [
    ConnectionStatus.LOST_CONNECTION,
    Action.Heartbeat,
    Action.StatusNotification,
    Action.StartTransaction,
    Action.StopTransaction,
]

LOCK_FOLDER = '/tmp/lock'

OCPP_VERSION = env('OCPP_VERSION', default='1.6')
