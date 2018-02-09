from django.shortcuts import render
from .models import Cryptocurrency, Coin, Cryptocurrencytable

from django_tables2 import RequestConfig

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

def cryptocurrenciesView(request):
    """
    Provides data for the coins page by pulling Cryptocurrencies being watched, from the database and displaying them
    on the page.
    """
    template_name = 'coins/cryptocurrencies.html'
    user = User.objects.get(username=request.user.username)

    table = Cryptocurrencytable(Cryptocurrency.objects.all())
    RequestConfig(request).configure(table)

    return render(request=request, template_name=template_name, context={'cryptocurrency': table}, )


# def coinsChart(request):
#   return render()

@login_required
def coinsChartDataJson(request):
    data = {}
    params = request.GET
