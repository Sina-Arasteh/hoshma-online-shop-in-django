from django.shortcuts import render
from django.views import View
from . import forms
from django.contrib.auth.models import User


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
                pass
            else:
                pass
        elif phone_form.is_valid():
            pass
        else:
            pass
