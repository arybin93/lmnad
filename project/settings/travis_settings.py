from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e^gzvyq8(f!5kg5o*(&a3!j(#0ky)80&8bd+_7i!i^7*3lbbno'

DEBUG = False
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'travis_ci_db',
        'USER': 'travis',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
