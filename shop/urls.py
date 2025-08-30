from django.urls import path
from . import views
from django.conf.urls.static import static   # Remove me
from config import settings   # Remove me


app_name = "shop"
urlpatterns = [
    path('', views.index, name="home"),
    path('product/<int:pk>/', views.product_detail, name="product-detail"),
]

urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # Remove me
