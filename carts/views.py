from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from store.models import Product, Variation, VariationManager
from carts.models import CartItem, Cart
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# To create private function just add underscore behind function name.
def _cart_id(request):
    """Private function to get session key from user."""

    # Getting user Cart via Posting session key.
    session_key = request.session.session_key
    # If session key doesn't exist.
    if not session_key:
        session_key = request.session.create()

    # Returning session key.
    return session_key


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

# Getting product variation from POST method.
    if request.method == "POST":
        # Getting all elements from POST.
        for item in request.POST:
            key = item # Getting Key
            value = request.POST[key]  # And getting value
            # print(key, value)

            # Trying to get Variation object
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    # This try block is for creating the cart for user
    try:   # Get the session key of current user.
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:  # If cart does not exist create them.
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    # ********

    # Check if Cart item exists
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        # Get the item from the current cart
        cart_item = CartItem.objects.filter(product=product,
                                          cart=cart)

        ex_var_list = []  # -> Existing variations of product in cart -> list
        id = [] # -> Product id's
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        # Check if variation of specific product exist in current Cart
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)  # Get current index of product
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()

        else:
            item = CartItem.objects.create(product=product,
                                           quantity=1,
                                           cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)

            item.save()

    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )

        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)

        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product,
                                         cart=cart,
                                         id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()

    except:
        pass

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product,
                                     cart=cart,
                                     id=cart_item_id)
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
