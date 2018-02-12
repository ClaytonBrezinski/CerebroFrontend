from django.conf.urls import url

from .views import

urlpatterns = [
    url(regex=r'^$',
        view=Tweet.as_view(),
        name='blog_list_view',
        ),
    ]
