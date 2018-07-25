# -*- coding: utf-8 -*-
import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
PREREQ_APPS = [
    'suit',
    'modeltranslation',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'suit_redactor',
    'suit_ckeditor',
    'favicon',
    'django_forms_bootstrap',
    'constance',
    'constance.backends.database',
    'ckeditor',
    'ckeditor_uploader',
    'geoposition',
    'django_select2',
    'daterange_filter',
]

PROJECT_APPS = [
   'lmnad',
   'igwatlas',
   'igwcoeffs',
   'tank',
   'publications'
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
    'django.middleware.locale.LocaleMiddleware',
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
                "django.contrib.messages.context_processors.messages"
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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

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
                {'label': u'Редактирование страниц', 'url': 'lmnad.page'},
                #{'label': u'Файловый менеджер', 'url': '/admin/filebrowser/browse/'},
                {'label': u'Персональные страницы', 'url': 'lmnad.account'}
            ]
        },
        {'app': 'lmnad', 'label': u'Основные разделы',
            'models': [
                'event',
                'seminar',
                'protection',
                'people',
                'grant',
                'project',
        ]},
        {'app': 'publications', 'label': u'Менеджер публикаций', 'models': [
            'publication',
            'author',
            'journal',
            'lmnad.article',
        ]},
        {'app': 'tank', 'label': u'Эксперименты', 'models': [
            'experiment',
        ]},
        {'app': 'igwcoeffs', 'label': u'IGW Калькулятор', 'models': [
            'calculation',
        ]},
        {'app': 'igwatlas', 'label': u'IGW Atlas', 'models': [
            'record',
            'source',
            'file',
            'pageData'
        ]},
        {'app': 'lmnad', 'label': u'Wiki', 'models': [
            'wiki',
        ]},
        {'app': 'auth', 'label': u'Пользователи', 'icon': 'icon-lock'}
    )
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'FEEDBACK_EMAIL': ('lmnad@nntu.ru', u'email для обратной связи', str),
    'LIST_EMAILS': ('arybin93@gmail.com', u'Список для рассылки', str),
    'API_KEY_IGWATLAS': ('d837d31970deb03ee35c416c5a66be1bba9f56d3', u'Ключ для доступа к API IGWAtlas', str)
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = 'lmnad@nntu.ru'
EMAIL_HOST_PASSWORD = '&62dmRJSLkrs'

SERVICE_EMAIL = 'lmnad@nntu.ru'
SERVER_EMAIL = 'lmnad@nntu.ru'
ADMINS = [('Admin', 'arybin93@gmail.com')]

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/profile/%s/" % u.username,
}

# file browser
FILEBROWSER_SUIT_TEMPLATE = True
FILEBROWSER_DIRECTORY = 'uploads/'
FILEBROWSER_MAX_UPLOAD_SIZE = 104857600

CKEDITOR_UPLOAD_PATH = "uploads/users/photo"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True

GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyCLumlxQ35v472UxtM0RupR3cXkxm4nW0I'


REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}