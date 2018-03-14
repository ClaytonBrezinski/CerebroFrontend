from django import forms
from django.urls import reverse
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions
from timezone_field import TimeZoneFormField

from glucoses.models import Category, Unit

from .validators import validate_email_unique, validate_username_unique


class NameModelChoiceField(forms.ModelChoiceField):
    """
    Overrides the default ModelChoiceField such that it will display the name of each individual object within the model
    instead of the name of the model .
    ex) instead of ModelChoiceField(Unit.Object.Field, ...)   => Unit object
    you get NameModelChoiceField(Unit.Object.Field, ....)     => mL, L, etc.
    """

    def label_from_instance(self, obj):
        return obj.get_name()


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30, validators=[validate_username_unique])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=75, validators=[validate_email_unique])
    glucose_unit = NameModelChoiceField(Unit.objects.all(), empty_label=None, label='Glucose Unit')
    time_zone = TimeZoneFormField(label='Time Zone')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-md-8 col-lg-8'

        self.helper.layout = Layout(Fieldset('Create Your Account',
                                             Field('username', autofocus=True),
                                             Field('password'),
                                             Field('email'),
                                             # Field('glucose_unit'),
                                             # Field('time_zone'),
                                             ),
                                    FormActions(
                                            Submit('submit', 'Create My Account', css_class='btn-success pull-right')),
                                    )


class UserSettingsForm(forms.Form):
    """
    Form to allow users to change profile settings and preferences.
    """
    username = forms.CharField(required=False)
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.EmailField(label='Email')
    time_zone = TimeZoneFormField(label='Time Zone')

    # glucose_unit = NameModelChoiceField(Unit.objects.all(), label='Primary Currency', empty_label=None)
    # default_category = NameModelChoiceField(Category.objects.all(), label='Default Category', empty_label='Auto',
    #                                         required=False)
    #
    # glucose_low = forms.DecimalField(label='MarketCap % Drop', max_digits=6, max_value=3000, min_value=0,
    #                                  help_text="-% change in market cap before alert email")
    # glucose_high = forms.DecimalField(label='MarketCap % Rise', max_digits=6, max_value=3000, min_value=0,
    #                                   help_text="+% change in market cap before alert email")
    # glucose_target_min = forms.DecimalField(label='Sentiment change %', max_digits=6, max_value=3000, min_value=0,
    #                                         help_text="change in currency's sentiment before alert email")
    # glucose_target_max = forms.DecimalField(label='Volume change %', max_digits=6, max_value=3000, min_value=0,
    #                                         help_text="change in currency's volume change before alert email")

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-6'
        self.helper.label_class = 'col-xs-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-md-8 col-lg-8'
        self.helper.help_text_inline = False

        self.helper.layout = Layout(
                HTML('''
            {% if messages %}
            {% for message in messages %}
            <p {% if message.tags %} class="alert alert-{{ message.tags }}"\
            {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
            </p>
            '''),
                Fieldset('Profile',
                         Field('username', readonly=True),
                         Field('email'),
                         Field('first_name'),
                         Field('last_name'),
                         Field('time_zone'),
                         ),
                # Fieldset('Preferences',
                #          Field('glucose_unit'),
                #          Field('default_category'),
                #          ),
                Fieldset('Email Alert Parameters ',
                         Field('glucose_low'),
                         Field('glucose_high'),
                         Field('glucose_target_min'),
                         Field('glucose_target_max'),
                         ),
                FormActions(Submit('submit', 'Save'),
                            Button('cancel', 'Cancel', onclick='location.href="%s";' % reverse('dashboard')), ),
                )

    def clean_email(self):
        """
        Validates the email field.

        Check if the email field changed. If true, check whether the new email
        address already exists in the database and raise an error if it does.
        """
        email = self.cleaned_data['email']
        user = User.objects.get(username=self.cleaned_data['username'])

        if email.lower() != user.email.lower():
            if User.objects.filter(email__iexact=email):
                raise forms.ValidationError('Another account is already using '
                                            'this email address.')

        return email
