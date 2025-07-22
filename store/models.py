from django.db import models
from . import constants, validators
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField("نام", max_length=30, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name


class Discount(models.Model):
    type = models.CharField("نوع تخفیف", max_length=10, choices=constants.DISCOUNT_CHOICES)
    discount = models.IntegerField("میزان تخفیف")
    start = models.DateTimeField("شروع تخفیف", validators=[validators.not_in_past_validator,])
    end = models.DateTimeField("پایان تخفیف")

    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیف‌ها"

    def clean(self):
        super().clean()
        if self.start < self.end:
            raise ValidationError({'end': "تاریخ و زمان پایان تخفیف نمی‌تواند قبل از تاریخ و زمان شروع تخفیف باشد."})

    def __str__(self):
        return self.pk


class Tag(models.Model):
    name = models.CharField("تگ", max_length=30, unique=True)

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"

    def __str__(self):
        return self.name


def product_images_upload_to(instance, filename):
    return f"{slugify(instance.product.title)}/{filename}"

class Image(models.Model):
    image = models.ImageField("تصویر", upload_to=product_images_upload_to)

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"

    def __str__(self):
        return f"Image for {self.product.title}"


def product_main_image_upload_to(instance, filename):
    return f"{slugify(instance.title)}/{filename}"

class Product(models.Model):
    title = models.CharField("عنوان", max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="دسته‌بندی")
    main_image = models.ImageField("تصویر اصلی", upload_to=product_main_image_upload_to)
    images = models.ManyToManyField(Image, verbose_name="تصاویر")
    price = models.IntegerField("قیمت")
    discount = models.OneToOneField(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="تخفیف")
    description_brief = models.TextField("توضیحات")
    description = models.TextField("توضیحات کامل")
    stock = models.IntegerField("موجودی")
    slug = models.SlugField(max_length=250)
    creation = models.DateTimeField("تاریخ/زمان ایجاد", auto_now_add=True)
    last_modification = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالا‌ها"

    def __str__(self):
        return self.title


class Order(models.Model):
    products = models.ManyToManyField(Product, verbose_name="کالاها")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    creation = models.DateTimeField("تاریخ/زمان ایجاد", auto_now_add=True)
    total_price = models.IntegerField('مجموع قیمت‌ها')

    class Meta:
        ordering = ["-creation"]
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
