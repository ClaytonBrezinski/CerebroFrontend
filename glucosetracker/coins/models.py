from django.db import models


class Cryptocurrency(models.Model):
    name = models.CharField(unique=True, max_length=25)
    tickerSymbol = models.CharField(max_length=5)
    active = models.BooleanField(default=True)
    # TODO add Exchange model to the coins app.
    # exchanges = models.ManyToManyField(Exchange)


class Coin(models.Model):
    cryptocurrency = models.ForeignKey(Cryptocurrency, null=False, blank=False, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=False, blank=False)
    volume = models.PositiveIntegerField(null=False, blank=False)
    time = models.DateTimeField(auto_now=False)
