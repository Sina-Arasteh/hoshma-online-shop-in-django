from django.shortcuts import render
from django.views import View
from . import forms, models
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse


class SignUpLoginView(View):
    def get(self, request):
        return render(request, "account/signup_login.html")
    
    def post(self, request):
        email_form = forms.EmailAddressForm({'email': request.POST.get('email_phone')})
        phone_form = forms.PhoneNumberForm({'phone': request.POST.get('email_phone')})

        if email_form.is_valid():
            try:
                user = User.objects.get(email=email_form.cleaned_data['email'])
            except:
                user = None
            if user:
                context = {'login_form': forms.CustomAuthenticationForm({'username': user.username}),}
                return render(request, "account/login.html", context)
            context = {'signup_form': forms.SignUp({'email_phone': email_form.cleaned_data['email']})}
            return render(request, 'account/signup.html', context)
        
        elif phone_form.is_valid():
            try:
                user = models.Customer.objects.get(phone_number=phone_form.cleaned_data['phone'])
            except:
                user = None
            if user:
                context = {'login_form': forms.CustomAuthenticationForm({'username': user.user.username}),}
                return render(request, "account/login.html", context)
            context = {'signup_form': forms.SignUp({'email_phone': phone_form.cleaned_data['phone']})}
            return render(request, 'account/signup.html', context)
        
        context = {'error': "شماره موبایل یا ایمیل نادرست است."}
        return render(request, "account/signup_login.html", context)


class SignUpView(View):
    def post(self, request):
        email_form = forms.EmailAddressForm({'email': request.POST.get('email_phone')})
        phone_form = forms.PhoneNumberForm({'phone': request.POST.get('email_phone')})

        if email_form.is_valid():
            try:
                user = User.objects.get(email=email_form.cleaned_data['email'])
            except:
                user = None
            if user:
                context = {'error': "ایمیل وارد شده قبلا ثبت شده است."}
                return render(request, "account/signup_login.html", context)
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
                return HttpResponseRedirect(reverse("store:index-page"))
            context = {'signup_form': signup_form}
            return render(request, 'account/signup.html', context)

        elif phone_form.is_valid():
            try:
                user = models.Customer.objects.get(phone_number=phone_form.cleaned_data['phone'])
            except:
                user = None
            if user:
                context = {'error': "شماره موبایل وارد شده قبلا ثبت شده است."}
                return render(request, "account/signup_login.html", context)
            signup_form = forms.SignUp(request.POST)
            if signup_form.is_valid():
                new_user = User.objects.create_user(
                    signup_form.cleaned_data['username'],
                    password=signup_form.cleaned_data['password']
                )
                new_user.first_name = signup_form.cleaned_data['first_name']
                new_user.last_name = signup_form.cleaned_data['last_name']
                new_user.save()
                new_user.customer.phone_number = signup_form.cleaned_data['email_phone']
                new_user.customer.save()
                return HttpResponseRedirect(reverse("store:index-page"))
            context = {'signup_form': signup_form}
            return render(request, 'account/signup.html', context)

        context = {'error': "شماره موبایل یا ایمیل نادرست است."}
        return render(request, "account/signup_login.html", context)
