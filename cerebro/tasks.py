"""
this is the tasks file built on the Heroku server.
Each of the functions within this file are called by Heroku's celery workers
at time intervals specified within Heroku's environment variables.
"""


@app.task()
def pullCoinsFromBackend():
    """
    Scraping process for getting the backend's coin data.
    Run every 10 minutes by Heroku's Celery workers
    """
    import requests
    from datetime import datetime, timedelta
    from coins.models import Coin, Cryptocurrency

    coinsToScrape = ['Bitcoin', 'Ripple', 'Ethereum', 'Litecoin', 'Dogecoin', 'Ambrossous', 'Monero']

    lastHalfHourDateTime = datetime.now() - timedelta(minutes=30)
    token = [BACKEND_TOKEN]

    for coin in coinsToScrape:

        cryptocurrency = Cryptocurrency.objects.get(name=coin)

        # call REST endpoint of backend and pull from it
        result = requests.get('http://dev.cerebro.alttrasolutions.tech:8000/scraper/coinsList',
                              params={'coin': coin, 'start': lastHalfHourDateTime 'end': datetime.now(), 'Authorization': 'Token %s' % token}

        # push the result from the backend into the database
        for entry in result:
            coinObject = Coin.objects.create(cryptocurrency=cryptocurrency, price=entry.price, volume=entry.rate,
                                             time=entry.dateEntry)
        coinObject.save()


# @app.task()
def pullSentimentFromBackend():
    """
    Scraping process for getting the backend's sentiment data
    Run every 30 minutes by Heroku's Celery workers
    This has not yet been implemented yet
    """
    import requests
    from datetime import datetime, timedelta
    # import sentiment class on frontend here

    lastHalfHourDateTime = datetime.now() - timedelta(minutes=30)
    token = [BACKEND_TOKEN]

    # call REST endpoint of backend and pull from it
    result = requests.get('http://dev.cerebro.alttrasolutions.tech:8000/sentiment/SentimentResultList',
                          params={'start': lastHalfHourDateTime, 'end': datetime.now(), 'Authorization': 'Token %s' % token}

    # get the average over the last 30 minutes
    average = 0
    for entry in result:
        average += entry.sentimentRating
    average = average / len(result)\

@app.task()
def pullTweetsFromBackend():
    """
    Scraping process for getting the backend's tweet data
    Run every 30 minutes by Heroku's Celery workers
    """
    import requests
    from datetime import datetime, timedelta
    from socialMedia.models import Tweet

    lastHalfHourDateTime = datetime.now() - timedelta(minutes=30)
    token = [BACKEND_TOKEN]

    # call REST endpoint and pull from it
    result = requests.get('http://dev.cerebro.alttrasolutions.tech:8000/scraper/tweetList',
                          params={'start': lastHalfHourDateTime 'end': datetime.now(), 'Authorization': 'Token %s' % token}

    # push the top 10 Tweets that were pulled to the database
    for entry in result:
        Tweet.objects.create(text=entry.text, retweetCount=entry.reTweetCount, likesCount=entry.favouriteCount,
                             createdAt=entry.createdAt, username=entry.user.screenName)