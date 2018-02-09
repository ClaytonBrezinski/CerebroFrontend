import csv
from datetime import datetime
import logging

from django.conf import settings
# TODO add email capabilities
# from django.core.mail import EmailMessage

from .models import Cryptocurrency, Coin
# from sentiment.models import sentimentResults
logger = logging.getLogger(__name__)

DATE_FORMAT = '%Y/%m/%d'
FILENAME_DATE_FORMAT = '%b%d%Y'
TIME_FORMAT = '%I:%M %p'


class ChartData(object):

    @classmethod
    def getCurrencyData(cls, user, timespan, currency):
        """
        pull currency data from the database about the specified currency
        :param user:
        :param timespan: daterange from which we are pulling from the database
        :param currency: currency that we are gathering data for
        :return:
        """
        # Alter currency value based on User's currency default
        # pull all data from the database
        curencyData = Coin.objects.all().filter(cryptocurrency=currency)

        # TODO add volume in the future
        data = {'dates': [],
                'values': []}
        data['values'].append(curencyData)

    # TODO create a getCurrencySentimentData class
    @classmethod
    def getCurrencySentimentData(cls, timespan, currency):
        """
        pull sentiment data from the databse about the specified curency
        :param timespan: daterange from which we are pulling from the database
        :param currency: currency that we are gathering data for
        :return:
        """

        now = datetime.now(tz=user.settings.time_zone).date()
        # sentimentData = Sentiment.objects.all().filter(name=currency)
        data = {'dates': [], 'sentiment': []}
