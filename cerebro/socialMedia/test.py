from django.test import TestCase
from .models import RedditPost, Tweet, NewsItem

# Datetime stuff
from django.utils.timezone import now

# REST API stuff
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse



class TweetModelTestCase(TestCase):
    """
    This is a test suite for the Cryptocurrency model
    """

    def setUp(self):
        """
        Define variables for a basic Tweet model
        :return:
        """
        self.text = 'test'
        self.createdAt = now()
        self.username = 'tester'
        self.url = 'reddit.com/'
        self.tweet = Tweet(text=self.text, createdAt=self.createdAt, username=self.username, url=self.url)

    def testCreateNewModel(self):
        """
        Creating a new tweet
        :return:
        """
        oldCount = Tweet.objects.count()
        self.tweet.save()
        newCount = Tweet.objects.count()
        self.assertNotEqual(oldCount, newCount)

    def testErrornousCreation(self):
        """
        Create tweet with errornous data inputs
        :return:
        """
        pass

    def testGetName(self):
        pass

    def testPopularityProperty(self):
        pass


class NewsItemTestCase(TestCase):
    """
    This is a test suite for the NewsItem model
    """

    def setUp(self):
        """
        Define variables for a basic News item model
        :return:
        """
        self.headlineText = 'thisIsATest'
        self.text = 'thisIsText'
        self.createdAt = now()
        self.url = 'reddit.com/'
        self.newsAgency = 'testerInc'
        self.newsItem = NewsItem(headlineText=self.headlineText, text=self.headlineText, createdAt=self.createdAt,
                                 url=self.url, newsAgency=self.newsAgency)

    def testCreateNewModel(self):
        """
        Creating a new news item
        :return:
        """
        oldCount = NewsItem.objects.count()
        self.newsItem.save()
        newCount = NewsItem.objects.count()
        self.assertNotEqual(oldCount, newCount)

    def testErrornousCreation(self):
        """
        Create news item with errornous data inputs
        :return:
        """
        pass


class RedditPostTestCase(TestCase):
    """
    This is a test suite for the RedditPost model
    """

    def setUp(self):
        """
        Define variables for a basic RedditPost model
        :return:
        """
        self.text = 'test'
        self.createdAt = now()
        self.url = 'reddit.com/'
        self.subreddit = 'test'
        self.comments = 1
        self.upvotes = 1
        self.redditPost = RedditPost(text=self.text, createdAt=self.createdAt, url=self.url, subreddit=self.subreddit,
                                     comments=self.comments, upvotes=self.upvotes)

    def testCreateNewModel(self):
        """
        Creating a new RedditPost
        :return:
        """
        oldCount = RedditPost.objects.count()
        self.redditPost.save()
        newCount = RedditPost.objects.count()
        self.assertNotEqual(oldCount, newCount)

    def testErrornousCreation(self):
        """
        Create RedditPost with errornous data inputs
        :return:
        """
        pass
