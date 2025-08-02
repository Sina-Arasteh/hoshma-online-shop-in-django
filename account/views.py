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
                user = User.objects.get(email=email_serializer.validated_data['email'])
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


class SignUpView(View):
    def post(self, request):
        email_form = forms.EmailAddressForm({'email': request.POST.get('email_phone')})
        phone_form = forms.PhoneNumberForm({'phone': request.POST.get('email_phone')})

        if email_form.is_valid():
            signup_form = forms.SignUp(request.POST)
            if signup_form.is_valid():
                new_user = User.objects.create_user(
                    signup_form.cleaned_data['username'],
                    email=signup_form.cleaned_data['email_phone'],
                    password=signup_form.cleaned_data['password']
                )
                new_user.first_name = signup_form.cleaned_data['first_name']
                new_user.last_name = signup_form.cleaned_data['last_name']
                new_user.save()
                login(request, new_user)
                return HttpResponseRedirect(reverse("store:index-page"))
            context = {'signup_form': signup_form}
            return render(request, 'account/signup.html', context)

        elif phone_form.is_valid():
            signup_form = forms.SignUp(request.POST)
            if signup_form.is_valid():
                new_user = User.objects.create_user(
                    signup_form.cleaned_data['username'],
                    password=signup_form.cleaned_data['password']
                )
                new_user.first_name = signup_form.cleaned_data['first_name']
                new_user.last_name = signup_form.cleaned_data['last_name']
                new_user.save()
                new_user.customer.phone = signup_form.cleaned_data['email_phone']
                new_user.customer.save()
                login(request, new_user)
                return HttpResponseRedirect(reverse("store:index-page"))
            context = {'signup_form': signup_form}
            return render(request, 'account/signup.html', context)

        context = {
            'signup_form': signup_form,
            'emph_error': _("What you have entered is not a valid Email or Phone."),
        }
        return render(request, 'account/signup.html', context)


# class SignUpView(View):
#     def get(self, request):
#         context = {'signup_form': forms.SignUp(initial={'email_phone': request.GET.get('email_phone'),}),}
#         return render(request, 'account/signup.html', context)

#     def post(self, request):
#         email_form = forms.EmailAddressForm({'email': request.POST.get('email_phone')})
#         phone_form = forms.PhoneNumberForm({'phone': request.POST.get('email_phone')})

#         if email_form.is_valid():
#             signup_form = forms.SignUp(request.POST)
#             if signup_form.is_valid():
#                 new_user = User.objects.create_user(
#                     signup_form.cleaned_data['username'],
#                     email=signup_form.cleaned_data['email_phone'],
#                     password=signup_form.cleaned_data['password']
#                 )
#                 new_user.first_name = signup_form.cleaned_data['first_name']
#                 new_user.last_name = signup_form.cleaned_data['last_name']
#                 new_user.save()
#                 login(request, new_user)
#                 return HttpResponseRedirect(reverse("store:index-page"))
#             context = {'signup_form': signup_form}
#             return render(request, 'account/signup.html', context)

#         elif phone_form.is_valid():
#             signup_form = forms.SignUp(request.POST)
#             if signup_form.is_valid():
#                 new_user = User.objects.create_user(
#                     signup_form.cleaned_data['username'],
#                     password=signup_form.cleaned_data['password']
#                 )
#                 new_user.first_name = signup_form.cleaned_data['first_name']
#                 new_user.last_name = signup_form.cleaned_data['last_name']
#                 new_user.save()
#                 new_user.customer.phone = signup_form.cleaned_data['email_phone']
#                 new_user.customer.save()
#                 login(request, new_user)
#                 return HttpResponseRedirect(reverse("store:index-page"))
#             context = {'signup_form': signup_form}
#             return render(request, 'account/signup.html', context)

#         context = {
#             'signup_form': signup_form,
#             'emph_error': _("What you have entered is not a valid Email or Phone."),
#         }
#         return render(request, 'account/signup.html', context)


class CustomLoginView(auth_views.LoginView):
    def get_initial(self):
        initial = super().get_initial()
        username = self.request.GET.get('username')
        if username:
            initial['username'] = username
        return initial
