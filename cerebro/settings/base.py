import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Regina'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Run management command 'set_site_values to set these values
SITE_NAME = 'Cerebro.net'
SITE_DOMAIN = 'www.Cerebro.net'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# # Absolute filesystem path to the directory that will hold user-uploaded files.
# # Example: "/var/www/example.com/media/"
# MEDIA_ROOT = 'media'
#
# # URL that handles the media served from MEDIA_ROOT. Make sure to use a
# # trailing slash.
# # Examples: "http://example.com/media/", "http://media.example.com/"
# MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles/')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
    ]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    ]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
            ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                # Used by Grappelli
                'django.template.context_processors.request',

                # 3rd-party context processors
                'stickymessages.context_processors.latest_sticky_message',

                # cerebro context processors
                'core.context_processors.third_party_tracking_ids',
                'core.context_processors.site_info',
                ]
            ,
            'loaders': [
                # Template loaders
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # TODO remove depricated file here
                # depricated 'django.template.loaders.eggs.Loader',
                ],
            },
        }
    ]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # for heroku static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ]

ROOT_URLCONF = 'cerebro.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'cerebro.wsgi.application'

INSTALLED_APPS = [
    # Grappelli custom admin, needs to be defined before the admin app.
    'grappelli',
    # whitenoise needs to be run before  'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    # 3rd-party apps
    'axes',
    'compressor',
    'crispy_forms',
    'gunicorn',
    'redactor',
    'stickymessages',
    'taggit',
    'storages',
    'django_tables2',

    # Local apps
    'accounts',
    'blogs',
    'core',
    'glucoses',
    'subscribers',
    'coins',
    'socialMedia',
    ]

# Django-crispy-forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django-axes settings
AXES_LOGIN_FAILURE_LIMIT = 100

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Session cookie expiration in seconds
SESSION_COOKIE_AGE = 7776000

# SMTP settings
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s  [%(name)s:%(lineno)s]  %(levelname)s - %(message)s',
            },
        'simple': {
            'format': '%(levelname)s %(message)s',
            },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
            }
        },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            }
        },
    'loggers': {
        # Silence SuspiciousOperation.DisallowedHost exception ('Invalid
        # HTTP_HOST' header messages). Set the handler to 'null' so we don't
        # get those annoying emails.
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
            },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        '': {
            'handlers': ['console', ],
            'level': 'INFO',
            }
        }
    }

# Grappelli settings.
GRAPPELLI_ADMIN_TITLE = SITE_NAME

# Django WYSIWYG Redactor settings.
REDACTOR_OPTIONS = {
    'lang': 'en',
    'buttonSource': 'true',
    'toolbarFixed': 'true',
    }
REDACTOR_UPLOAD = 'editor-uploads/'

# MailChimp settings.
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
MAILCHIMP_LIST_ID = os.getenv('MAILCHIMP_LIST_ID')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
AXES_CACHE = 'axes_cache'