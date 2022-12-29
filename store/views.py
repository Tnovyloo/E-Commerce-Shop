from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from store.models import Product, ProductGallery
from category.models import Category
from carts.models import CartItem, Cart
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import ReviewRating
from .forms import ReviewForm
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
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
        # To get into category model slug we need to use '__'
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

    except Exception:
        raise Exception

    # Check if user is authenticated and if user bought it
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    # Getting the reviews ordered by the newest.
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True).order_by('-created_at')

    # Get the product gallery
    # product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'product': product,
        'in_cart': in_cart,
        'orderproduct': order_product,
        'reviews': reviews,
        # 'product_gallery': product_gallery,
    }

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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)  # Get into ForeignKey
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
