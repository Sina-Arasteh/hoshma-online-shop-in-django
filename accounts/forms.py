from django import forms
from django.core.validators import RegexValidator, EmailValidator
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from .models import ContactInfo
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model


user_model = get_user_model()

def get_max_password_length(default=128):
    for validator in settings.AUTH_PASSWORD_VALIDATORS:
        if validator['NAME'] == 'accounts.passsword_validators.MaximumLengthValidator':
            return validator.get('OPTIONS', {}).get('max_length', default)
    return default

class CheckoutForm(forms.Form):
    pass

class SignUpLogInForm(forms.Form):
    identifier_value = forms.CharField(max_length=254)

    def clean_identifier_value(self):
        user_input = self.cleaned_data['identifier_value']
        email_validator = EmailValidator()
        phone_validator = RegexValidator(regex=r"^09\d{9}$", flags=re.A)
        try:
            email_validator(user_input)
            self.cleaned_data['identifier_type'] = 'email'
        except ValidationError:
            try:
                phone_validator(user_input)
                self.cleaned_data['identifier_type'] = 'phone'
            except ValidationError:
                raise ValidationError(_("The user input is invalid."))
        return user_input

class LogIn(forms.Form):
    password = forms.CharField(max_length=128)

class SignUp(forms.Form):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=50,
        min_length=3
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=50,
        min_length=3
    )
    email = forms.EmailField(label=_("Email"))
    phone = forms.CharField(
        label=_("Phone"),
        max_length=11,
        validators=[RegexValidator(regex=r"^09\d{9}$", flags=re.A)]
    )
    password = forms.CharField(
        label=_("Password"),
        max_length=get_max_password_length(),
        widget=forms.PasswordInput
    )
    password_confirmation = forms.CharField(
        label=_("Password Confirmation"),
        max_length=get_max_password_length(),
        widget=forms.PasswordInput
    )

    def clean_email(self):
        """Checks if email is duplicate"""
        email = self.cleaned_data['email']
        try:
            user_model.objects.get(email__iexact=email)
        except user_model.DoesNotExist:
            return email
        raise ValidationError(_("The email address has been registered before."))

    def clean_phone(self):
        """Checks if phone is duplicate"""
        phone = self.cleaned_data['phone']
        try:
            user_model.objects.get(phone=phone)
        except user_model.DoesNotExist:
            return phone
        raise ValidationError(_("The phone number has been registered before."))

    def clean_password(self):
        """Validates the password through the password validators"""
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        user = user_model(
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name
        )
        validate_password(password, user=user)
        return password

    def clean_password_confirmation(self):
        """Checks the similarity of the password_confirmation field to the password field"""
        password_confirmation = self.cleaned_data.get('password_confirmation')
        password = self.cleaned_data.get('password')
        if password_confirmation != password:
            raise ValidationError(_("Password confirmation is not correct."))
        return password_confirmation
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
#         self.fields['username'].widget.attrs.pop('autofocus', None)
#         self.fields['password'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
