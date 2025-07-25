from django.shortcuts import render
from django.views import View
from . import forms, models
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import views as auth_views, login
from django.utils.translation import gettext as _


class SignUpLoginView(View):
    def get(self, request):
        return render(request, "account/signup_login.html")
    
    def post(self, request):
        email_form = forms.EmailAddressForm({'email': request.POST.get('email_phone'),})
        phone_form = forms.PhoneNumberForm({'phone': request.POST.get('email_phone'),})

        if email_form.is_valid():
            try:
                user = User.objects.get(email=email_form.cleaned_data['email'])
                return HttpResponseRedirect(reverse('account:login', query={'username': user.username,}))
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('account:signup', query={'email_phone': email_form.cleaned_data['email'],}))
        
        elif phone_form.is_valid():
            try:
                customer = models.Customer.objects.get(phone=phone_form.cleaned_data['phone'])
                return HttpResponseRedirect(reverse('account:login', query={'username': customer.user.username,}))
            except models.Customer.DoesNotExist:
                return HttpResponseRedirect(reverse('account:signup', query={'email_phone': phone_form.cleaned_data['phone'],}))
        
        context = {'emph_error': _("What you have entered is not a valid Email or Phone.")}
        return render(request, "account/signup_login.html", context)


class SignUpView(View):
    def get(self, request):
        context = {'signup_form': forms.SignUp(initial={'email_phone': request.GET.get('email_phone'),}),}
        return render(request, 'account/signup.html', context)

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


class CustomLoginView(auth_views.LoginView):
    def get_initial(self):
        initial = super().get_initial()
        username = self.request.GET.get('username')
        if username:
            initial['username'] = username
        return initial
