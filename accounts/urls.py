from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path('checkout/', views.Checkout.as_view(), name="checkout"),
]
