from django.urls import path
from . import views, forms
from django.contrib.auth import views as auth_views

app_name = "accounts"
urlpatterns = [
    path("signup-login/", views.SignUpLoginView.as_view(), name='signup-login'),
    path(
        "login/",
        views.CustomLoginView.as_view(
            authentication_form=forms.CustomAuthenticationForm,
            template_name="accounts/login.html"
        ),
        name='login'
    ),
    path("signup/", views.SignUpView.as_view(), name='signup'),
]
