from django.db import models


class Tweet(models.Model):
    text = models.CharField(max_length=512)
    retweetCount = models.IntegerField(default=0)
    likesCount = models.IntegerField(default=0)
    createdAt = models.DateTimeField()
    user = models.CharField(max_length=100)
