from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'e^gzvyq8(f!5kg5o*(&a3!j(#0ky)80&8bd+_7i!i^7*3lbbno')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', False)
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1 188.120.248.147 lmnad.nntu.ru").split(" ")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'lmnad_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'root'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
