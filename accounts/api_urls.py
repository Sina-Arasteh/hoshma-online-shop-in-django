# from django.urls import path
# from . import api_views, forms
# from django.contrib.auth import views as auth_views

# app_name = "api_accounts"
# urlpatterns = [
#     path("signup-login/", api_views.SignUpLoginView.as_view(), name='signup-login'),
#     path(
#         "login/",
#         api_views.CustomLoginView.as_view(
#             authentication_form=forms.CustomAuthenticationForm,
#             template_name="accounts/login.html"
#         ),
#         name='login'
#     ),
#     path("signup/", api_views.SignUpView.as_view(), name='signup'),
# ]
