from django.db import models
from . import constants, validators
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=30,
        unique=True
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True
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

    def get_parent_hierarchy(self):
        parent = self.parent
        parents = list()
        while parent:
            parents.append(parent.name)
            parent = parent.parent
        return "/".join(reversed(parents))

    def __str__(self):
        parents = self.get_parent_hierarchy()
        return f"{parents}/{self.name}" if parents else self.name


class Discount(models.Model):
    type = models.CharField(
        _('Type'),
        max_length=10,
        choices=constants.DISCOUNT_CHOICES
    )
    discount = models.IntegerField(_("Amount"))
    start = models.DateTimeField(
        _("Start"),
        validators=[validators.not_in_past_validator,]
    )
    end = models.DateTimeField(_("End"))

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def clean(self):
        super().clean()
        if self.start < self.end:
            raise ValidationError({'end': _("Please set a date and time after the date and time of the start.")})

    def __str__(self):
        return self.pk


class Tag(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=30,
        unique=True
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


def product_images_upload_to(instance, filename):
    return f"{slugify(instance.product.title)}/{filename}"

class Image(models.Model):
    image = models.ImageField(
        _("Image"),
        upload_to=product_images_upload_to
    )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return f"Image for {self.product.title}"


def product_main_image_upload_to(instance, filename):
    return f"{slugify(instance.title)}/{filename}"

class Product(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=250,
        unique=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Category")
    )
    main_image = models.ImageField(
        _("Main Image"),
        upload_to=product_main_image_upload_to
    )
    images = models.ManyToManyField(
        Image,
        verbose_name=_("Images")
    )
    price = models.IntegerField(_("Price"))
    discount = models.OneToOneField(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Discount")
    )
    description_brief = models.TextField(_("Brief Description"))
    description = models.TextField(_("Description"))
    stock = models.IntegerField(_("Stock"))
    slug = models.SlugField(max_length=250)
    creation = models.DateTimeField(
        _("Creation"),
        auto_now_add=True
    )
    last_modification = models.DateTimeField(
        _("Last Modification"),
        auto_now=True
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title


class Order(models.Model):
    products = models.ManyToManyField(
        Product,
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
    total_price = models.IntegerField(_("Total Price"))

    class Meta:
        ordering = ["-creation"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
