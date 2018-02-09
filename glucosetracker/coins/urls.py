from django.conf.urls import url

from .views import cryptocurrenciesView

urlpatterns = [
    url(regex=r'^$',
        view=cryptocurrenciesView,
        name='cryptocurrencies',
        ),
    ]
