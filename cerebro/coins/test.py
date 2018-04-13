from django.test import TestCase
from .models import Cryptocurrency, Coin
from django.contrib.auth.models import User

# Datetime stuff
from django.utils.timezone import now

# REST API stuff
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token


class CryptocurrencyModelTestCase(TestCase):
    """
    This is a test suite for the Cryptocurrency model
    """

    def setUp(self, cryptocurrencyName='test', cryptocurrencyTickerSymbol='tst'):
        """
        Define variables for a basic cryptocurrency
        :return:
        """
        self.cryptocurrencyName = cryptocurrencyName
        self.cryptocurrencyTickerSymbol = cryptocurrencyTickerSymbol
        self.cryptocurrency = Cryptocurrency(name=self.cryptocurrencyName, tickerSymbol=self.cryptocurrencyTickerSymbol)

    def testCreateNewModel(self):
        """
        Creating a new cryptocurrency
        :return:
        """
        oldCount = Cryptocurrency.objects.count()
        # self.cryptocurrency.save()
        currency = Cryptocurrency.objects.create(Cryptocurrency='BTC', Price=1234, Volume=12, Time='')
        currency.save()
        newCount = Cryptocurrency.objects.count()
        self.assertNotEqual(oldCount, newCount)

    def testErrornousCreation(self):
        """
        Create cryptocurrencies with errornous data inputs
        :return:
        """
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.client.post({Name = '', tickerSymbol = 123456, Active = 'QQ'})


class CoinModelTestCase(TestCase):
    """
    This is a test suite for the Coins model
    """

    def setUp(self):
        """
        Define variables for a basic cryptocurrency, coin
        :return:
        """
        self.cryptocurrencyName = 'tester'
        self.cryptocurrencyTickerSymbol = 'test'
        self.cryptocurrency = Cryptocurrency(name=self.cryptocurrencyName, tickerSymbol=self.cryptocurrencyTickerSymbol)
        self.cryptocurrency.save()

        self.coinPrice = 5
        self.coinVolume = 5
        self.coinTime = now()
        self.coin = Coin(cryptocurrency=self.cryptocurrency, price=self.coinPrice, volume=self.coinVolume,
                         time=self.coinTime)

    def testCreateNewModel(self):
        """
        Creating a new Coin
        :return:
        """

        oldCount = Coin.objects.count()
        self.coin.save()
        newCount = Coin.objects.count()
        self.assertNotEqual(oldCount, newCount)

    def testErrornousCreation(self):
        """
        Create coins with errornous data inputs
        :return:
        """
        currency = Cryptocurrency.objects.create(Name='', tickerSymbol=123456, Active='QQ')
        self.assertFormError(self.post.currency)
        coin = Coin.objects.create(Cryptocurrency='', Price='qq', Volume='qq', Time='123')
        self.assertFormError(self.post.coin)


class CryptoCurrencyViewTestCase(TestCase):
    """
    Test suite for the API views for cryptocurrencies

    """

    def setUp(self):
        # create a test user and give them a token
        testUser = User.objects.create(username='tester', password='pass')
        Token.objects.create(user=testUser)
        self.token = Token.objects.get(user__username=testUser.username)
        # initialize the client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=testUser)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.cryptocurrencyData = {'name': "test", 'tickerSymbol': "tst"}

        self.response = self.client.post(
                reverse('coinAPI'),
                self.cryptocurrencyData,
                format="json")

    def testAPInput(self):
        """
        test that the api can create a new model
        :return:
        """


class CoinViewTestCase(TestCase):
    """
    Test suite for the API views for coins
    """

    def setUp(self):
        import requests
        self.url = 'http://127.0.0.1:8000'
        self.apiToken = requests.post('http://127.0.0.1:8000/api-token-auth/', params={
            'username': 'admin', 'password': 'pass'})

    def testAPInput(self):
        """
        test that the api can create a new model
        :return:
        """
        # test cryptocurrency
        import requests
        from datetime import datetime
        useURL = self.url + '/coins/cryptocurrencyAPI'
        requests.post(useURL,
                      params={'name': 'Bitcoin', 'tickerSymbol': 'BTC', 'active': True,
                              'Authorization': 'Token %s' % self.apiToken})

        # test coins
        useURL = self.url + '/coins/coinAPI'

        requests.post(useURL,
                      params={'cryptocurrency': "cryptocurrency_name='Bitcoin'",
                              'price': 5, 'volume': 5 'time': datetime.now(),
                              'Authorization': 'Token %s' % self.apiToken})
