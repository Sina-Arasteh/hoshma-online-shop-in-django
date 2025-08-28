from django import forms
from django.core.validators import RegexValidator, EmailValidator
import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from .models import ContactInfo
from django.utils.translation import gettext_lazy as _


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

    # def clean_password(self):
    #     pass

# class SignUp(forms.Form):
#     first_name = forms.CharField(label=_("First Name"), max_length=50, min_length=3)
#     last_name = forms.CharField(label=_("Last Name"), max_length=50, min_length=3)
#     username = forms.CharField( 
#         label=_("Username"),
#         max_length=150,
#         min_length=4,
#         validators=[
#             RegexValidator(
#                 regex=r"^[\w.@+-]+\Z",
#                 message="Username may contain alphanumeric, _, @, +, . and - characters.",
#                 flags=re.A
#             )
#         ]
#     )
#     email_phone = forms.CharField(
#         label="Email or Phone",
#         max_length=254
#     )
#     password = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput
#     )
#     password_confirmation = forms.CharField(
#         label=_("Password Confirmation"),
#         widget=forms.PasswordInput
#     )

#     first_name.widget.attrs.update({'class': 'form-control'})
#     last_name.widget.attrs.update({'class': 'form-control'})
#     username.widget.attrs.update({'class': 'form-control'})
#     email_phone.widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
#     password.widget.attrs.update({'class': 'form-control'})
#     password_confirmation.widget.attrs.update({'class': 'form-control'})

#     def clean_username(self):
#         """Prevents the duplication of username."""
#         username = self.cleaned_data['username']
#         try:
#             User.objects.get(username__iexact=username)
#         except User.DoesNotExist:
#             return username
#         raise ValidationError(_("The username has been registered before."))

#     def clean_email_phone(self):
#         """Checks if email or phone is duplicate"""
#         emph = self.cleaned_data['email_phone']
#         try:
#             User.objects.get(email__iexact=emph)
#         except User.DoesNotExist:
#             try:
#                 ContactInfo.objects.get(phone=emph)
#             except:
#                 return emph
#             raise ValidationError(_("The phone number has been registered before."))
#         raise ValidationError(_("The email address has been registered before."))


#     def clean_password(self):
#         """Validates the password through the password validators"""
#         password = self.cleaned_data['password']
#         try:
#             username = self.cleaned_data['username']
#         except:
#             username = None
#         try:
#             email = self.cleaned_data['email']
#         except:
#             email = None
#         user = User(
#             username=username,
#             email=email,
#         )
#         validate_password(password, user=user)
#         return password

#     def clean_password_confirmation(self):
#         """Checks the similarity of the password_confirmation field to the password field"""
#         password_confirmation = self.cleaned_data['password_confirmation']
#         try:
#             password = self.cleaned_data['password']
#         except:
#             password = None
#         if password_confirmation != password:
#             raise ValidationError(_("Password confirmation is not correct."))
#         return password_confirmation


# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
#         self.fields['username'].widget.attrs.pop('autofocus', None)
#         self.fields['password'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
