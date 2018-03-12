from django.conf.urls import url

from .views import cryptocurrenciesView, coinsChartDataJson

urlpatterns = [
    url(regex=r'^$',
        view=cryptocurrenciesView,
        name='cryptocurrencies',
        ),
    url(regex=r'^coinsChartDataJson/$',
        view=coinsChartDataJson,
        name='coinsChartDataJson',
        ),
    ]
