from django.shortcuts import render
from .models import NewsItem, RedditPost, Tweet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required()
def socialMediaView(request):
    template_name = 'socialMedia/socialMedia.html'
    user = User.objects.get(username=request.user.username)
    # news items
    newsItems = NewsItem.objects.all()[:9]
    # TODO get most popular Reddit and Twitter items through an equation of # of upvotes, retweet, and X days ago
    # TODO need days ago calc
    # reddit items
    redditPosts = RedditPost.objects.all()[:9]
    # twitter items
    tweets = Tweet.objects.all()[:9]
    return render(request, template_name,
                  {'newsItems': newsItems, 'redditPosts': redditPosts, 'tweets': tweets})
