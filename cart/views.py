from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect


class Add(View):
    def post(self, request, pk):
        cart = request.session.get('cart', {})
        try:
            cart[pk] += 1
        except KeyError:
            cart[pk] = 1
        request.session['cart'] = cart
        return redirect(reverse("product-detail", args=[pk,]))
