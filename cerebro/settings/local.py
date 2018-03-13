from .base import *


DEBUG = True

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', 'https://lit-spire-51893.herokuapp.com/']

# Make this unique, and don't share it with anybody.
SECRET_KEY = '79&vz)($@07na+25vw4nb0r^p*6w0j+-x!m)y5p#76tp!gvs_5'

# 3rd-party apps tracking IDs.
INTERCOM_APP_ID = None
GOOGLE_ANALYTICS_TRACKING_ID = None
ADDTHIS_PUBLISHER_ID = None

ADMINS = (
    ('Local Admin', 'admin@cerebro.net'),
    )

MANAGERS = ADMINS

CONTACTS = {
    'support_email': 'support@cerebro.net',
    'admin_email': 'admin@cerebro.net',
    'info_email': 'info@cerebro.net',
    }

# For 'subscribers' app
SEND_SUBSCRIBERS_EMAIL_CONFIRMATION = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cerebro',
        'USER': 'cerebro',
        'PASSWORD': 'password',
        'HOST': os.getenv('POSTGRESQL_HOST', 'localhost'),
        'PORT': '',
        }
    }

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Django-debug-toolbar config
INSTALLED_APPS += ['debug_toolbar', ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
    'HIDE_DJANGO_SQL': False,
    }
