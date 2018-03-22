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

    def setUp(self):
        """
        Define variables for a basic cryptocurrency
        :return:
        """
        self.cryptocurrencyName = 'test'
        self.cryptocurrencyTickerSymbol = 'tst'
        self.cryptocurrency = Cryptocurrency(name=self.cryptocurrencyName, tickerSymbol=self.cryptocurrencyTickerSymbol)

    def testCreateNewModel(self):
        """
        Creating a new cryptocurrency
        :return:
        """
        oldCount = Cryptocurrency.objects.count()
        self.cryptocurrency.save()
        newCount = Cryptocurrency.objects.count()
        self.assertNotEqual(oldCount, newCount)

    def testErrornousCreation(self):
        """
        Create cryptocurrencies with errornous data inputs
        :return:
        """
        pass


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
        pass


class CryptoCurrencyViewTestCase(TestCase):
    """
    Test suite for the API views
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

        # self.cryptocurrencyData = {'name': "test", 'tickerSymbol': "tst"}
        #
        # self.response = self.client.post(
        #         reverse('coinAPI'),
        #         self.cryptocurrencyData,
        #         format="json")

    def testAPIput(self):
        """
        test that the api can create a new model
        :return:
        """
        # self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        pass


class CoinViewTestCase(TestCase):
    """
    Test suite for the API views
    """

    def setUp(self):
        pass

    def testAPIput(self):
        """
        test that the api can create a new model
        :return:
        """
