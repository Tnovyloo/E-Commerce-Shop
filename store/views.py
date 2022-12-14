from django.shortcuts import render, get_object_or_404, HttpResponse
from store.models import Product
from category.models import Category
from carts.models import CartItem, Cart
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        print(page)
        paged_products = paginator.get_page(page)
        products_count = products.count()
        print(paged_products)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        print(page)
        paged_products = paginator.get_page(page)
        products_count = products.count()
        print(paged_products)

    context = {'products': paged_products,
               'products_founded': products_count}

    return render(request, template_name='store/store.html', context=context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

        # To get into category model slug we need to use '__'
        context = {
            'product': product,
            'in_cart': in_cart,
        }
    except Exception:
        raise Exception

    return render(request, template_name='store/product_detail.html', context=context)

@csrf_exempt
def search(request):
    if 'keyword' in request.POST:
        keyword = request.POST['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)
                                                                        | Q(product_name__icontains=keyword))
            products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count,
        'phrase': keyword,
    }

    # TODO adjust html page.
    return render(request, template_name='store/store.html', context=context)
