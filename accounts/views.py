from django.shortcuts import render, redirect
from .forms import RegistrationForm
from accounts.models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Verification email imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Assign unauthorized cart to user if they logged in.
from carts.views import _cart_id
from accounts.models import Account
from carts.models import CartItem, Cart
import requests

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)  # Using created Form.
        if form.is_valid():  # Check if the form is valid
            # Get data from our clean method.
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email.split('@')[0]  # Username is the text before '@'

            # Create user with 'is_active = False' - To change it to True user needs to activate account by email.
            user = Account.objects.create_user(first_name=first_name,
                                               last_name=last_name,
                                               email=email,
                                               username=username,
                                               password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION BY EMAIL.
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"  # This will be subject of our activation e-mail
            # We have to use render_to_string method. We serve variables.
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Sending encoded user primary key
                'token': default_token_generator.make_token(user),  # Sending token which is assigned to this user
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Registration successful, We have sent you a e-mail to activate your account!')

            return redirect(f'/accounts/login/?command=verification&email={email}')

        # If form is not valid
        else:
            messages.error(request, 'Provided a wrong data.')

    # If method is not POST
    else:
        form = RegistrationForm()

    # Send only form to context.
    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context=context)


def login(request):
    if request.method == "POST":
        # Get the POST values from Form.
        email = request.POST['email']
        password = request.POST['password']

        # Check if user exists.
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            # auth.login(request, user)
            try:
                # Get current cart.
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product type of variations.
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to get cart products variations.
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []  # Existing variations of Cart items.
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # Check if 'pv' - ( product variation ) exists in ex_var_list ( existing product variation list)
                    for pv in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pv)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        # If it not exists in current product variations in cart then assign the item.user to user.
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass

            # Login user via django auth and send success message.
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')

            # Getting the url from where user came.
            url = request.META.get("HTTP_REFERER")
            try:
                query = requests.utils.urlparse(url).query
                # The request is: "next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)

            except:
                pass

            return redirect('dashboard')

        # If credentials is valid send a message to user.
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required(login_url='url')
def logout(request):
    """Simple logout function."""
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect('login')


def activate(request, uidb64, token):
    """Activate Account function
        uidb64 -> encoded user primary key
        token  -> default token generator
    """

    # Try to decode the 'uidb64'
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    # If decode goes wrong then user is None
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # If Try block and check token goes correctly then activate user account
    if user is not None and default_token_generator.check_token(user, token=token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated!")
        return redirect('login')

    # Send error message if something of our statements goes wrong.
    else:
        messages.error(request, "Invalid activation link")
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    """Dashboard function."""
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    """forgotPassword - if user forgotten password then
        send him to this view.
    """
    # User has to provide his e-mail.
    if request.method == "POST":
        email = request.POST["email"]
        # Check if any Account with this email exists.
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)  # __exact check if request email is email of user.

            # Reset password email.
            current_site = get_current_site(request)
            mail_subject = "Please reset your password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset e-mail has been sent to your email address.")
            return redirect('login')

        else:
            messages.error(request, "Account does not exist!")
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    """This view is on the email who has been sent in reset password"""

    # Try to decode uidb64 and check if decoded value is a primary key
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # If user exists and token is right
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid  # Save to current user session UID value to check later if user is really
        # changing his password.
        messages.success(request, "Please reset your password.")
        return redirect('resetPassword')

    else:
        messages.error(request, "This link has been expired!")
        return redirect('login')


def resetPassword(request):
    """ Only works when user is coming from email link."""
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            # Check if this user has on the session UID key
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("login")

        else:
            messages.error(request, "Passwords is not the same!")
            return redirect('resetPassword')

    else:
        return render(request, 'accounts/resetPassword.html')
