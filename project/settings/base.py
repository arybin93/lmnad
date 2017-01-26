# -*- coding: utf-8 -*-
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
PREREQ_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'suit_redactor',
    'suit_ckeditor',
    'favicon',
    'django_forms_bootstrap',
    'constance',
    'constance.backends.database',
    'ckeditor'
]

PROJECT_APPS = [
   'lmnad'
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

#LANGUAGE_CODE = 'en-us'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "../static/")

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = 'media/'

FAVICON_PATH = STATIC_URL + 'lmnad/favicon.ico'

MARKDOWN_EDITOR_SKIN = 'simple'

SUIT_CONFIG = {
    'ADMIN_NAME': 'Админ панель',
    'LIST_PER_PAGE': 15,
    'SEARCH_URL': '',
    'MENU': (
        {
            'label': u'Настройки',
            'models': [
                {'label': u'Основные настройки', 'url': '/admin/constance/config/'},
                {'label': u'Редактирование страниц', 'url': 'lmnad.page'}
            ]
        },
        {'app': 'lmnad', 'label': u'Основные разделы',
            'models': [
                'article',
                'event',
                'seminar',
                'protection',
                'people',
        ]},
        {'app': 'auth', 'label': u'Пользователи', 'icon': 'icon-lock'}
    )
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'FEEDBACK_EMAIL': ('lmnad@nntu.ru', u'email для обратной связи', str),
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = 'lmnad@nntu.ru'
EMAIL_HOST_PASSWORD = '&62dmRJSLkrs'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/profile/%s/" % u.username,
}