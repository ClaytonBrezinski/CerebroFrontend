import csv
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from core.utils import to_mg




DATE_FORMAT = '%Y/%m/%d'
TIME_FORMAT = '%I:%M %p'


# def import_glucose_from_csv(user, csv_file):
#     """
#     Import glucose CSV data.
#
#     We'll process all rows first and create Glucose model objects from them
#     and perform a bulk create. This way, no records will be inserted unless
#     all records are good.
#
#     Also note that we're using splitlines() to make sure 'universal newlines'
#     is used.
#
#     Assumed order: value, category, record_date, record_time, notes
#     """
#     csv_data = []
#     reader = csv.reader(csv_file.read().splitlines(), delimiter=',',
#                         quotechar='"')
#     for row in reader:
#         csv_data.append([item.strip() for item in row])
#
#     glucose_objects = []
#
#     # Check if headers exists. Skip the first entry if true.
#     header_check = ['value', 'category', 'date', 'time']
#     first_row = [i.lower().strip() for i in csv_data[0]]
#     if all(i in first_row for i in header_check):
#         csv_data = csv_data[1:]
#
#     for row in csv_data:
#         # Let's do an extra check to make sure the row is not empty.
#         if row:
#             try:
#                 category = Category.objects.get(name__iexact=row[1].strip())
#             except ObjectDoesNotExist:
#                 category = Category.objects.get(name__iexact='No Category'.strip())
#
#             # Since we always store the value in mg/dL format in the db, we need
#             # to make sure we convert it here if the user's setting is set to
#             # mmol/L.
#             if user.settings.glucose_unit.name == 'mmol/L':
#                 value = int(to_mg(row[0]))
#             else:
#                 value = int(row[0])
#
#             glucose_objects.append(Glucose(
#                 user=user,
#                 value=value,
#                 category=category,
#                 record_date=datetime.strptime(row[2], DATE_FORMAT),
#                 record_time=datetime.strptime(row[3], TIME_FORMAT),
#                 notes=row[4],
#             ))
#
#     Glucose.objects.bulk_create(glucose_objects)
#
#
# def get_initial_category(user):
#     """
#     Retrieve the default category from the user settings.
#
#     If the default category is None (labeled as 'Auto' in the settings page),
#     automatically pick the category based on time of day.
#     """
#     user = User.objects.get(username=user.username)
#     user_settings = user.settings
#     default_category = user_settings.default_category
#
#     if not default_category:
#         now = datetime.now(tz=user_settings.time_zone)
#
#         breakfast_start = now.replace(hour=4, minute=0)
#         breakfast_end = now.replace(hour=11, minute=0)
#
#         lunch_start = now.replace(hour=11, minute=0)
#         lunch_end = now.replace(hour=16, minute=0)
#
#         dinner_start = now.replace(hour=16, minute=0)
#         dinner_end = now.replace(hour=22, minute=0)
#
#         if now > breakfast_start and now < breakfast_end:
#             category_name = 'Breakfast'
#         elif now > lunch_start and now < lunch_end:
#             category_name = 'Lunch'
#         elif now > dinner_start and now < dinner_end:
#             category_name = 'Dinner'
#         else:
#             category_name = 'Bedtime'
#
#         default_category = Category.objects.get(name=category_name)
#
#     return default_category