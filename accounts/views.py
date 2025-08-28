from django.views import View
from .models import Order, OrderItem, CustomUser
from shop.models import Product
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .constants import ORDER_STATUS
from .forms import SignUpLogInForm, LogIn
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate


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
        # Riderect the user to the his/her account.

class Account(View):
    def get(self, request):
        return render(request, 'accounts/account.html')

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
                login = CustomUser.objects.filter(email__iexact=form.cleaned_data["identifier_value"]).exists()
            else:
                login = CustomUser.objects.filter(phone=form.cleaned_data["identifier_value"]).exists()
            if login:
                return redirect('accounts:login')
            return redirect('accounts:signup')
        context = {'error': True}
        return render(request, 'accounts/signup_login.html', context)

class LogIn(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        password_form = LogIn(request.POST)
        if password_form.is_valid():
            identifier=request.session.get('identifier_value')
            password = password_form.cleaned_data.get('password')
            user = authenticate(identifier=identifier, password=password)
            if user:
                # Log the user in
                pass
        context = {'error': True}
        return render(request, 'accounts/login.html', context)

class SignUp(View):
    def get(self, request):
        return render(request, 'accounts/signup.html')
    
    def post(self, request):
        pass
