from shop.models import Category


def category(request):
    return {'root_categories': Category.objects.filter(parent__isnull=True).prefetch_related('children'),}
