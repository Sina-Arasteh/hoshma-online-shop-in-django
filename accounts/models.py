from django.db import models
from django.core.validators import RegexValidator
import re
from . import constants
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from shop import models as shop_models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import MultipleObjectsReturned


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_staff=True and is_superuser=True."))
        
        return self.create_user(email=email, phone=phone, password=password, **extra_fields)

    def get_by_natural_key(self, natural_key):
            if not natural_key:
                return None
            try:
                return self.get(email__iexact=self.normalize_email(natural_key))
            except self.model.DoesNotExist:
                try:
                    return self.get(phone=natural_key)
                except self.model.DoesNotExist:
                    return None

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        _("Email"),
        unique=True,
        null=True,
        blank=True
    )
    phone = models.CharField(
        _("Phone"),
        max_length=11,
        validators=[RegexValidator(regex=r"^09\d{9}$", flags=re.A)],
        unique=True,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        super().clean()
        if not self.email and not self.phone:
            raise ValidationError(_("User instances need at least an email or a phone."))
        
        if (self.is_staff or self.is_superuser) and not self.email:
            raise ValidationError(_("Staff members should have an email."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email if self.email else self.phone

class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_("User")
    )
    province = models.CharField(
        _("Province"),
        max_length=30,
        choices=constants.PROVINCE_CHOICES
    )
    city = models.CharField(
        _("City"),
        max_length=60
    )
    street = models.CharField(
        _("Street"),
        max_length=60
    )
    alley = models.CharField(
        _("Alley"),
        max_length=60
    )
    number = models.CharField(
        # Translators: The 'Number' here means the number in Addresses.
        _("Number"),
        max_length=5
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

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("User")
    )
    # address = models
    creation = models.DateTimeField(
        _("Creation"),
        auto_now_add=True
    )
    status = models.CharField(
        max_length=10,
        choices=constants.ORDER_STATUS,
        verbose_name=_("Status"),
        default='pending'
    )
    customer_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-creation"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def total_price(self):
        return sum(orderitem.item_total_price() for orderitem in self.orderitems)

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='orderitems',
        verbose_name=_("Order")
    )
    product = models.ForeignKey(
        shop_models.Product,
        on_delete=models.SET_NULL,
        related_name='orderitems',
        null=True,
        verbose_name=_("Product")
    )
    price = models.PositiveIntegerField(_("Price"))
    discount = models.ForeignKey(
        shop_models.Discount,
        on_delete=models.SET_NULL,
        verbose_name=_("Discount"),
        null=True
    )
    quantity = models.PositiveIntegerField(_("Quantity"))

    def save(self, *args, **kwargs):
        self.price = self.product.get_final_price()
        self.discount = self.product.discount
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
    
    def item_total_price(self):
        return self.price * self.quantity
