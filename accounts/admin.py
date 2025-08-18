from django.contrib import admin
from django.apps import apps
from .models import ContactInfo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models
from shop import models as shop_models


admin.site.register(models.Address)
admin.site.register(shop_models.Category)
admin.site.register(shop_models.Discount)
admin.site.register(shop_models.Image)
admin.site.register(shop_models.Order)
admin.site.register(shop_models.Product)
admin.site.register(shop_models.Tag)


class ContactInfoInline(admin.StackedInline):
    model = ContactInfo
    can_delete = False


admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ContactInfoInline]
