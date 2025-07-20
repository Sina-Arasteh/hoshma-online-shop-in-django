from django.contrib import admin
from django.apps import apps
from .models import Customer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from . import models
from store import models as store_models


# models = apps.get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass


# admin.site.unregister(Customer)

admin.site.register(models.Address)
admin.site.register(store_models.Category)
admin.site.register(store_models.Discount)
admin.site.register(store_models.Image)
admin.site.register(store_models.Order)
admin.site.register(store_models.Product)
admin.site.register(store_models.Tag)


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False


admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [CustomerInline]
