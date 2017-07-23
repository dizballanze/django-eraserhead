# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import os

import django

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ")n(4b0hp!ne#q7jb@w8$kpk9jd8$=fk34@$0a-(-ro2dty2+0&"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "bar",
]

ERASERHEAD_ENABLED = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
        },
    },
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()

if 'RUNSERVER' in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "eraserhead.db3",
        }
    }

    INSTALLED_APPS += ("eraserhead.apps.EraserheadConfig",)
    ERASERHEAD_TRACEBACK_BASE_PATH = os.path.join(BASE_DIR, 'bar')
