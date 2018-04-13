from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email_unique(value):
    """
    helper function to ensure that user's email addresses are unique to those in the database
    :param value:
    :return:
    """
    exists = User.objects.filter(email__iexact=value)

    if exists:
        raise ValidationError('Someone is already using this email address. '
                              'Please try another.')


def validate_username_unique(value):
    """
    disallow any of the following usernames to exist
    :param value:
    :return:
    """
    exists = User.objects.filter(username__iexact=value)
    invalid_usernames = [
        'cerebro',
        'admin',
        'help',
        'helpdesk',
        'sales',
        'support',
        'info',
        'warning',
        'success',
        'danger',
        'error',
        'debug',
        'alert',
        'alerts',
        'signup',
        'signin',
        'signout',
        'login',
        'logout',
        'activate',
        'register',
        'password',
    ]

    if exists or value in invalid_usernames:
        raise ValidationError('This username is not available. '
                              'Please try another.')