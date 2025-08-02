from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class EmailAddressSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5, max_length=254)

class PhoneNumberSerializer(serializers.Serializer):
    phone = serializers.RegexField(regex=r"^09\d{9}$")
