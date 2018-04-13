import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserSettings

logger = logging.getLogger(__name__)

# Signals are a built-in django functionality that allow for system wide listening for specific actions

@receiver(signal=post_save, sender=User)
def create_usersettings_on_user_create(sender, instance, created, **kwargs):
    """
    Automatically create a UserSettings object when a new user is created.
    """

    if created:
        UserSettings.objects.get_or_create(user=instance)
