## E-Commerce-Shop
# E-Commerce created in Django.

Front-end - Created in HTML, CSS, JS, BootStrap.
Back-end - Created in Django Framework connected with SQLite. 
Payments - PayPal

# PRODUCTS:
 - Shop is able to have products with various variations ( Sizes and Colors of product) and also categories.
 - User could easily search products via Search View. 
 - User could browse by categories.
 - Easy Adding to Cart View.
 
# CART:
 - User has a Cart from which he can increase or decrease amount of specific Product (And of course Delete).
 - If User is not authorized, the cart is saved on Session Key, when if User authorizes, the cart will be assigned to the User.
 - When User goes to "Checkout" on "Cart Page" and provide data then goes to "Make Order", his Cart is assigned to the new Order.
 
# ORDERS:
 - Every order has generated unique ID.
 - "Checkout" view uses a "Billing" Form which contains needed data to make a order.
 - "Make Order" is the page with summarized data of the order and cart. User could pay for order via PayPal.
 - When payment is successful User is redirected to "Payment Successful" View.
 - Server sends a confirmation of taking order (To the Order E-mail and Account E-mail)
 
 # ACCOUNTS
 - Custom user model
    - To register use "Register View"
    - To activate account User needs to activate it via e-mail (Verification E-mail via SMTP G-Mail)
    - "Forgot Password View" also uses verification e-mail process.
    - Implemented DashBoard with User orders and User contact data (with forms to change them if needed).
    
# ADMIN PANEL
- Created a lot of changes in Admin Panel to make it easier to use.
    
