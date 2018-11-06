from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e^gzvyq8(f!5kg5o*(&a3!j(#0ky)80&8bd+_7i!i^7*3lbbno'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lmnad_db',
        'USER': 'dev',
        'PASSWORD': 'dev',
        'HOST': 'db',
        'PORT': '3306',
    }
}

