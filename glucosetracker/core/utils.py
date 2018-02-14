from django.contrib.auth.models import User

# TODO create a currency-base by user setting function - allow for USD, CAD, etc. conversions
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def calc_hba1c(value):
    """
    Calculate the HbA1c from the given average blood glucose value.

    This formula is the same one used by Accu-Chek:
    https://www.accu-chek.com/us/glucose-monitoring/a1c-calculator.html#
    """
    if value:
        return ((46.7 + value) / 28.7)
    else:
        return 0


def round_value(value):
    """
    Round the given value to 1 decimal place.

    If the value is 0 or None, then simply return 0.
    """
    if value:
        return round(float(value), 1)
    else:
        return 0


def percent(part, whole):
    """
    Get the percentage of the given values.

    If the the total/whole is 0 or none, then simply return 0.
    """
    if whole:
        return round_value(100 * float(part) / float(whole))
    else:
        return 0


def to_mmol(value):
    """
    Convert a given value in mg/dL to mmol/L rounded to 1 decimal place.
    """
    return round((float(value) / 18.018), 1)


def to_mg(value):
    """
    Convert a given value in mmol/L to mg/dL rounded to nearest integer.
    """
    try:
        return int(round((float(value) * 18.018), 0))
    except ValueError:
        # We're catching ValueError here as some browsers like Firefox won't
        # validate the input for us. We're returning the value entered as this
        # will be passed in to the Django validator which will return the
        # validation error message.
        return value


def glucose_by_unit_setting(user, value):
    """
    Return the glucose value based on the unit setting.

    Glucose values are stored in mg/dL in the database. If a user's setting
    is set to mmol/L, convert the value.
    """
    user = User.objects.get(username=user.username)
    user_settings = user.settings
    if user_settings.glucose_unit.name == 'mmol/L':
        return to_mmol(value)
    else:
        return value
