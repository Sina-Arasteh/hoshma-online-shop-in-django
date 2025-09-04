from django.views import View
from .models import (
    Order,
    OrderItem
)
from shop.models import Product
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from .constants import ORDER_STATUS
from .forms import (
    SignUpLogInForm,
    SignUpForm,
    LogInForm,
    AddAddressForm,
    CheckoutForm
)
from django.utils.translation import gettext as _
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404


User = get_user_model()

class SignUpLogIn(View):
    def get(self, request):
        next_url = request.GET.get('next')
        request.session['next'] = next_url
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
        identifier_type = request.session.get('identifier_type')
        identifier_value = request.session.get('identifier_value')
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = User(
                first_name=signup_form.cleaned_data.get('first_name'),
                last_name=signup_form.cleaned_data.get('last_name'),
            )
            if identifier_type == 'email':
                user.email = identifier_value
            else:
                user.phone = identifier_value
            user.set_password(signup_form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            del request.session['identifier_type']
            del request.session['identifier_value']
            next_url = request.session.pop('next', None)
            return redirect(next_url or 'shop:home')
        context = {
            'form': signup_form,
            'identifier_type': identifier_type,
            'identifier_value': identifier_value,
        }
        return render(request, 'accounts/signup.html', context)

# Write a test to give permission only to users with a session that has 'identifier_key' and 'identifier_value'
class LogIn(View):
    def get(self, request):
        identifier_type = request.session.get('identifier_type')
        identifier_value = request.session.get('identifier_value')
        if identifier_type == 'email':
            user = User.objects.get(email__iexact=identifier_value)
        else:
            user = User.objects.get(phone=identifier_value)
        context = {'user': user}
        return render(request, 'accounts/login.html', context)
    
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
                next_url = request.session.pop('next', None)
                return redirect(next_url or 'shop:home')
        context = {'error': True}
        return render(request, 'accounts/login.html', context)

class Checkout(LoginRequiredMixin, View):
    def get(self, request):
        order = Order.objects.create(user=request.user)
        cart = request.session.pop('cart', None)
        if not cart:
            raise PermissionDenied(_("You must have item(s) in your cart to proceed."))
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
        if hasattr(request.user, 'addresses'):
            addresses = request.user.addresses.all()
        else:
            addresses = []
        context = {
            'order': order,
            'addresses': addresses,
        }
        return render(request, 'accounts/checkout.html', context)

class OrderCancellation(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = ORDER_STATUS[4][0]
        return redirect('shop:home')

class payment(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_orders = Order.objects.filter(user=request.user)
        order = get_object_or_404(user_orders, pk=pk)
        if not order.status == ORDER_STATUS[0][0]:
            raise Http404()
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            selected_address = form.cleaned_data['address']
            customer_note = form.cleaned_data['customer_note']
            order.address = selected_address
            order.customer_note = customer_note
            order.status = ORDER_STATUS[1][0]
            order.save()
            return redirect('accounts:accounts')
        if hasattr(request.user, 'addresses'):
            addresses = request.user.addresses.all()
        else:
            addresses = []
        context = {
            'order': order,
            'addresses': addresses,
            'error': True,
        }
        return render(request, 'accounts/checkout.html', context)

# login required
# Users can have at most five addresses.
# If a user have the max number of addresses disable the 'add address' button.
# Orders that have 'pending' status should have the 'payment' button.
class Account(View):
    def get(self, request):
        user = request.user
        context = {
            'full_name': user.get_full_name(),
            'phone': user.phone,
            'email': user.email,
            'addresses': user.addresses.all(),
            'orders': user.orders
        }
        return render(request, 'accounts/account.html', context)

# Only users that the number of their addresses is less than 5 can access this view.
class AddAddress(LoginRequiredMixin, View):
    def get(self, request):
        next_url = request.GET.get('next')
        request.session['next'] = next_url
        address_form = AddAddressForm()
        context = {'form': address_form}
        return render(request, 'accounts/add_address.html', context)

    def post(self, request):
        address_form = AddAddressForm(request.POST)
        if address_form.is_valid():
            address_form.save(commit=False)
            address_form.user = request.user
            address_form.save()
            next_url = request.session.pop('next', None)
            return redirect(next_url or 'accounts:account')
        context = {'form': address_form}
        return render(request, 'accounts/add_address.html', context)

# Only users that they've got at least an address.
class RemoveAddress(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Check if the pk exists
        pass
