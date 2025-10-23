from django.db import models
from . import validators
from .constants import PHONE_BRANDS
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


def product_main_image_upload_to(instance, filename):
    return f"products/{slugify(instance.title)}/main_image/{filename}"

def product_images_upload_to(instance, filename):
    return f"products/{slugify(instance.product.title)}/{filename}"


class Category(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=30,
        unique=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        verbose_name=_("Parent"),
        related_name='children'
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def clean(self):
        super().clean()

        if self.parent == self:
            raise ValidationError({'parent': _("A category cannot be set as a parent for itself.")})
        
        ancestor = self.parent
        while ancestor:
            if ancestor == self:
                raise ValidationError({'parent': _("Circular parent relationship detected.")})
            ancestor = ancestor.parent

    def get_parents(self):
        parent = self.parent
        parents = list()
        while parent:
            parents.append(parent)
            parent = parent.parent
        parents.reverse()
        return parents
    
    def has_children(self):
        return bool(self.children)

    def __str__(self):
        parents = "/".join([p.name for p in self.get_parents()])
        return f"{parents} / {self.name}" if parents else self.name

class GlobalDiscount(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=150,
        unique=True
    )
    percentage = models.PositiveIntegerField(
        _("Percentage"),
        validators=[
            MinValueValidator(
                1,
                message=_("The percentage of the global discount should start from 1%.")
            ),
            MaxValueValidator(
                100,
                message=_("The percentage of the global discount cannot be greater than 100%")
            ),
        ]
    )
    start_date = models.DateField(
        _("Start Date"),
        validators=[validators.validate_not_in_past,]
    )
    end_date = models.DateField(
        _("End Date"),
        validators=[validators.validate_not_in_past,]
    )

    class Meta:
        verbose_name = _("Global Discount")
        verbose_name_plural = _("Global Discounts")

    def clean(self):
        super().clean()

        if self.start_date >= self.end_date:
            raise ValidationError({'end_date': _("End date cannot be sooner than the start date.")})

    def __str__(self):
        return self.name

# class Coupon(models.Model):
#     pass

class Product(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=150,
        unique=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="%(class)ss",
        verbose_name=_("Category"),
        null=True
    )
    price = models.PositiveIntegerField(_("Price"))
    discount = models.PositiveIntegerField(
        _("Discount"),
        null=True,
        blank=True,
        validators=[
            MinValueValidator(
                1,
                message=_("The percentage of the discount should start from 1%.")
            ),
            MaxValueValidator(
                100,
                message=_("The percentage of the discount cannot be greater than 100%")
            ),
        ]
    )
    global_discount = models.ForeignKey(      # Set this field to null automatically when the global_discount.end_date has been expired.
        GlobalDiscount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Global Discount"),
        related_name="%(class)ss"
    )
    product_description = models.TextField(
        _("Product Description"),
        max_length=2000
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True
    )

    class Meta:
        abstract = True
    
    def clean(self):
        super().clean()

        if self.category.has_children():
            raise ValidationError({'category': _("Categories with child (or children) are not permissible.")})

    def get_final_price(self):
        final_price = self.price
        if self.discount:
            final_price -= final_price * self.discount / 100
        if self.global_discount and self.global_discount.start_date <= timezone.now().date() <= self.global_discount.end_date:
            final_price -= final_price * self.global_discount.percentage / 100
        return final_price

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse("shop:product-detail", kwargs={"pk": self.pk})

class Phone(Product):
    brand = models.CharField(
        _("Brand"),
        max_length=50,
        choices=PHONE_BRANDS
    )
    os = models.CharField(
        _("Operating System"),
        max_length=20
    )
    internal_storage = models.CharField(
        _("Internal Storage"),
        max_length=20
    )
    connectivity_networks = models.CharField(
        _("Connectivity Networks"),
        max_length=20
    )
    rear_cameras_number = models.CharField(_("Rear Cameras Number"))
    guarantee = models.CharField(
        _("Guarantee"),
        max_length=100
    )
    # specifications = models.
    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")

class PhoneColorVariant(models.Model):
    phone = models.ForeignKey(
        Phone,
        on_delete=models.CASCADE,
        related_name="colors",
        verbose_name=_("Phone")
    )
    color = models.CharField(
        _("Color"),
        max_length=6
    )   # Hexadecimal Colors
    stock = models.PositiveIntegerField(
        _("Stock"),
        default=0
    )

    # def __str__(self):
    #     pass

class MainImage(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='main_image',
        primary_key=True,
        verbose_name=_("Product")
    )
    image = models.ImageField(
        _("Main Image"),
        upload_to=product_main_image_upload_to
    )
    alt = models.CharField(
        _("Alt"),
        max_length=100
    )

    class Meta:
        verbose_name = _("Main Image")
        verbose_name_plural = _("Main Images")

    def __str__(self):
        return f"Main image for {self.product.id}"

class Image(models.Model):
    image = models.ImageField(
        _("Image"),
        upload_to=product_images_upload_to
    )
    alt = models.CharField(
        _("Alt"),
        max_length=100,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Product")
    )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return f"Image for {self.product.id}"
