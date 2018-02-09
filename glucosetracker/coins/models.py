from django.db import models
import django_tables2 as tables


class Cryptocurrency(models.Model):
    name = models.CharField(unique=True, max_length=25)
    tickerSymbol = models.CharField(max_length=5)
    active = models.BooleanField(default=True)
    # TODO add Exchange model to the coins app.
    # exchanges = models.ManyToManyField(Exchange)

    def __str__(self):
        return '(' + self.tickerSymbol + ') - ' + self.name

    class Meta:
        verbose_name_plural = 'Cryptocurrencies'

    def get_name(self):
        return self.name

class Coin(models.Model):
    cryptocurrency = models.ForeignKey(Cryptocurrency, null=False, blank=False, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=False, blank=False)
    volume = models.PositiveIntegerField(null=False, blank=False)
    time = models.DateTimeField(auto_now=False)


    class Meta:
        verbose_name_plural = 'Coins'

    def __str__(self):
        return self.cryptocurrency.name + ' at ' + str(self.time.date())

    def get_name(self):
        return self.cryptocurrency.name

class Cryptocurrencytable(tables.Table):
    class Meta:
        model = Cryptocurrency
        template_name = 'django_tables2/bootstrap.html'
