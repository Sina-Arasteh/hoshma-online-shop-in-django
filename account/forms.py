from django import forms
from django.core.validators import RegexValidator
import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer


class EmailAddressForm(forms.Form):
    email = forms.EmailField(max_length=254)


class PhoneNumberForm(forms.Form):
    phone = forms.CharField(validators=[RegexValidator(regex=r"^09\d{9}$", flags=re.A)])


class SignUp(forms.Form):
    first_name = forms.CharField(label="نام", max_length=50, min_length=3)
    last_name = forms.CharField(label="نام خانوادگی", max_length=50, min_length=3)
    username = forms.CharField( 
        label="نام کاربری",
        max_length=150,
        min_length=4,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message="فقط از حروف الفبا و اعداد انگلیسی و نمادهای [@.-_+] استفاده شود.",
                flags=re.A
            )
        ]
    )
    email_phone = forms.CharField(
        label="ایمیل / شماره موبایل",
        max_length=254
    )
    password = forms.CharField(
        label="گذرواژه",
        widget=forms.PasswordInput
    )
    password_confirmation = forms.CharField(
        label="تکرار گذرواژه",
        widget=forms.PasswordInput
    )

    first_name.widget.attrs.update({'class': 'form-control'})
    last_name.widget.attrs.update({'class': 'form-control'})
    username.widget.attrs.update({'class': 'form-control'})
    email_phone.widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
    password.widget.attrs.update({'class': 'form-control'})
    password_confirmation.widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        """Prevents the duplication of username."""
        username = self.cleaned_data['username']
        try:
            User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("نام کاربری وارد شده قبلا ثبت شده است.")

    def clean_email_phone(self):
        """Checks if email or phone is duplicate"""
        emph = self.cleaned_data['email_phone']
        try:
            User.objects.get(email__iexact=emph)
        except User.DoesNotExist:
            try:
                Customer.objects.get(phone=emph)
            except:
                return emph
            raise ValidationError("شماره موبایل وارد شده قبلا ثبت شده است.")
        raise ValidationError("ایمیل وارد شده قبلا ثبت شده است.")


    def clean_password(self):
        """Validates the password through the password validators"""
        password = self.cleaned_data['password']
        try:
            username = self.cleaned_data['username']
        except:
            username = None
        try:
            email = self.cleaned_data['email']
        except:
            email = None
        user = User(
            username=username,
            email=email,
        )
        validate_password(password, user=user)
        return password

    def clean_password_confirmation(self):
        """Checks the similarity of the password_confirmation field to the password field"""
        password_confirmation = self.cleaned_data['password_confirmation']
        try:
            password = self.cleaned_data['password']
        except:
            password = None
        if password_confirmation != password:
            raise ValidationError("تکرار گذرواژه صحیح نمی‌باشد.")
        return password_confirmation


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
        self.fields['username'].widget.attrs.pop('autofocus', None)
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
