from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password


class EmailAddressSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5, max_length=254)


class PhoneNumberSerializer(serializers.Serializer):
    phone = serializers.RegexField(regex=r"^09\d{9}$")


class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, min_length=3)
    last_name = serializers.CharField(max_length=50, min_length=3)
    username = serializers.RegexField(
        r"^[\w.@+-]+$",
        max_length=150,
        min_length=4,
        error_messages = {'invalid': _('Username may contain alphanumeric, _, @, +, . and - characters.')}
    )
    email = serializers.EmailField(max_length=254, min_length=5, required=False)
    phone = serializers.RegexField(regex=r"^09\d{9}$", required=False)
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate_username(self, value):
        """Ensure the username is unique (case-insensitive)."""
        try:
            User.objects.get(username__iexact=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError(_("The username has been registered before."))

    def validate_email(self, value):
        """Ensure the Email is unique"""
        try:
            User.objects.get(email__iexact=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError(_("The email address has been registered before."))

    def validate_phone(self, value):
        """Ensure the Phone is unique"""
        try:
            models.ContactInfo.objects.get(phone=value)
        except models.ContactInfo.DoesNotExist:
            return value
        raise serializers.ValidationError(_("The phone number has been registered before."))


    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError(_("You must provide either an email address or a phone number."))

        user = User(
            username=data['username'],
            email=data.get('email'),
        )
        validate_password(data['password'], user=user)

        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({'password_confirmation': _("Password confirmation is not correct.")})

        return data
    
    def create(self, validated_data):
        new_user = User.objects.create_user(
            validated_data.get('username'),
            email = validated_data.get('email'),
            password = validated_data.get('password'),
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
        )
        return new_user


# class signup(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name']


class AddressReadSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Address
        fields = [
            'id',
            'province',
            'city',
            'street',
            'alley',
            'number',
            'zip_code',
            'users',
        ]


class AddressReadWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = [
            'province',
            'city',
            'street',
            'alley',
            'number',
            'zip_code',
        ]


class ContactInfoSerializer(serializers.ModelSerializer):
    address = AddressReadWriteSerializer()

    class Meta:
        model = models.ContactInfo
        fields = ['user', 'phone', 'address',]
    
    def create(self, validated_data):
        address_data = validated_data.pop('address', [])
        contactinfo = models.ContactInfo.objects.create

    def update(self, instance, validated_data):
        pass


class AuthUserModelSerializer(serializers.ModelSerializer):
    pass


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
