from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/store/', include("store.urls")),
    path('api/accounts/', include("accounts.urls")),
]
