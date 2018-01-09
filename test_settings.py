from testapp.settings import *  # noqa
from os.path import abspath, dirname, join

PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testapp_test.db',
    }
}

DEBUG = True
CELERY_ALWAYS_EAGER = True

DEFAULT_SITE_PORT = 8000

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(PROJECT_ROOT, 'testapp', 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'molo.core.context_processors.locale',
                'wagtail.contrib.settings.context_processors.settings',
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "mote.loaders.app_directories.Loader",
                "django.template.loaders.app_directories.Loader",
            ]
        },
    },
]
