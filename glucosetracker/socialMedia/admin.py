from django.contrib import admin
from .models import Tweet, NewsItem, RedditPost


# Register your models here.
class TweetAdmin(admin.ModelAdmin):
    date_hierarchy = 'createdAt'
    search_fields = ['text', 'username', 'url']
    list_display = ('username', 'text', 'createdAt', 'retweetCount', 'likesCount')
    list_filter = ('username',)


class NewsItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'createdAt'
    search_fields = ['headlineText', 'text', 'newsAgency']
    list_display = ('newsAgency', 'headlineText', 'createdAt', 'text')
    list_filter = ('newsAgency',)


class RedditPostAdmin(admin.ModelAdmin):
    date_hierarchy = 'createdAt'
    search_fields = ['text', 'subreddit']
    list_display = ('subreddit', 'createdAt', 'text')
    list_filter = ('subreddit',)


admin.site.register(Tweet, TweetAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(RedditPost, RedditPostAdmin)

# TODO add sorting system in admin pages for each of these
