from .models import Coin, Cryptocurrency
from rest_framework import serializers


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('cryptocurrency', 'price', 'volume', 'time')


class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = ('name', 'tickerSymbol', 'active')
