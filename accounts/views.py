from django.views import View
from .models import Order, OrderItem
from shop.models import Product
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .constants import ORDER_STATUS
from .forms import SignUpLogInForm, LogInForm, SignUpForm
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model


User = get_user_model()

class Checkout(View):
    def get(self, request):
        order = Order.objects.create(user=request.user)
        cart = request.session.pop('cart', {})
        purchases = []
        for pk,quantity in cart.items():
            try:
                product = Product.objects.get(pk=pk)
                purchase = (product, quantity)
                purchases.append(purchase)
            except:
                continue
        for purchase in purchases:
            OrderItem.objects.create(
                order=order,
                product=purchase[0],
                quantity=purchase[1]
            )
        order = Order.objects.get(pk=order.pk)
        context = {'order': order}
        return render(request, 'accounts/checkout.html', context)

class payment(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = ORDER_STATUS[1][0]
        # Riderect the user to his/her account.

class SignUpLogIn(View):
    def get(self, request):
        return render(request, 'accounts/signup_login.html')
    
    def post(self, request):
        form = SignUpLogInForm(request.POST)
        if form.is_valid():
            identifier_type = form.cleaned_data["identifier_type"]
            identifier_value = form.cleaned_data["identifier_value"]
            request.session['identifier_type'] = identifier_type
            request.session['identifier_value'] = identifier_value
            if identifier_type == 'email':
                login = User.objects.filter(email__iexact=form.cleaned_data["identifier_value"]).exists()
            else:
                login = User.objects.filter(phone=form.cleaned_data["identifier_value"]).exists()
            if login:
                return redirect('accounts:login')
            return redirect('accounts:signup')
        context = {'error': True}
        return render(request, 'accounts/signup_login.html', context)

# Write a test to give permission only to users with a session that has 'identifier_key' and 'identifier_value'
class LogIn(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        password_form = LogInForm(request.POST)
        if password_form.is_valid():
            identifier=request.session.get('identifier_value')
            password = password_form.cleaned_data.get('password')
            user = authenticate(identifier=identifier, password=password)
            if user:
                login(request, user)
                del request.session['identifier_type']
                del request.session['identifier_value']
                return redirect('shop:home')
        context = {'error': True}
        return render(request, 'accounts/login.html', context)

# Write a test to give permission only to users with a session that has 'identifier_key' and 'identifier_value'
class SignUp(View):
    def get(self, request):
        identifier_type = request.session.get('identifier_type')
        identifier_value = request.session.get('identifier_value')
        context = {
            'form': SignUpForm(),
            'identifier_type': identifier_type,
            'identifier_value': identifier_value,
        }
        return render(request, 'accounts/signup.html', context)

    def post(self, request):
        signup_form = SignUpForm(request.POST)
        identifier_type = request.session.get('identifier_type')
        identifier_value = request.session.get('identifier_value')
        if signup_form.is_valid():
            user = User(
                first_name=signup_form.cleaned_data.get('first_name'),
                last_name=signup_form.cleaned_data.get('last_name'),
            )
            if identifier_type == 'email':
                user.email = identifier_value
                user.phone = signup_form.cleaned_data.get('phone')
            else:
                user.phone = identifier_value
                user.email = signup_form.cleaned_data.get('email')
            user.set_password(signup_form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            del request.session['identifier_type']
            del request.session['identifier_value']
            return redirect('shop:home')
        context = {
            'form': signup_form,
            'identifier_type': identifier_type,
            'identifier_value': identifier_value,
        }
        return render(request, 'accounts/signup.html', context)

class Account(View):
    def get(self, request):
        return render(request, 'accounts/account.html')
