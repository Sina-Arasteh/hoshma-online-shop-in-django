from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path('signup-login/', views.SignUpLogIn.as_view(), name='signup-login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('checkout/', views.Checkout.as_view(), name="checkout"),
    path('checkout/cancellation/<int:pk>/', views.OrderCancellation.as_view(), name="order-cancellation"),
    path('address/addition/', views.AddAddress.as_view(), name='add-address'),
    path('address/removal/<int:pk>/', views.RemoveAddress.as_view(), name='remove-address'),
    path('payment/<int:pk>/', views, name='payment'),
    path('account/', views.Account.as_view(), name='account'),
]
