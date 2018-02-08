from django.conf.urls import url

from .views import *

urlpatterns = [
    url(
            regex=r'^cryptocurrencies/',
            view=
            name='cryptocurrencies',

        )
    ]