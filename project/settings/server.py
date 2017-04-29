from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e^gzvyq8(f!5kg5o*(&a3!j(#0ky)80&8bd+_7i!i^7*3lbbno'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '188.120.248.147',
    'lmnad.nntu.ru'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lmnad_db',
        'USER': 'root',
        'PASSWORD': '17ff0b32da',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, '../locale'),
)


