from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dandy',
        'USER': 'dandy',
        'PASSWORD': 'dandy',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
