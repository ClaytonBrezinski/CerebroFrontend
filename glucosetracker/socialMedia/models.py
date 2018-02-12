from django.db import models
from django.core import validators


class Tweet(models.Model):
    text = models.CharField(max_length=512)
    retweetCount = models.IntegerField(default=0)
    likesCount = models.IntegerField(default=0)
    createdAt = models.DateTimeField()
    username = models.CharField(max_length=100)
    url = models.URLField(validators=([validators.URLValidator]))
    # TODO add default name


class NewsItem(models.Model):
    headlineText = models.CharField(max_length=128)
    text = models.CharField(
            max_length=512)  # TODO we will need to cut down the length of this when displayed on webpage
    createdAt = models.DateTimeField()
    url = models.URLField(validators=([validators.URLValidator]))
    newsAgency = models.CharField(max_length=256)

    # TODO add default name


class RedditPost(models.Model):
    text = models.CharField(max_length=512)
    createdAt = models.DateTimeField()
    url = models.URLField(validators=([validators.URLValidator]))
    subreddit = models.CharField(max_length=128, validators=[validators.RegexValidator(
            regex=r'^\/r\/',
            message="Please do not include the /r/ of the subreddit",
            inverse_match=True,
            )])
    # ^\/r\/
    comments = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    # TODO add default name
