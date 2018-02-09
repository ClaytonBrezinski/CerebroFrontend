from django.contrib import admin

from .models import Cryptocurrency, Coin
# Register your models here.

admin.site.register(Cryptocurrency)
admin.site.register(Coin)
