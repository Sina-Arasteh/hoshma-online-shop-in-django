from django.db import models
from . import constants
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    type = models.CharField(max_length=10, choices=constants.DISCOUNT_CHOICES)
    discount = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.pk


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


def product_main_image_upload_to(instance, filename):
    return f"{slugify(instance.title)}/{filename}"

class Product(models.Model):
    title = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to=product_main_image_upload_to)
    price = models.IntegerField()
    discount = models.OneToOneField(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    description_brief = models.TextField()
    description = models.TextField()
    stock = models.IntegerField()
    slug = models.SlugField(max_length=250)
    creation = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def product_images_upload_to(instance, filename):
    return f"{slugify(instance.product.title)}/{filename}"

class Image(models.Model):
    image = models.ImageField(upload_to=product_images_upload_to)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f"Image for {self.product.title}"


class Order(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    creation = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField('مجموع قیمت‌ها')

    class Meta:
        ordering = ["-creation"]
    
