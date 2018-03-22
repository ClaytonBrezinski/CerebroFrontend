from .models import RedditPost, Tweet, NewsItem
from rest_framework import serializers


class RedditPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditPost
        fields = ('text', 'createdAt', 'url', 'subreddit', 'comments', 'upvotes')


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('text', 'retweetCount', 'likesCount', 'createdAt', 'username', 'url')


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ('headlineText', 'text', 'createdAt', 'url', 'newsAgency')