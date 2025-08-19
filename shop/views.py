from . import models
from django.shortcuts import render
from django.shortcuts import get_object_or_404


def index(request):
    products = models.Product.objects.all()
    context = {'products': products}
    return render(request, "shop/index.html", context)

def product_detail(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    context = {'product': product}
    return render(request, "shop/product_detail.html", context)
