from django.urls import path
from . import views
from django.conf.urls.static import static   # Remove me
from config import settings   # Remove me


app_name = "shop"
urlpatterns = [
    path('', views.ProductsPage.as_view(), name="products"),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name="product-detail"),
    path('category/<int:pk>/', views.CategoryProducts.as_view(), name="category-products"),
]

urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # Remove me
