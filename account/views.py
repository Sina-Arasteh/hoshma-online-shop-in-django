from django.shortcuts import render
from django.views import View
from . import forms, models, serializers
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import views as auth_views, login
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class SignUpLoginAPIView(APIView):
    def post(self, request):
        user_input = request.data.get('email_phone')
        if not user_input:
            return Response({'error': _("Please don't leave the field empty."), 'user_input': None}, status=status.HTTP_400_BAD_REQUEST)

        email_serializer = serializers.EmailAddressSerializer(data={'email': user_input})
        phone_serializer = serializers.PhoneNumberSerializer(data={'phone': user_input})

        if email_serializer.is_valid():
            try:
                user = User.objects.get(email__iexact=email_serializer.validated_data['email'])
                return Response({'user': True, 'username': user.username,}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'user': False, 'email': email_serializer.validated_data['email'],}, status=status.HTTP_404_NOT_FOUND)
        
        elif phone_serializer.is_valid():
            try:
                customer = models.Customer.objects.get(phone=phone_serializer.validated_data['phone'])
                return Response({'user': True, 'username': customer.user.username,}, status=status.HTTP_200_OK)
            except models.Customer.DoesNotExist:
                return Response({'user': False, 'phone': phone_serializer.validated_data['phone'],}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': _("What you have entered is not a valid Email or Phone."), 'user_input': user_input}, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    def post(self, request):
        signup_serializer = serializers.SignUpSerializer(data=request.data)
        if signup_serializer.is_valid():
            new_user = signup_serializer.save()
            if signup_serializer.validated_data.get('phone'):
                new_user.customer.phone = signup_serializer.validated_data.get('phone')
                new_user.customer.save()
                # login(request, new_user)
            return Response({'username': new_user.username}, status=status.HTTP_201_CREATED)
        return Response({'errors': signup_serializer.errors, 'user_inputs': request.data}, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(auth_views.LoginView):
    def get_initial(self):
        initial = super().get_initial()
        username = self.request.GET.get('username')
        if username:
            initial['username'] = username
        return initial
