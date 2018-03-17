import logging
import json

from django.views.generic import TemplateView, FormView, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings

import mailchimp
from braces.views import (
    AjaxResponseMixin,
    JSONResponseMixin,
    LoginRequiredMixin,
)


from socialMedia.models import Tweet, RedditPost, NewsItem
from socialMedia.utils import datetimeToTimeAgo, timeAgoToString
from django.shortcuts import render, HttpResponse
from braces.views import LoginRequiredMixin

from .forms import ContactForm

DATE_FORMAT = '%Y/%m/%d'
TIME_FORMAT = '%I:%M %p'

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    """
    Displays the glucose data table for the currently logged in user. A form
    for quickly adding glucose values is also included.

    The data is loaded by the GlucoseListJson view and rendered by the
    Datatables plugin via Javascript.
    """
    # form = GlucoseQuickAddForm()
    # form.fields['category'].initial = get_initial_category(request.user)
    user = User.objects.get(username=request.user.username)
    user_settings = user.settings

    # TODO update from .latest to a more complex algorithm
    newsItems = NewsItem.objects.order_by('-createdAt')[:4]
    redditPosts = RedditPost.objects.order_by('-createdAt')[:4]
    tweets = Tweet.objects.order_by('-createdAt')[:4]

    for item in newsItems:
        item.daysAgo = timeAgoToString(datetimeToTimeAgo(item.createdAt))
    for item in redditPosts:
        item.daysAgo = timeAgoToString(datetimeToTimeAgo(item.createdAt))
    for item in tweets:
        item.daysAgo = timeAgoToString(datetimeToTimeAgo(item.createdAt))

    return render(template_name='core/dashboard.html',
                  context={
                      # 'form': form,
                           # 'glucose_unit_name': user_settings.glucose_unit.name,
                           'newsItems': newsItems,
                           'redditPosts': redditPosts,
                           'tweets': tweets,
                           },
                  request=request, )


@login_required
def chart_data_json(request):
    data = {}
    params = request.GET

    days = params.get('days', 0)
    name = params.get('name', '')
    # if name == 'avg_by_category':
    #     # data['chart_data'] = ChartData.get_avg_by_category(user=request.user, days=int(days))
    if name == 'avg_by_day':
        # data['chart_data'] = ChartData.get_avg_by_day(user=request.user, days=int(days))
        data['chart_data'] = {'dates': ['2017/05/05', '2017/05/06', '2017/05/07'],
                              'values': [90.0, 95.0, 100.0]}
    # elif name == 'level_breakdown':
    #     data['chart_data'] = ChartData.get_level_breakdown(user=request.user, days=int(days))
    # elif name == 'count_by_category':
    #     data['chart_data'] = ChartData.get_count_by_category(user=request.user, days=int(days))

    return HttpResponse(json.dumps(data), content_type='application/json')

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # context['glucose_count'] = Glucose.objects.count()

        return context


class HelpPageView(LoginRequiredMixin, FormView):
    success_url = '.'
    form_class = ContactForm
    template_name = 'core/help.html'

    def get_initial(self):
        return {
            'email': self.request.user.email
        }

    def form_valid(self, form):
        success_message = '''Email sent! We'll try to get back to you as
            soon as possible.'''
        messages.add_message(self.request, messages.SUCCESS, success_message)

        return super(HelpPageView, self).form_valid(form)

    def form_invalid(self, form):
        failure_message = 'Email not sent. Please try again.'
        messages.add_message(self.request, messages.WARNING, failure_message)

        return super(HelpPageView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            support_email = settings.CONTACTS['support_email']

            message = 'Sent By: %s (%s)\n\n%s' % (
                form.cleaned_data['email'],
                self.request.user.username,
                form.cleaned_data['message'])
            email = EmailMessage(
                from_email=support_email,
                subject='[Help] %s ' % form.cleaned_data['subject'],
                body=message,
                to=[support_email])

            email.send()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MailingListSignupAjaxView(JSONResponseMixin, AjaxResponseMixin, View):
    """
    Sign up an email address to a MailChimp list.
    """

    def post_ajax(self, request, *args, **kwargs):
        email = request.POST.get('email').strip().lower()
        mailchimp_list_id = settings.MAILCHIMP_LIST_ID

        response_dict = {
            'message': '{0} successfully subscribed to {1}!'.format(
                email, mailchimp_list_id),
        }

        mc = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)

        try:
            mc.lists.subscribe(
                id=mailchimp_list_id,
                email={'email': email},
                update_existing=True,
                double_optin=True,
            )
            logger.info('%s successfully subscribed to %s', email,
                        mailchimp_list_id)
        except mailchimp.Error as e:
            logger.error('A MailChimp error occurred: %s', e)

            response_dict['message'] = 'Sorry, an error occurred.'
            return self.render_json_response(response_dict, status=500)

        return self.render_json_response(response_dict)