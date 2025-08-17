from django.contrib import admin
from django.apps import apps
from .models import ContactInformation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models
from store import models as store_models


admin.site.register(models.Address)
admin.site.register(store_models.Category)
admin.site.register(store_models.Discount)
admin.site.register(store_models.Image)
admin.site.register(store_models.Order)
admin.site.register(store_models.Product)
admin.site.register(store_models.Tag)


class ContactInformationInline(admin.StackedInline):
    model = ContactInformation
    can_delete = False


admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ContactInformationInline]
