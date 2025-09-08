from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models
from shop import models as shop_models


admin.site.register(models.CustomUser)
admin.site.register(models.Address)
admin.site.register(models.Order)

admin.site.register(shop_models.Category)
admin.site.register(shop_models.Discount)
admin.site.register(shop_models.Coupon)
admin.site.register(shop_models.Tag)
admin.site.register(shop_models.Product)
admin.site.register(shop_models.MainImage)
admin.site.register(shop_models.Image)
