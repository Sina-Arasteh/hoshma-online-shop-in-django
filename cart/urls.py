from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
    path('add/<int:pk>/', views.Add, name="add"),
]
