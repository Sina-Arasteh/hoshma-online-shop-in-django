from .models import (
    Product,
    Category
)
from django.shortcuts import (
    render,
    get_object_or_404
)
from django.views import View


# class ProductsPage(View):
#     def get(self, request):
#         products = Product.objects.all().select_related('main_image', 'discount')
#         context = {'products': products}
#         return render(request, "shop/index.html", context)

class IndexPage(View):
    def get(self, request):
        return render(request, 'index.html')

class RemoveMe(View):
    def get(self, request):
        return render(request, 'search.html')

class RemoveMe2(View):
    def get(self, request):
        return render(request, 'product.html')

class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('main_image', 'discount').prefetch_related('images', 'tags', 'categories'),
            pk=pk
        )
        context = {'product': product}
        return render(request, "shop/product_detail.html", context)

class CategoryProducts(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        products = category.get_all_children_products()
        context = {'products': products}
        return render(request, 'shop/category_products.html', context)
