from django.db import models
import django_tables2 as tables
from datetime import datetime, timedelta


class Cryptocurrency(models.Model):
    name = models.CharField(unique=True, max_length=25)
    tickerSymbol = models.CharField(max_length=5)
    active = models.BooleanField(default=True)

    # TODO add Exchange model to the coins app.
    # exchanges = models.ManyToManyField(Exchange)
    # TODO add cryptocurrency rank that gets updated daily

    def __str__(self):
        return '(' + self.tickerSymbol + ') - ' + self.name

    class Meta:
        verbose_name_plural = 'Cryptocurrencies'

    def get_name(self):
        return self.name


class Coin(models.Model):
    cryptocurrency = models.ForeignKey(Cryptocurrency, null=False, blank=False, on_delete=models.CASCADE)
    price = models.DecimalField(null=False, blank=False, max_digits=17, decimal_places=8)
    volume = models.PositiveIntegerField(null=False, blank=False)
    time = models.DateTimeField(auto_now=False)

    class Meta:
        verbose_name_plural = 'Coins'

    def __str__(self):
        return self.cryptocurrency.name + ' at ' + str(self.time.date())

    def get_name(self):
        return self.cryptocurrency.name


class Cryptocurrencytable(tables.Table):
    rank = tables.Column(verbose_name='#')
    name = tables.Column(verbose_name='Name', accessor='cryptocurrency.name')
    tickerSymbol = tables.Column(verbose_name='Ticker Symbol', accessor='cryptocurrency.tickerSymbol')
    price = tables.Column(verbose_name='Price ($)', )
    marketCap = tables.Column(verbose_name='Market Cap', accessor='cryptocurrency.tickerSymbol')
    volume = tables.Column(verbose_name='Social Media Volume')

    circulatingSupply = tables.Column(verbose_name='Circulating Supply', accessor='cryptocurrency.tickerSymbol')
    dayChange = tables.Column(verbose_name='% Change(24h)')
    weekChange = tables.Column(verbose_name='% Change(7d)')

    class Meta:
        model = Coin
        template_name = 'django_tables2/bootstrap-responsive.html'
        sequence = ('rank', 'name', 'tickerSymbol')
        fields = ('name', 'tickerSymbol')  # 'price', 'Market Cap'
        attrs = {'class': 'table table-striped table-hover'}

    def render_price(self, record, value):
        """
        Since all coins except for BTC are priced in relation to BTC, convert them back to $ USD when printing on the table
        :param record: the whole row that is being pulled. such as BTC, LTC, etc.
        :param value: the value from the row that is being pulled, BTC's price, LTC's price.
        :return: either BTC's USD value or the coin's value converted to USD value based on BTC's latest price.
        """
        if record.cryptocurrency.tickerSymbol == 'BTC':
            return round(value, 3)
        else:
            latestBTCprice = Coin.objects.filter(cryptocurrency__tickerSymbol='BTC').latest('id')
            return round(float(value) * float(latestBTCprice.price), 3)

    def render_volume(self, record):
        """
        Override the traditional social volume reading, instead output the whole day's volume.
        :param record: the whole row that is being pulled. such as BTC, LTC, etc.
        :return: the whole day's social media volume
        """
        ## change this for project day accuracy
        daysCoins = Coin.objects.filter(time__gte=datetime.now() - timedelta(days=14),
                                        cryptocurrency__tickerSymbol=record.cryptocurrency.tickerSymbol)
        socialVolume = 0
        for coin in daysCoins:
            socialVolume += coin.volume
        return "%i posts" % socialVolume

    # TODO: remove the hardcoded marketcap and circulating supply values
    # hard code these two for presentation day
    def render_marketCap(self, record):
        """
        hardcode the marketcap value being outputted on the table
        :param record:
        :return:
        """
        def getMarketCap(tickerSymbol):
            return {
                'BTC': 115461148996,
                'LTC': 6602863513,
                'ETH': 37361268692,
                'DASH': 2396292038,
                'BCH': 10976152334,
                'XRP': 19239977379,
                }[tickerSymbol]

        ticker = record.cryptocurrency.tickerSymbol
        return "$ %s" %format(getMarketCap(ticker), ',d')

    def render_circulatingSupply(self, record):
        def getCirculatingSupply(tickerSymbol):
            return {
                'BTC': 16960550,
                'LTC': 55957419,
                'ETH': 98643874,
                'DASH': 7994142,
                'BCH': 17057700,
                'XRP': 39094520623,
                }[tickerSymbol]

        ticker = record.cryptocurrency.tickerSymbol
        return "%s %s" %(format(getCirculatingSupply(ticker), ',d'), ticker)
    # def render_dayChange()
    # def render_weekChange()
