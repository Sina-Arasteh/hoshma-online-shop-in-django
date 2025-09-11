from .models import (
    Product,
    Category
)
from django.shortcuts import (
    render,
    get_object_or_404
)
from django.views import View


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "shop/index.html", context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, "shop/product_detail.html", context)

class CategoryProducts(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        products = category.get_all_children_products()
        context = {'products': products}
        return render(request, 'shop/category_products.html', context)
