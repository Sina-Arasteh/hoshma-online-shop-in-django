from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import re
from . import constants


class Address(models.Model):
    province = models.CharField("استان", max_length=30, choices=constants.PROVINCE_CHOICES)
    city = models.CharField('شهر', max_length=20)
    street = models.CharField('خیابان', max_length=20)
    alley = models.CharField('کوچه', max_length=20)
    number = models.CharField('پلاک', max_length=3)
    zip_code = models.CharField('کدپستی', max_length=10)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"
    
    def __str__(self):
        return f"{self.province}/{self.city}/{self.street}/{self.alley}/{self.number}"


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="customer",
        verbose_name="کاربر"
    )
    phone_number = models.CharField(
        "شماره موبایل",
        max_length=11,
        validators=[RegexValidator(regex=r"^09\d{9}$", flags=re.A)],
        blank=True
    )
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="آدرس")

    class Meta:
        verbose_name = "سایر مشخصات"
    
    def __str__(self):
        return self.user.username
