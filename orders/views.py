from django.shortcuts import render, redirect
from carts.models import CartItem, Cart
from orders.models import Order, OrderProduct, Payment
from accounts.models import Account
from .forms import OrderForm
import datetime
import json
# Create your views here.

def payments(request):
    # Getting Data from 'payments.html' JS (fetch) and post method
    body = json.loads(request.body)
    print(body)

    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction detail inside Payment model.
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    # Update the order model.
    order.payment = payment
    order.is_ordered = True  # Order is ordered.
    order.save()

    return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0):
    """ Getting all information from billing post method. """
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    # Get the amount to pay.
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (23 * total) / 100
    grand_total = total + tax

    # Try to get billing information from POST method via using OrderForm.
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information from form
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')  # Getting user IP
            data.save()

            # Generating order number
            yr = int(datetime.date.today().strftime('%Y'))  # Current Year
            dt = int(datetime.date.today().strftime('%d'))  # Current Day
            mt = int(datetime.date.today().strftime('%m'))  # Current Month
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,
                                      is_ordered=False,
                                      order_number=order_number
                                      )
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }

            return render(request=request,
                          template_name='orders/payments.html',
                          context=context
                          )

    else:
        return redirect('checkout')

