from django.shortcuts import render
from .models import Cryptocurrency, Coin

# Create your views here.

def coinsView(request):
    """
    Provides data for the coins page by pulling Cryptocurrencies being watched, from the database and displaying them
    on the page.
    """
    template_name = 'coins/'
    user = User.objects.get(username=request.user.username)

    return render(template_name=template_name, context={}, request=request)