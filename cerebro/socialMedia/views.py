from django.shortcuts import render
from .models import NewsItem, RedditPost, Tweet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import datetimeToTimeAgo, timeAgoToString
# REST framework specific
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RedditPostSerializer, TweetSerializer, NewsItemSerializer


@login_required()
def socialMediaView(request):
    template_name = 'socialMedia/socialMedia.html'
    user = User.objects.get(username=request.user.username)
    # pull news, reddit posts, and tweets from the database
    newsItems = NewsItem.objects.order_by('-createdAt')[:9]
    redditPosts = RedditPost.objects.order_by('-createdAt')[:9]
    tweets = Tweet.objects.order_by('-createdAt')[:9]
    # generate the X mins/hours/days ago text for each entry and put it into the object as a new key
    for item in newsItems:
        item.daysAgo = timeAgoToString(datetimeToTimeAgo(item.createdAt))
    for item in redditPosts:
        item.daysAgo = timeAgoToString(datetimeToTimeAgo(item.createdAt))
    for item in tweets:
        item.daysAgo = timeAgoToString(datetimeToTimeAgo(item.createdAt))

    return render(request, template_name,
                  {'newsItems': newsItems, 'redditPosts': redditPosts, 'tweets': tweets})


class NewsItemList(generics.ListCreateAPIView):
    """
    Serializers are those components used to convert the received data from JSON format to the relative Django model
    and viceversa.
    ListCreateAPIView allows for get and POST requests to occur
    """
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer


class RedditPostList(generics.ListCreateAPIView):
    """
    Serializers are those components used to convert the received data from JSON format to the relative Django model
    and viceversa.
    ListCreateAPIView allows for get and POST requests to occur
    """
    queryset = RedditPost.objects.all()
    serializer_class = RedditPostSerializer


class TweetList(generics.ListCreateAPIView):
    """
    Serializers are those components used to convert the received data from JSON format to the relative Django model
    and viceversa.
    ListCreateAPIView allows for get and POST requests to occur
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
