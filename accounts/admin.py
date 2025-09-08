from django.contrib import admin
from . import models
from shop import models as shop_models
# from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


admin.site.register(models.CustomUser)
admin.site.register(models.Address)
admin.site.register(models.Order)

admin.site.register(shop_models.Category)
admin.site.register(shop_models.Discount)
admin.site.register(shop_models.Tag)
admin.site.register(shop_models.Product)
admin.site.register(shop_models.MainImage)
admin.site.register(shop_models.Image)

admin.site.site_header = _("Hoshma Admin Site")
admin.site.site_title = _("Hoshma Admin Site")
# admin.site.index_title = _("Admin Manager")
