from django.contrib import admin
from django.apps import apps
from .models import Customer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


models = apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


admin.site.unregister(User)
admin.site.unregister(Customer)


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [Customer]
