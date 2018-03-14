from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from blogs.models import Blog
from blogs.feeds import LatestBlogsFeed
from core.views import HomePageView
from core.sitemaps import StaticViewSitemap
from glucoses.views import dashboard
from subscribers.views import subscribe_view

admin.autodiscover()

blog_info_dict = {'queryset': Blog.objects.publicly_viewable(),
                  'date_field': 'modified',
                  }

sitemaps = {'static': StaticViewSitemap,
            'blog': GenericSitemap(blog_info_dict),
            }

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),

    # Sitemaps.
    url(r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
        ),

    # Django admin.
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),

    # RSS feeds.
    url(regex=r'^latest/feed/$',
        view=LatestBlogsFeed(),
        name='rss_feed'
        ),

    url(r'^redactor/', include('redactor.urls')),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^glucoses/', include('glucoses.urls')),
    url(r'^blog/', include('blogs.urls')),
    url(r'^coins/', include('coins.urls')),
    url(r'^socialMedia/', include('socialMedia.urls')),

    url(r'^dashboard/$', view=dashboard, name='dashboard'),
    url(r'^subscribe/$', view=subscribe_view, name='subscribe'),
    ]

# Route for media files in local development.
if settings.DEBUG:
    # This serves static files and media files.
    urlpatterns += staticfiles_urlpatterns()
    # In case media is not served correctly
    # urlpatterns += ['',
    #                url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #                    'document_root': settings.MEDIA_ROOT,
    #                    }),
    #                ]
    #

if not settings.DEBUG:
    urlpatterns.append(url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))
