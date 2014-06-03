"""
Django settings for philhealth project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

SECRET_KEY = '-9v4^s0ft4^l_d_*lj%t9!=fjv0chek($ip30ungc-+%=i9j*)'
DEBUG = True
TEMPLATE_DEBUG = True


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH   = os.path.join(BASE_DIR, 'static')
MEDIA_PATH = os.path.join(BASE_DIR, 'media')

MEDIA_ROOT = MEDIA_PATH
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

STATICFILES_DIRS = (
    STATIC_PATH,
)

STATIC_URL = '/static/'

LOGIN_URL = 'django.contrib.auth.views.login'
LOGIN_REDIRECT_URL = '/'


ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'tickets',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'philhealth.urls'

WSGI_APPLICATION = 'philhealth.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'philhealth',
        'USER': 'postgres',
        'PASSWORD': '1',
        'HOST': 'localhost'
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Hong_Kong'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
