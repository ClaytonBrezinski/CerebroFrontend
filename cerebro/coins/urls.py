from django.conf.urls import url
from .views import cryptocurrenciesView, coinsChartDataJson, CoinList, CryptocurrencyList

urlpatterns = [
    url(regex=r'^$',
        view=cryptocurrenciesView,
        name='cryptocurrencies',
        ),
    url(regex=r'^coinsChartDataJson/$',
        view=coinsChartDataJson,
        name='coinsChartDataJson',
        ),
    url(regex=r'^coinAPI/$',
        view=CoinList.as_view(),
        name='coinAPI'
        ),
    url(regex=r'^currencyAPI/$',
        view=CryptocurrencyList.as_view(),
        name='currencyAPI'
        ),
    ]
