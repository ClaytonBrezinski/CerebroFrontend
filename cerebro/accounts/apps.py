from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from .signals import create_usersettings_on_user_create


class ProfilesConfig(AppConfig):
    name = 'accounts'
    verbose_name = _('accounts')

    def ready(self):
        post_save.connect(create_usersettings_on_user_create, sender=User)
