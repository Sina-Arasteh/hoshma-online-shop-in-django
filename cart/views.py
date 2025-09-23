from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.views import View
from django.urls import reverse
from shop.models import Product


class Add(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.stock:
            cart = request.session.get('cart', {})
            try:
                cart[pk] += 1
            except KeyError:
                cart[pk] = 1
            request.session['cart'] = cart
        return redirect(reverse("product-detail", args=[pk]))

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
        context = {'purchases': purchases}
        return render(request, "cart/cart.html", context)
