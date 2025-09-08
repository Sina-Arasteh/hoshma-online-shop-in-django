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
    path('payment/<int:pk>/', views.Payment.as_view(), name='payment'),
    path('account/', views.Account.as_view(), name='account'),
    path('account/deletion/', views.AccountDeletion.as_view(), name='account-deletion'),
    path('account/password/change', views.PasswordChange.as_view(), name='password-change'),
    path('account/logout/', views, name='logout'),
]
