from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from store.models import Product, Variation, VariationManager
from carts.models import CartItem, Cart
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# To create private function just add underscore behind function name.
def _cart_id(request):
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.create()
    return session_key


def add_cart(request, product_id):
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]
            print(key, value)

            try:
                variation = Variation.objects.get(variation_category__iexact=key, variation_value__iexact=value)
                print(variation)
            except:
                pass

        # color = request.POST['color']
        # size = request.POST['size']
        # print(color, size)

    product = Product.objects.get(id=product_id)
    try:   # Get the session key of current user.
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:  # If cart does not exist create them.
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product)
        cart_item.quantity += 1  # Incrementing the amount of item in the cart.
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()

    # return HttpResponse(cart_item.product) # Check if cart_item returns a product.
    # return HttpResponse(cart_item.quantity) # Check if cart_item returns a valid amount of added items.

    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (23 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExists:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, template_name='cart/cart.html', context=context)
