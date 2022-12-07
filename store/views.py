from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category


# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all()
        products_count = products.count()

    context = {'products': products,
               'products_founded': products_count}

    return render(request, template_name='store/store.html', context=context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        is_available = product.is_available
        # To get into category model slug we need to use '__'
        context = {
            'product': product,
            'is_available': is_available
        }
    except Exception:
        raise Exception

    return render(request, template_name='store/product_detail.html', context=context)

