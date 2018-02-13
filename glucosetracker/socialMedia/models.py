from django.db import models
from django.core import validators
from datetime import datetime
from django.utils import timezone
from .utils import datetimeToTimeAgo


class Tweet(models.Model):
    # TODO add # of comments field, add that to the popularity eqn
    text = models.CharField(max_length=512)
    retweetCount = models.IntegerField(default=0)
    likesCount = models.IntegerField(default=0)
    createdAt = models.DateTimeField()
    username = models.CharField(max_length=100)
    url = models.URLField(validators=([validators.URLValidator]))

    def get_name(self):
        return self.username + " - " + self.text

    def __str__(self):
        return self.username + " - " + self.text

    @property
    def popularity(self):
        today = datetime.now(timezone.get_current_timezone())
        datetimedelta = self.createdAt - today
        timeAgo = datetimeToTimeAgo(datetimedelta)

        if timeAgo['timeParameter'] == 'day':
            return (self.retweetCount + self.likesCount) / (timeAgo['value'] * 6)
        elif timeAgo['timeParameter'] == 'hour':
            return (self.retweetCount + self.likesCount) / (timeAgo['value'] * 3)
        elif timeAgo['timeParameter'] == 'minute':
            return (self.retweetCount + self.likesCount) / (timeAgo['value'] * 2)
        else:
            return 0

    class Meta:
        get_latest_by = "createdAt"


class NewsItem(models.Model):
    headlineText = models.CharField(max_length=128)
    text = models.CharField(
            max_length=512)  # TODO we will need to cut down the length of this when displayed on webpage
    createdAt = models.DateTimeField()
    url = models.URLField(validators=([validators.URLValidator]))
    newsAgency = models.CharField(max_length=256)

    def __str__(self):
        return self.newsAgency + " - " + self.headlineText

    class Meta:
        get_latest_by = "createdAt"


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

    @property
    def popularity(self):
        # TODO should account for the popularity of the subreddit
        today = datetime.now(timezone.get_current_timezone())
        datetimedelta = self.createdAt - today
        timeAgo = datetimeToTimeAgo(datetimedelta)

        if timeAgo['timeParameter'] == 'day':
            return (self.comments + self.upvotes) / (timeAgo['value'] * 6)
        elif timeAgo['timeParameter'] == 'hour':
            return (self.comments + self.upvotes) / (timeAgo['value'] * 3)
        elif timeAgo['timeParameter'] == 'minute':
            return (self.comments + self.upvotes) / (timeAgo['value'] * 2)
        else:
            return 0

    def get_name(self):
        return self.subreddit + " - " + self.text

    def __str__(self):
        return self.subreddit + " - " + self.text

    class Meta:
        get_latest_by = "createdAt"
