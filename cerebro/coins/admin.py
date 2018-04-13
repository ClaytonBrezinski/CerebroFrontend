from django.contrib import admin

from .models import Cryptocurrency, Coin


# customize the admin view panel with this class


class CoinAdmin(admin.ModelAdmin):
    list_filter = [
        'cryptocurrency',
        'time',
        ]
    list_per_page = 800


admin.site.register(Cryptocurrency)
admin.site.register(Coin, CoinAdmin)
