import csv
from datetime import datetime
import logging
import datetime
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
    def getCurrencyData(cls, currency, user='', timespan=''):
        """
        pull currency data from the database about the specified currency
        :param user:
        :param timespan: daterange from which we are pulling from the database
        :param currency: currency that we are gathering data for
        :return:
        """
        # Alter currency value based on User's currency default
        # pull all data from the database
        # TODO add volume
        data = Coin.objects.all().filter(cryptocurrency__name=currency).values('price', 'time')
        # update time field to unix time, multiply by 10,000 to get time 'accuracy' to mS
        # update price field to always be a float variable
        for object in data:
            unixTime = int(object['time'].timestamp()) * 10000
            object['time'] = unixTime
            object['price'] = float(object['price'])
        # convert the queryset to a list of dictionaries
        data = [item for item in data]
        # time, price inverted
        return [[row[key] for key in ['time', 'price']] for row in data]

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
