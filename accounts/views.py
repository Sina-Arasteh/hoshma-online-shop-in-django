from django.views import View
from .forms import CheckoutForm
from .models import Order, OrderItem
from shop.models import Product
from django.shortcuts import render


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
        context = {'order': order}
        return render(request, 'accounts/checkout.html', context)
