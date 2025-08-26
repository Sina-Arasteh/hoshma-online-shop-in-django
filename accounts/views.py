from django.views import View
from .models import Order, OrderItem
from shop.models import Product
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .constants import ORDER_STATUS


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
