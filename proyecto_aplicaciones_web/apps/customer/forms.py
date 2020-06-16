import string

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from oscar.apps.customer.utils import get_password_reset_url, normalise_email
from oscar.core.compat import (
    existing_user_fields, get_user_model, url_has_allowed_host_and_scheme)
from oscar.core.loading import get_class, get_model, get_profile_class
from oscar.forms import widgets

from oscar.apps.customer.views import EmailUserCreationForm as CoreEmailUserCreationForm

CustomerDispatcher = get_class('customer.utils', 'CustomerDispatcher')
ProductAlert = get_model('customer', 'ProductAlert')
User = get_user_model()

class EmailUserCreationForm(CoreEmailUserCreationForm):
    email = forms.EmailField(label=_('Email address'))
    first_name = forms.CharField(label=_('First Name'), required=True, max_length=30)
    last_name = forms.CharField(label=_('Last Name'), required=True, max_length=30)
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Confirm password'), widget=forms.PasswordInput)
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username',)

    def __init__(self, host=None, *args, **kwargs):
        self.host = host
        super().__init__(*args, **kwargs)

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        # Validate after self.instance is updated with form data
        # otherwise validators can't access email
        # see django.contrib.auth.forms.UserCreationForm
        if password:
            try:
                validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def clean_email(self):
        """
        Checks for existing users with the supplied email address.
        """
        email = normalise_email(self.cleaned_data['email'])
        if User._default_manager.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                _("A user with that email address already exists"))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        return password2

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and url_has_allowed_host_and_scheme(url, self.host):
            return url
        return settings.LOGIN_REDIRECT_URL

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if 'username' in [f.name for f in User._meta.fields]:
            user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user

