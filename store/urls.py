from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='category'),
]
