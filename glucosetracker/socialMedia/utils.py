from datetime import datetime
from django.db import models
from django.utils import timezone
from settings.base import TIME_ZONE

now_aware = timezone.now()

DATE_FORMAT = '%Y/%m/%d'
TIME_FORMAT = '%I:%M %p'


def datetimeToTimeAgo(inDatetime):
    """
    takes the input datetime variable and outputs the # of mins, hours, days ago that the entry was made
    :param inDatetime:
    :return: dictionary: {timeParameter: , value: }
    example: for 2 days = {timeParameter: 'day', value: 2}
             for 5 hours = {timeParameter: 'hour', value: 5}
    """
    if isinstance(inDatetime, datetime):
        today = datetime.now(timezone.get_current_timezone())
        datetimedelta = today - inDatetime

        # if > 24 hours: use days to 1 day precision
        if datetimedelta.days > 0:
            return {'timeParameter': 'day',
                    'value': int(datetimedelta.days)}

        # > 60 mins < 24 hours: use hours to 1 hour precision
        elif datetimedelta.days < 1 and datetimedelta.seconds > 3600:
            return {'timeParameter': 'hour',
                    'value': int(datetimedelta.seconds / 3600)}

        # if < 60 mins: use minutes to 5 minute precision
        elif datetimedelta.days < 1 and datetimedelta.seconds < 3600:
            return {'timeParameter': 'minute',
                    'value': (int(datetimedelta.seconds / 60) % 60)}


def timeAgoToString(inTimeAgo):
    """
    output a properly formatted string for the datetimeToTimeAgo function
    :param inTimeAgo:
    :return:
    """
    if inTimeAgo['value'] == 1:
        return str(inTimeAgo['value']) + ' ' + inTimeAgo['timeParameter'] + ' ago'
    else:
        return str(inTimeAgo['value']) + ' ' + inTimeAgo['timeParameter'] + 's ago'
