from django.db import models
from django.core.validators import RegexValidator
import re
from . import constants
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from shop import models as shop_models


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
    number = models.CharField(
        # Translators: By 'Number' here means the number in Addresses.
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


class ContactInfo(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="contact_info",
        verbose_name=_("User")
    )
    phone = models.CharField(
        _("Phone"),
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r"^09\d{9}$", flags=re.A)],
        blank=True
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Address"),
        related_name="users"
    )

    class Meta:
        verbose_name = _("Contact Information")
    
    def __str__(self):
        return self.user.username


class Order(models.Model):
    products = models.ManyToManyField(
        shop_models.Product,
        verbose_name=_("Products")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("User")
    )
    creation = models.DateTimeField(
        _("Creation"),
        auto_now_add=True
    )
    last_modification = models.DateTimeField(
        _("Last Modification"),
        auto_now=True,
        editable=False
    )

    class Meta:
        ordering = ["-creation"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
