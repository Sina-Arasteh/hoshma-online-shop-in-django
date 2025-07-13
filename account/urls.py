from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("signup-login/", views.SignUpLoginView.as_view(), name="signup-login"),
]
