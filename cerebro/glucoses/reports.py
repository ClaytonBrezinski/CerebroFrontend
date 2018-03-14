# import csv
# from io import BytesIO, StringIO
# from datetime import datetime, timedelta
# import logging
#
# from reportlab.lib import colors
# from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
# from django.contrib.auth.models import User
# from django.conf import settings
# from django.core.mail import EmailMessage
# from django.db.models import Avg, Min, Max
#
# from core import utils as core_utils
#
# # from .models import Glucose
#
# logger = logging.getLogger(__name__)
#
# DATE_FORMAT = '%Y/%m/%d'
# FILENAME_DATE_FORMAT = '%b%d%Y'
# TIME_FORMAT = '%I:%M %p'
#
#
# class UserStats(object):
#
#     def __init__(self, user):
#         self.user = user
#         # self.data = Glucose.objects.by_user(self.user)
#         # self.glucose_unit_name = user.settings.glucose_unit.name
#
#     def glucose_by_unit_setting(self, value):
#         return core_utils.glucose_by_unit_setting(self.user, value)
#
#     @property
#     def user_settings(self):
#         user = User.objects.get(username=self.user.username)
#         user_settings = user.settings
#
#         low = user_settings.glucose_low
#         high = user_settings.glucose_high
#         target_min = user_settings.glucose_target_min
#         target_max = user_settings.glucose_target_max
#
#         return {
#             'low': low,
#             'high': high,
#             'target_min': target_min,
#             'target_max': target_max
#             }
#
#     @property
#     def user_stats(self):
#         stats = {
#             'latest_entry': self.latest_entry,
#             'num_records': self.data.count(),
#             'hba1c': self.hba1c,
#             'breakdown': self.get_breakdown(),
#             }
#
#         return stats
#
#     @property
#     def latest_entry(self):
#         latest_entry = self.data.order_by('-record_date', '-record_time')[0] if self.data else None
#
#         latest_entry_value = 'None'
#         latest_entry_time = latest_entry_notes = ''
#         css_class = self.get_css_class(None)
#         if latest_entry:
#             latest_entry_value = '%s %s' % (self.glucose_by_unit_setting(latest_entry.value), self.glucose_unit_name)
#             latest_entry_time = latest_entry.record_time.strftime(TIME_FORMAT)
#             latest_entry_notes = latest_entry.notes
#             css_class = self.get_css_class(latest_entry.value)
#
#         return {
#             'value': latest_entry_value,
#             'record_time': latest_entry_time,
#             'notes': latest_entry_notes,
#             'css_class': css_class,
#             }
#
#     @property
#     def hba1c(self):
#         """
#         The HbA1c is calculated using the average blood glucose from the last
#         90 days.
#
#             Less than 7 = Excellent
#             Between 7 and 8 = Average
#             Greater than 8 = Bad
#         """
#         now = datetime.now(tz=self.user.settings.time_zone).date()
#         subset = self.by_date(now - timedelta(days=90), now)
#         average = core_utils.round_value(
#                 subset.aggregate(Avg('value'))['value__avg'])
#         hba1c = core_utils.round_value(core_utils.calc_hba1c(average))
#
#         css_class = 'text-default'
#
#         if hba1c:
#             if hba1c < 7:
#                 css_class = 'text-success'
#             elif hba1c > 8:
#                 css_class = 'text-danger'
#             else:
#                 css_class = 'text-primary'
#
#         value_html = '%s%%<br><small>(%s %s)</small>' % (hba1c, self.glucose_by_unit_setting(average),
#                                                          self.glucose_unit_name) \
#             if hba1c else 'None<br><small>(None)</small>'
#
#         return {
#             'value': value_html,
#             'css_class': css_class
#             }
#
#     def get_breakdown(self, days=14):
#         now = datetime.now(tz=self.user.settings.time_zone).date()
#         subset = self.by_date(now - timedelta(days=days), now)
#
#         total = subset.count()
#         lowest = subset.aggregate(Min('value'))['value__min']
#         highest = subset.aggregate(Max('value'))['value__max']
#         average = core_utils.round_value(
#                 subset.aggregate(Avg('value'))['value__avg'])
#
#         highs = subset.filter(value__gt=self.user_settings['high']).count()
#         lows = subset.filter(value__lt=self.user_settings['low']).count()
#         within_target = subset.filter(
#                 value__gte=self.user_settings['target_min'],
#                 value__lte=self.user_settings['target_max']
#                 ).count()
#         other = total - (highs + lows + within_target)
#
#         return {
#             'total': total,
#             'lowest': {'value': '%s %s' % (self.glucose_by_unit_setting(lowest), self.glucose_unit_name)
#             if lowest else 'None', 'css_class': self.get_css_class(lowest),
#                        },
#             'highest': {'value': '%s %s' % (self.glucose_by_unit_setting(highest), self.glucose_unit_name)
#             if highest else 'None',
#                         'css_class': self.get_css_class(highest),
#                         },
#             'average': {'value': '%s %s' % (self.glucose_by_unit_setting(average), self.glucose_unit_name)
#             if average else 'None',
#                         'css_class': self.get_css_class(average)
#                         },
#             'highs': '%s (%s%%)' % (highs, core_utils.percent(highs, total)),
#             'lows': '%s (%s%%)' % (lows, core_utils.percent(lows, total)),
#             'within_target': '%s (%s%%)' % (within_target, core_utils.percent(within_target, total)),
#             'other': '%s (%s%%)' % (other, core_utils.percent(other, total)),
#             }
#
#     def by_date(self, start, end):
#         return self.data.filter(record_date__gte=start, record_date__lte=end)
#
#     def get_css_class(self, value):
#         css_class = 'text-default'
#
#         low = self.user_settings['low']
#         high = self.user_settings['high']
#         target_min = self.user_settings['target_min']
#         target_max = self.user_settings['target_max']
#
#         # Only change the css_class if a value exists.
#         if value:
#             if value < low or value > high:
#                 css_class = 'text-danger'
#             elif value >= target_min and value <= target_max:
#                 css_class = 'text-success'
#             else:
#                 css_class = 'text-primary'
#
#         return css_class
#
#
    # class ChartData(object):
    #
    #     @classmethod
    #     def get_count_by_category(cls, user, days):
    #         now = datetime.now(tz=user.settings.time_zone).date()
    #
    #         category_count = Glucose.objects.by_category(
    #                 (now - timedelta(days=days)), now, user)
    #
    #         data = [[c['category__name'], c['count']] for c in category_count]
    #
    #         return data
    #
    # @classmethod
    # def get_level_breakdown(cls, user, days):
    #     now = datetime.now(tz=user.settings.time_zone).date()
    #
    #     glucose_level = Glucose.objects.level_breakdown(
    #             (now - timedelta(days=days)), now, user)
    #
    #     chart_colors = {
    #         'Low': 'orange',
    #         'High': 'red',
    #         'Within Target': 'green',
    #         'Other': 'blue'
    #         }
    #
    #     data = []
    #     keyorder = ['Low', 'High', 'Within Target', 'Other']
    #     for k, v in sorted(glucose_level.items(),
    #                        key=lambda i: keyorder.index(i[0])):
    #         data.append({'name': k, 'y': v, 'color': chart_colors[k]})
    #
    #     return data
    #
    # @classmethod
    # def get_avg_by_category(cls, user, days):
    #     now = datetime.now(tz=user.settings.time_zone).date()
    #
    #     glucose_averages = Glucose.objects.avg_by_category(
    #             (now - timedelta(days=days)), now, user)
    #
    #     data = {'categories': [], 'values': []}
    #     for avg in glucose_averages:
    #         rounded_value = core_utils.round_value(avg['avg_value'])
    #         data['values'].append(
    #                 core_utils.glucose_by_unit_setting(user, rounded_value))
    #         data['categories'].append(avg['category__name'])
    #
    #     return data

    # @classmethod
    # def get_avg_by_day(cls, user, days):
    #     """
    #     pull data from the database for displaying on the website
    #     :param user:
    #     :param days:
    #     :return:
    #     """
    #     now = datetime.now(tz=user.settings.time_zone).date()
    #
    #     glucose_averages = Glucose.objects.avg_by_day(
    #             (now - timedelta(days=days)), now, user)
    #
    #     data = {'dates': [], 'values': []}
    #     for avg in glucose_averages:
    #         rounded_value = core_utils.round_value(avg['avg_value'])
    #         data['values'].append(core_utils.glucose_by_unit_setting(user, rounded_value))
    #         data['dates'].append(avg['record_date'].strftime('%m/%d'))
    #
    #     return data


# class GlucoseBaseReport(object):
#
#     def __init__(self, start_date, end_date, user, include_notes=True,
#                  include_tags=True):
#         self.start_date = start_date
#         self.end_date = end_date
#         self.user = user
#         self.include_notes = include_notes
#         self.include_tags = include_tags
#         self.email_footer = '----------\nSent from https://%s' % settings.SITE_DOMAIN
#
#     def glucose_by_unit_setting(self, value):
#         return core_utils.glucose_by_unit_setting(self.user, value)
#
#
# class GlucoseCsvReport(GlucoseBaseReport):
#
#     def generate(self):
#         data = Glucose.objects.by_date(self.start_date, self.end_date, self.user)
#         data = data.order_by('-record_date', '-record_time')
#
#         csv_data = StringIO()
#         try:
#             headers = ['Value', 'Category', 'Date', 'Time']
#
#             if self.include_notes:
#                 headers.append('Notes')
#
#             if self.include_tags:
#                 headers.append('Tags')
#
#             writer = csv.writer(csv_data)
#             writer.writerow(headers)
#
#             for item in data:
#                 row = [
#                     self.glucose_by_unit_setting(item.value),
#                     item.category,
#                     item.record_date.strftime(DATE_FORMAT),
#                     item.record_time.strftime(TIME_FORMAT),
#                     ]
#
#                 if self.include_notes:
#                     row.append(item.notes)
#
#                 if self.include_tags:
#                     tag_list = ', '.join([t.name for t in item.tags.all()])
#                     row.append(tag_list)
#
#                 writer.writerow(row)
#
#             logging.info('CSV report generated for %s', self.user)
#
#             return csv_data.getvalue()
#
#         finally:
#             csv_data.close()
#
#     def email(self, recipient, subject='', message=''):
#         message = '%s\n\n\n%s' % (message, self.email_footer)
#
#         email = EmailMessage(
#                 from_email=settings.CONTACTS['info_email'],
#                 subject=subject,
#                 body=message,
#                 to=[recipient],
#                 headers={'Reply-To': self.user.email},
#                 )
#
#         attachment_filename = 'GlucoseData_%sto%s.csv' % (self.start_date.strftime(FILENAME_DATE_FORMAT),
#                                                           self.end_date.strftime(FILENAME_DATE_FORMAT))
#
#         email.attach(attachment_filename, self.generate(), 'text/csv')
#         email.send()
#
#
# class GlucosePdfReport(GlucoseBaseReport):
#
#     def __init__(self, *args, **kwargs):
#         super(GlucosePdfReport, self).__init__(*args, **kwargs)
#
#         self.styles = getSampleStyleSheet()
#         self.styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
#         self.styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
#         self.styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
#         self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
#
#         # Width of a letter size paper
#         self.max_width = 8.5 * inch
#         self.left_margin = 0.7 * inch
#         self.right_margin = 0.75 * inch
#         self.top_margin = 0.7 * inch
#         self.bottom_margin = 0.7 * inch
#
#         self.fields = [
#             ('value', 'Value'),
#             ('category', 'Category'),
#             ('date', 'Date'),
#             ('time', 'Time'),
#             ]
#
#         if self.include_notes:
#             self.fields.append(('notes', 'Notes'))
#
#         if self.include_tags:
#             self.fields.append(('tags', 'Tags'))
#
#     def generate(self):
#         qs = Glucose.objects.by_date(
#                 self.start_date, self.end_date, self.user)
#         qs = qs.order_by('-record_date', '-record_time')
#
#         data = []
#         for i in qs:
#             value = i.value
#             value_by_unit_setting = self.glucose_by_unit_setting(value)
#
#             # Bold the text if the value is high or low based on the user's
#             # settings
#             low = self.user.settings.glucose_low
#             high = self.user.settings.glucose_high
#             if value < low or value > high:
#                 value_by_unit_setting = '<b>%s</b>' % value_by_unit_setting
#
#             data_dict = {
#                 'value': self.to_paragraph(value_by_unit_setting),
#                 'category': i.category,
#                 'date': i.record_date.strftime(DATE_FORMAT),
#                 'time': i.record_time.strftime(TIME_FORMAT),
#                 }
#
#             if self.include_notes:
#                 data_dict['notes'] = self.to_paragraph(i.notes)
#
#             if self.include_tags:
#                 tag_list = ', '.join([t.name for t in i.tags.all()])
#                 data_dict['tags'] = self.to_paragraph(tag_list)
#
#             data.append(data_dict)
#
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer,
#                                 pagesize=letter,
#                                 leftMargin=self.left_margin,
#                                 rightMargin=self.right_margin,
#                                 topMargin=self.top_margin,
#                                 bottomMargin=self.bottom_margin)
#
#         styles = getSampleStyleSheet()
#         styleH = styles['Heading1']
#
#         story = []
#
#         story.append(Paragraph('Glucose Data', styleH))
#         story.append(Spacer(1, 0.25 * inch))
#
#         converted_data = self.__convert_data(data)
#         table = Table(converted_data, hAlign='LEFT')
#         table.setStyle(TableStyle([
#             ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#             ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#             ('ALIGN', (1, 0), (0, -1), 'LEFT'),
#             ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
#             ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
#             ]))
#
#         story.append(table)
#         doc.build(story)
#
#         pdf = buffer.getvalue()
#         buffer.close()
#
#         logging.info('PDF report generated for %s', self.user)
#
#         return pdf
#
#     def email(self, recipient, subject='', message=''):
#         message = '%s\n\n\n%s' % (message, self.email_footer)
#
#         email = EmailMessage(
#                 from_email=settings.CONTACTS['info_email'],
#                 subject=subject,
#                 body=message,
#                 to=[recipient],
#                 headers={'Reply-To': self.user.email},
#                 )
#
#         attachment_filename = 'GlucoseData_%sto%s.pdf' % (self.start_date.strftime(FILENAME_DATE_FORMAT),
#                                                           self.end_date.strftime(FILENAME_DATE_FORMAT))
#
#         email.attach(attachment_filename, self.generate(), 'application/pdf')
#         email.send()
#
#     def get_width_from_percent(self, values=[], max_width=None, indent=0):
#         """
#         Return the width values from the given percent values.
#         """
#         if not max_width:
#             max_width = self.max_width
#
#         width_diff = (max_width) - (indent + self.left_margin +
#                                     self.right_margin)
#         widths = [((width_diff * v) / 100) for v in values]
#
#         return widths
#
#     def to_paragraph(self, data):
#         """
#         Convert the data to a Paragraph object.
#
#         Paragraph objects can be easily formatted using HTML-like tags
#         and automatically wrap inside a table.
#         """
#         return Paragraph(str(data), self.styles['Left'])
#
#     def __convert_data(self, data):
#         """
#         Convert the list of dictionaries to a list of list to create
#         the PDF table.
#         """
#         # Create 2 separate lists in the same order: one for the
#         # list of keys and the other for the names to display in the
#         # table header.
#         keys, names = zip(*[[k, n] for k, n in self.fields])
#         new_data = [names]
#
#         for d in data:
#             new_data.append([d[k] for k in keys])
#
#         return new_data
