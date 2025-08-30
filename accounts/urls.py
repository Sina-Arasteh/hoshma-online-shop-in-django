from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path('checkout/', views.Checkout.as_view(), name="checkout"),
    path('payment/<int:pk>/', views, name='payment'),
    path('account/', views.Account.as_view(), name='account'),
    path('signup-login/', views.SignUpLogIn.as_view(), name='signup-login'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
