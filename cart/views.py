from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect
from shop.models import Product


class Add(View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})
        try:
            cart[pk] += 1
        except KeyError:
            cart[pk] = 1
        request.session['cart'] = cart
        return redirect(reverse("product-detail", args=[pk,]))

class CartPage(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        purchases = []
        for pk,quantity in cart.items():
            try:
                product = Product.objects.get(pk=pk)
                purchase = (product, quantity)
                purchases.append(purchase)
            except:
                continue
        context = {'purchases': purchases,}
        return render(request, "cart/cart.html", context)
