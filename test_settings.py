from testapp.settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testapp_test.db',
    }
}

DEBUG = True
CELERY_ALWAYS_EAGER = True

DEFAULT_SITE_PORT = 8000

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',

    'taggit',
    'modelcluster',

    'testapp',
    'molo.core',
    'molo.profiles',
    'mote',
    'google_analytics',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtailmedia',
    'wagtail.contrib.wagtailsitemaps',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',

    'mptt',
    'djcelery',
    'molo.polls',

    'raven.contrib.django.raven_compat',
    'django_cas_ng',
    'compressor',
]
