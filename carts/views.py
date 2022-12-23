from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from store.models import Product, Variation, VariationManager
from carts.models import CartItem, Cart
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

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
    current_user = request.user
    # Getting product via product id and creating empty list with product variation.
    product = Product.objects.get(id=product_id)
    # If user is authenticated.
    if current_user.is_authenticated:

        product_variation = []
        # Getting product variation from POST method.
        if request.method == "POST":
            # Getting all elements from POST.
            for item in request.POST:
                key = item  # Getting Key
                value = request.POST[key]  # And getting value
                # print(key, value)

                # Trying to get Variation object
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        # Check if Cart item exists to avoid 'doubling' items. We want to iterate a quantity
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            # Get the item from the current cart
            cart_item = CartItem.objects.filter(product=product,
                                                user=current_user,
                                                )

            ex_var_list = []  # list -> Existing variations of product in cart
            id = []  # -> Product id's
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

            # Else create them.
            else:
                item = CartItem.objects.create(product=product,
                                               quantity=1,
                                               user=current_user)
                # Check if list of product variation is greater than 0
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(
                        *product_variation)  # We have to use '*' because we want to add all items from list

                item.save()

        # If Cart item does not exist then:
        else:
            # Create this cart item.
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )

            # Check if list of product variation is greater than 0 / Just repeat the same process as in Try block.
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()

        return redirect('cart')

    # **********
    # If user is not authenticated
    else:
        product_variation = []

        # Getting product variation from POST method.
        if request.method == "POST":
            # Getting all elements from POST.
            for item in request.POST:
                key = item  # Getting Key
                value = request.POST[key]  # And getting value
                # print(key, value)

                # Trying to get Variation object
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        # This try block is for creating the cart for user
        try:  # Get the session key of current user.
            cart = Cart.objects.get(cart_id=_cart_id(request))

        # If cart does not exist create them.
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        # ********

        # Check if Cart item exists to avoid 'doubling' items. We want to iterate a quantity
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            # Get the item from the current cart
            cart_item = CartItem.objects.filter(product=product,
                                                cart=cart)

            ex_var_list = []  # -> Existing variations of product in cart
            id = []  # -> Product id's
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

            # Else create them.
            else:
                item = CartItem.objects.create(product=product,
                                               quantity=1,
                                               cart=cart)
                # Check if list of product variation is greater than 0
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation) # We have to use '*' because we want to add all items from list

                item.save()

        # If Cart item does not exist then:
        else:
            # Create this cart item.
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )

            # Check if list of product variation is greater than 0 / Just repeat the same process as in Try block.
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()

        # Return user to 'cart.html'
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    """ Function of removing item from cart
        product_id   -> the id of product to remove
        cart_item_id -> the id of Cart item id
    """

    # Get the Cart ID from session key and get the product who has going to be removed.
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    try:
        # If user is authenticated we dont need to get
        if user.is_authenticated:
            # Get specific CartItem object
            cart_item = CartItem.objects.get(product=product,
                                             user=user,
                                             id=cart_item_id)
        # If user is not authenticated
        else:
            # Get cart via session key.
            cart = Cart.objects.get(cart_id=_cart_id(request))
            # Get specific CartItem object
            cart_item = CartItem.objects.get(product=product,
                                             cart=cart,
                                             id=cart_item_id)
        # Check if quantity of this product is greater than 1 to decrement the quantity of CartItem
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            # If quantity is 1 just delete the CartItem
            cart_item.delete()

    except:
        pass

    # Redirect user to his own cart.
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    """ This view is for DELETING Cart item ( Just 'X' button )
        product_id   -> product of item which is going to delete.
        cart_item_id -> Cart item ID which is going to delete.
    """

    user = request.user
    if user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product,
                                         id=cart_item_id,
                                         user=user)
    else:
        # Get current cart and product from user session key
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product,
                                         cart=cart,
                                         id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    """ View to check cart."""
    # Try to get a cartID
    try:
        tax = 0
        grand_total = 0

        # Check if user is authenticated, if yes then get user cart.
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        # Else, get cart from session key.
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        # Variables to getting the cart price and tax.
        tax = (23 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        # cart = Cart.objects.create(cart_id=_cart_id(request))
        pass

    # Send context to 'cart.html'
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, template_name='cart/cart.html', context=context)

@login_required(login_url='login')
def checkout(request,  total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (23 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        # cart = Cart.objects.create(cart_id=_cart_id(request))
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request=request,
                  template_name='cart/checkout.html',
                  context=context)
