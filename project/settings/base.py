# -*- coding: utf-8 -*-
import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
PREREQ_APPS = [
    'suit',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
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
    'formsetfield'
]

PROJECT_APPS = [
    'lmnad',
    'igwatlas',
    'igwcoeffs',
    'tank',
    'publications',
    'phenomenon_db'
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'request_logging.middleware.LoggingMiddleware',
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
    os.path.join(BASE_DIR, '../locale/'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

FAVICON_PATH = STATIC_URL + 'lmnad/favicon.ico'

MARKDOWN_EDITOR_SKIN = 'simple'

SUIT_CONFIG = {
    'ADMIN_NAME': 'Админ панель',
    'LIST_PER_PAGE': 15,
    'SEARCH_URL': '',
    'MENU': (
        {
            'label': 'Настройки',
            'models': [
                {'label': 'Основные настройки', 'url': '/admin/constance/config/'},
                {'label': 'Редактирование страниц', 'url': 'lmnad.page'},
                {'label': 'Персональные страницы', 'url': 'lmnad.account'}
            ]
        },
        {'app': 'lmnad', 'label': 'Основные разделы',
            'models': [
                'event',
                'seminar',
                'protection',
                'people',
                'grant',
                'project',
                'UsefulLink'
            ]},
        {'app': 'publications', 'label': 'Менеджер публикаций', 'models': [
            'publication',
            'conference',
            'author',
            'journal'
        ]},
        {'app': 'tank', 'label': 'Эксперименты', 'models': [
            'experiment',
        ]},
        {'app': 'igwcoeffs', 'label': 'IGW Калькулятор', 'models': [
            'calculation',
        ]},
        {'app': 'igwatlas', 'label': 'IGW Atlas', 'models': [
            'record',
            'source',
            'file',
            'pageData',
            'waveData'
        ]},
        {'app': 'phenomenon_db', 'label': 'Сахалин', 'models': [
            'SeaPhenomenon',
        ]},
        {'app': 'lmnad', 'label': 'Wiki', 'models': [
            'wiki',
        ]},
        {'app': 'auth', 'label': 'Пользователи', 'icon': 'icon-lock'}
    )
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'FEEDBACK_EMAIL': ('lmnad@nntu.ru', 'email для обратной связи', str),
    'LIST_EMAILS': ('arybin93@gmail.com', 'Список для рассылки', str),
    'API_KEY_IGWATLAS': ('d837d31970deb03ee35c416c5a66be1bba9f56d3', 'Ключ для доступа к API IGWAtlas', str)
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'lmnad@nntu.ru')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'test')

SERVICE_EMAIL = 'lmnad@nntu.ru'
SERVER_EMAIL = 'lmnad@nntu.ru'
ADMINS = [('Admin', 'arybin93@gmail.com')]

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/profile/{}/".format(u.username),
}

CKEDITOR_UPLOAD_PATH = "uploads/users/photo"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            {'name': 'yourcustomtools', 'items': [
                'Preview',
                'Maximize',
            ]}
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': 60*60*24,
    }
}

# Set the cache backend to select2
SELECT2_CACHE_BACKEND = 'default'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s: %(module)s: %(funcName)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
        'request': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}/log/request.log'.format(BASE_DIR),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 10
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['request', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

if not os.path.exists('{}/log/request.log'.format(BASE_DIR)):
    del LOGGING['handlers']['request']
    del LOGGING['loggers']['django.request']

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

YANDEX_TRANSLATE_API_KEY = os.getenv('YANDEX_TRANSLATE_API_KEY', 'base')
GEOPOSITION_GOOGLE_MAPS_API_KEY = os.getenv('GEOPOSITION_GOOGLE_MAPS_API_KEY', 'base')

DATA_UPLOAD_MAX_MEMORY_SIZE = 12621440
FILE_UPLOAD_PERMISSIONS = 0o644
