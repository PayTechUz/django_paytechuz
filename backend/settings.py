"""
Django settings for backend project.
"""
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8$&(5lx7=3d+!eed7_jryrw0zqjpthtqo*3lig6yz!t-idpw8*'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'paytechuz.integrations.django',
    'apps.shop',
    'apps.payment',
]

PAYTECHUZ = {
    'PAYME': {
        'PAYME_ID': env.str('PAYME_ID'),
        'PAYME_KEY': env.str('PAYME_KEY'),
        'ACCOUNT_MODEL': 'apps.payment.models.Invoice',
        'ACCOUNT_FIELD': 'id',
        'AMOUNT_FIELD': 'amount',
        'ONE_TIME_PAYMENT': True,
        'IS_TEST_MODE': True,
    },
    'CLICK': {
        'SERVICE_ID': env.str('CLICK_SERVICE_ID'),
        'MERCHANT_ID': env.str('CLICK_MERCHANT_ID'),
        'MERCHANT_USER_ID': env.str('CLICK_MERCHANT_USER_ID'),
        'SECRET_KEY': env.str('CLICK_SECRET_KEY'),
        'ACCOUNT_MODEL': 'apps.payment.models.Invoice',
        'COMMISSION_PERCENT': 0.0,
        'IS_TEST_MODE': True,
    },
    'ATMOS': {
        'CONSUMER_KEY': env.str('ATMOS_CONSUMER_KEY'),
        'CONSUMER_SECRET': env.str('ATMOS_CONSUMER_SECRET'),
        'STORE_ID': env.str('ATMOS_STORE_ID'),
        'TERMINAL_ID': env.str('ATMOS_TERMINAL_ID', default=''),
        'API_KEY': env.str('ATMOS_API_KEY'),
        'IS_TEST_MODE': env.bool('ATMOS_TEST_MODE', default=True),
        'ACCOUNT_MODEL': 'apps.payment.models.Invoice',
        'ACCOUNT_FIELD': 'id',
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
