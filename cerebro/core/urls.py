from django.conf.urls import url

from .views import HelpPageView, MailingListSignupAjaxView, chart_data_json

urlpatterns = [

    url(regex=r'^help/',
        view=HelpPageView.as_view(),
        name='help',
        ),
    url(regex=r'^mailing-list-signup-ajax-view/',
        view=MailingListSignupAjaxView.as_view(),
        name='mailing_list_signup_ajax_view',
        ),
    url(regex=r'^chart_data_json/$',
        view=chart_data_json,
        name='chart_data_json',
        ),
    ]
