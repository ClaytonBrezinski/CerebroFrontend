from django.test import TestCase
from .models import Cryptocurrency, Coin

# Datetime stuff
from django.utils.timezone import now


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
