from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("shop.urls")),
    # path('api/shop/', include("shop.api_urls")),
    # path('accounts/', include("accounts.urls")),
    # path('api/accounts/', include("accounts.api_urls")),
    path('cart/', include("cart.urls")),
]
