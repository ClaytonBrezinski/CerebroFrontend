import json
from django.shortcuts import render, HttpResponse
from .models import Cryptocurrency, Coin, Cryptocurrencytable
from django_tables2 import RequestConfig
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .reports import ChartData
from django.db.models import Max
# REST framework specific
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CoinSerializer, CryptocurrencySerializer


# Create your views here.

def cryptocurrenciesView(request):
    """
    Provides data for the coins page by pulling Cryptocurrencies being watched, from the database and displaying them
    on the page.
    """
    template_name = 'coins/cryptocurrencies.html'
    user = User.objects.get(username=request.user.username)

    cryptocurencies = Cryptocurrency.objects.annotate(latest_created_at=Max('coin__time'))
    table = Cryptocurrencytable(Coin.objects.filter(time__in=[b.latest_created_at for b in cryptocurencies]))
    RequestConfig(request).configure(table)

    return render(request=request, template_name=template_name, context={'cryptocurrency': table}, )


# def coinsChart(request):
#   return render()

@login_required
def coinsChartDataJson(request):
    data = {}
    params = request.GET
    # to pull from the js code from cryptocurrencies.html, use this method. If nothing is added, days = 0, name = ""
    # days = params.get('days', 0)
    # name = params.get('name', '')

    # TODO let currency choice get pulled from the webpage
    # data will contain crypto name, price, and the unix time
    data['chart_data'] = ChartData.getCurrencyData(currency='Bitcoin')

    return HttpResponse(json.dumps(data), content_type='application/json')


class CoinList(generics.ListCreateAPIView):
    """
    Serializers are those components used to convert the received data from JSON format to the relative Django model
    and viceversa.
    ListCreateAPIView allows for get and POST requests to occur
    """
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer


class CryptocurrencyList(generics.ListCreateAPIView):
    """
    Serializers are those components used to convert the received data from JSON format to the relative Django model
    and viceversa.
    ListCreateAPIView allows for get and POST requests to occur
    """
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer
