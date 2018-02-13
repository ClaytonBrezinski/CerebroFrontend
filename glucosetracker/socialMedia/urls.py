from django.conf.urls import url

from .views import socialMediaView

urlpatterns = [
    url(regex=r'^$',
        view=socialMediaView,
        name='socialMedia',
        ),
    ]
