from django.db import models
from . import constants, validators
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
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
        on_delete=models.CASCADE,
        null=True,
        related_name='children'
    )
    hierarchy = models.PositiveIntegerField(editable=False, default=0)  # The hierarchy of a root category equals 0.

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        indexes = [
            models.Index(fields=['hierarchy',]),
        ]

    def save(self, *args, **kwargs):
        count = 0
        parent = self.parent
        while parent:
            count += 1
            parent = parent.parent
        self.hierarchy = count
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.parent == self:
            raise ValidationError({'parent': _("A category cannot be set as a parent for itself.")})
        
        ancestor = self.parent
        while ancestor:
            if ancestor == self:
                raise ValidationError({'parent': _("Circular parent relationship detected.")})
            ancestor = ancestor.parent

    def get_parents_hierarchy(self):
        parent = self.parent
        parents = list()
        while parent:
            parents.append(parent.id)
            parent = parent.parent
        parents.reverse()
        return parents

    def get_children(self):
        """This method retrieves all the direct and grand children."""
        children = list()
        def collect_children(category):
            for child in category.children.all():
                children.append(child)
                collect_children(child)
        collect_children(self)
        return children
    
    def get_all_children_products(self):
        children = self.get_children()
        products = set()
        for child in children:
            products.update(product.id for product in child.products.all())
        return sorted(list(products))

    def __str__(self):
        all_parents = self.get_parents_hierarchy()
        parents = list()
        for parent in all_parents:
            parents.append(parent.name)
        parents = "/".join(parents)
        return f"{parents}/{self.name}" if parents else f"{self.name}"

class Discount(models.Model):
    type = models.CharField(
        _('Type'),
        max_length=10,
        choices=constants.DISCOUNT_CHOICES
    )
    amount = models.PositiveIntegerField(
        _("Amount"),
        validators=[validators.validate_positive_value,]
    )
    start = models.DateTimeField(
        _("Start"),
        validators=[validators.validate_not_in_past,]
    )
    end = models.DateTimeField(
        _("End"),
        validators=[validators.validate_not_in_past,]
    )

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

    def clean(self):
        super().clean()

        if self.type == "percentage" and self.amount > 100:
            raise ValidationError({'amount': _("Amount cannot be more than 100 while the discount type is percentage.")})

        if self.start >= self.end:
            raise ValidationError({'end': _("Please set a date and time after the date and time of the start.")})

    def __str__(self):
        return f"{self.type}: {self.amount}"

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

class Product(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=250,
        unique=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
        verbose_name=_("Category")
    )
    price = models.PositiveIntegerField(
        _("Price")
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Discount"),
        related_name='products'
    )
    tags = models.ManyToManyField(Tag, related_name="products")
    description_brief = models.TextField(_("Brief Description"))
    description = models.TextField(_("Description"))
    stock = models.PositiveIntegerField(
        _("Stock"),
        default=0
    )
    # slug = models.SlugField(
    #     max_length=250,
    #     editable=False
    # )
    creation = models.DateTimeField(
        _("Creation"),
        auto_now_add=True,
        editable=False
    )
    last_modification = models.DateTimeField(
        _("Last Modification"),
        auto_now=True,
        editable=False
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def get_final_price(self):
        if self.discount:
            if self.discount.type == "fixed":
                final_price = self.price - self.discount.amount
                return final_price if final_price > 0 else 0
            final_price = self.price - (self.price * self.amount / 100)
            return final_price
        return self.price

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("shop:product-detail", kwargs={"pk": self.pk})

class MainImage(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='main_image',
        primary_key=True
    )
    image = models.ImageField(
        _("Main Image"),
        upload_to=product_main_image_upload_to
    )
    alt = models.CharField(max_length=100)

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
        max_length=100,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return f"Image for {self.product.id}"
