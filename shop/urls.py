from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
# from django.conf.urls.static import static   # Remove me
# from config import settings   # Remove me


app_name = "shop"
urlpatterns = [
    path(
        '',
        cache_page(0)(views.Index.as_view()),
        name="products"
    ),
    path(
        'product/<int:pk>/',
        views.ProductDetail.as_view(),
        name="product-detail"
    ),
    path(
        'category/<int:pk>/',
        cache_page(60 * 5)(views.CategoryProducts.as_view()),
        name="category-products"
    ),
]

# urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # Remove me
