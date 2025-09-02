from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
    path('add/<int:pk>/', views.Add.as_view(), name="add"),
    path('', views.CartPage.as_view(), name='cart'),
]
