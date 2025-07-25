from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import re
from . import constants
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    province = models.CharField(
        _("Province"),
        max_length=30,
        choices=constants.PROVINCE_CHOICES
    )
    city = models.CharField(
        _("City"),
        max_length=20
    )
    street = models.CharField(
        _("Street"),
        max_length=20
    )
    alley = models.CharField(
        _("Alley"),
        max_length=20
    )
    # Translators: By 'Number' here means the number in Addresses.
    number = models.CharField(
        _("Number"),
        max_length=3
    )
    zip_code = models.CharField(
        _("Zip Code"),
        max_length=10
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
    
    def __str__(self):
        return f"{self.province}/{self.city}/{self.street}/{self.alley}/{self.number}"


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="customer",
        verbose_name=_("User")
    )
    phone = models.CharField(
        _("Phone"),
        max_length=11,
        validators=[RegexValidator(regex=r"^09\d{9}$", flags=re.A)],
        blank=True
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Address")
    )

    class Meta:
        verbose_name = _("Contact Information")
    
    def __str__(self):
        return self.user.username
