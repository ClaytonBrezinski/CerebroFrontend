from django.conf.urls import url

from .views import socialMediaView, NewsItemList, RedditPostList, TweetList

urlpatterns = [
    url(regex=r'^$',
        view=socialMediaView,
        name='socialMedia',
        ),
    url(regex=r'^redditPostAPI/$',
        view=NewsItemList.as_view()
        ),
    url(regex=r'^tweetAPI/$',
        view=RedditPostList.as_view()
        ),
    url(regex=r'^newsItemAPI/$',
        view=TweetList.as_view()
        ),

    ]
