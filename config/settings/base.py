import environ
import json
import os

from datetime import timedelta

ROOT_DIR = environ.Path(__file__) - 3
BASE_DIR = ROOT_DIR
APPS_DIR = ROOT_DIR.path('apps')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.exceptions import ImproperlyConfigured

with open(ROOT_DIR("secrets.json")) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Definir la variable de ambiente {0}".format(setting)
        raise ImproperlyConfigured(error_msg)

ALLOWED_HOSTS = get_secret('DOMINIOS_PROPIOS')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
#LOGIN_REDIRECT_URL = 'usuarios:login'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
#LOGIN_URL = 'usuarios:login'

SECRET_KEY = get_secret('SECRET_KEY')
DEBUG = get_secret('DEBUG')

LANGUAGE_CODE = 'es'
SITE_ID = 1
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = False
USE_TZ = False

DATE_INPUT_FORMATS = ["%Y-%m-%d",]
DATETIME_FORMAT = "Y-m-d h:i a"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
}


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': get_secret('DATABASE_DEFAULT'),
}

#DATABASE_ROUTERS = (
#    'django_tenants.routers.TenantSyncRouter',
#)

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
#ROOT_URLCONF = 'config.urls'
ROOT_URLCONF = 'config.urls'
#PUBLIC_SCHEMA_URLCONF = 'config.public_urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]
THIRD_PARTY_APPS = [
    'bootstrap4',
    'rest_framework',
    'django_extensions',
    'rest_framework_simplejwt',
]
LOCAL_APPS = [
    'apps.users',
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS +LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('../staticfiles'))

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
    str(APPS_DIR.path('media')),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

USE_S3 = get_secret('USE_S3')
AWS_ACCESS_KEY_ID=get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=get_secret('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME=get_secret('AWS_STORAGE_BUCKET_NAME')

if USE_S3:
    # config aws
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = str(APPS_DIR('media'))

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR.path('templates')), ],
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


# DJANGO ALLAUTH
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # These are provider-specific settings that can only be
        # listed here:
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    }
}

SOCIALACCOUNT_ADAPTER = 'apps.usuarios.adapter.MySocialAccountAdapter'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_LOGOUT_ON_GET = True

# VARIABLES DE CONFIGURACION DE LA APLICACION
USUARIO_INICIAL = get_secret('USUARIO_INICIAL')
ACTIVAR_ENVIO_CORREOS = get_secret('ACTIVAR_ENVIO_CORREOS')
EXTENSIONES_VALIDAS_CARGUE_ARCHIVOS = get_secret('EXTENSIONES_VALIDAS_CARGUE_ARCHIVOS')
DJANGO_EASY_AUDIT_REMOTE_ADDR_HEADER = get_secret('DJANGO_EASY_AUDIT_REMOTE_ADDR_HEADER')

EMAIL_CONFIG = get_secret("EMAIL_CONFIG")

EMAIL_BACKEND = EMAIL_CONFIG["EMAIL_BACKEND"]
EMAIL_HOST = EMAIL_CONFIG["EMAIL_HOST"]
EMAIL_HOST_USER = EMAIL_CONFIG["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = EMAIL_CONFIG["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = EMAIL_CONFIG["EMAIL_PORT"]
EMAIL_USE_TLS = EMAIL_CONFIG["EMAIL_USE_TLS"]
DEFAULT_FROM_EMAIL = EMAIL_CONFIG["DEFAULT_FROM_EMAIL"]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'