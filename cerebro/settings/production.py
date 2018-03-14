import dj_database_url

from .base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Use the cached template loader so template is compiled once and read from
# memory instead of reading from disk on each load.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.herokuapp.com']

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cerebro',
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': 'cerebro',
        'PORT': '',
    }
}

# 3rd-party apps tracking IDs.
INTERCOM_APP_ID = 'a6d0326564469dfd7f7d9b1bfc909ee3815a85a8'
GOOGLE_ANALYTICS_TRACKING_ID = 'UA-45698014-1'
ADDTHIS_PUBLISHER_ID = 'ra-52fffdf9456ec7d2'

# The 'From:' header of admin-related emails.
DEFAULT_FROM_EMAIL = 'info@cerebro.net'

ADMINS = (
    ('Local Admin', 'admin@cerebro.net'),
)

MANAGERS = ADMINS

CONTACTS = {
    'support_email': 'GlucoseTracker.net <support@cerebro.net>',
    'admin_email': 'admin@cerebro.net',
    'info_email': 'GlucoseTracker.net <info@cerebro.net>',
}

# Subscribers app settings
SEND_SUBSCRIBERS_EMAIL_CONFIRMATION = True

#whitenoise staticfile storage
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Django-storages settings
#DEFAULT_FILE_STORAGE = 'core.s3utils.MediaRootS3BotoStorage'

# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = 'cerebro-assets'
# AWS_QUERYSTRING_AUTH = False
#
# MEDIA_URL = '//%s.s3.amazonaws.com/%s/' % (AWS_STORAGE_BUCKET_NAME, MEDIA_ROOT)

# Parse database configuration from $DATABASE_URL
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

# set max connection time to the database to 10 mins
db_from_env = dj_database_url.config(conn_max_age=600)