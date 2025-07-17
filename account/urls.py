from django.urls import path
from . import views, forms
from django.contrib.auth import views as auth_views

app_name = "account"
urlpatterns = [
    path("signup-login/", views.SignUpLoginView.as_view(), name='signup-login'),
    path("login/", auth_views.LoginView.as_view(authentication_form=forms.CustomAuthenticationForm), name='login'),
    path("signup/", views.SignUpView.as_view(), name='signup'),
]
