from django.conf.urls import url

from .views import BlogDetailView, BlogListView, BlogTagListView

urlpatterns = [
    url(regex=r'^$',
        view=BlogListView.as_view(),
        name='blog_list_view',
        ),
    url(regex=r'^tag/(?P<tag>[\w ]+)/$',
        view=BlogTagListView.as_view(),
        name='blog_tag_list_view',
        ),
    url(regex=r'^(?P<slug>[\w-]+)/$',
        view=BlogDetailView.as_view(),
        name='blog_detail_view',
        ),
    ]
