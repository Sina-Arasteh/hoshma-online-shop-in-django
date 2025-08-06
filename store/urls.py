from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),
    path('discounts/', views.CategoryListAPIView.as_view(), name='discount-list'),
    path('discounts/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='discount-detail'),
]
