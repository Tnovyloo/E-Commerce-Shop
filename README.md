## E-Commerce-Shop
# E-Commerce created in Django.

Front-end - Created in HTML, CSS, JS, BootStrap.
Back-end - Created in Django Framework connected with SQLite. 
Payments - PayPal

# Products
 - Shop is able to have products with various variations ( Sizes and Colors of product) and also categories.
 - User could easily search products via Search View. 
 - User could browse by categories.
 - Easy Adding to Cart View.
 - If product quantity is equal to 0 user could not see products.
 
# Cart
 - User has a Cart from which he can increase or decrease amount of specific Product (And of course Delete).
 - If User is not authorized, the cart is saved on Session Key, when if User authorizes, the cart will be assigned to the User.
 - When User goes to "Checkout" on "Cart Page" and provide data then goes to "Make Order", his Cart is assigned to the new Order.
 
# Orders
 - Every order has generated unique ID.
 - "Checkout" view uses a "Billing" Form which contains needed data to make a order.
 - "Make Order" is the page with summarized data of the order and cart. User could pay for order via PayPal.
 - When payment is successful User is redirected to "Payment Successful" View.
 - Server sends a confirmation of taking order (To the Order E-mail and Account E-mail)
 
 # Accounts
 - Custom user model
    - To register use "Register View"
    - To activate account User needs to activate it via e-mail (Verification E-mail via SMTP G-Mail)
    - Imported "Django messages" to send success or error messages 
    - "Forgot Password View" also uses verification e-mail process.
    - Implemented DashBoard with User orders and User contact data (with forms to change them if needed).
    
# Admin Panel
- Created a lot of changes in Admin Panel to make it easier to use.
    

# Screenshots.
 ## Store
   - Home page (Context processors on categories data used in "Category" dropdown menu)
   ![image](https://user-images.githubusercontent.com/76777800/210073909-670c7c18-92da-4a9c-a981-d7771f66ef0c.png)
   
   -
   
 ## DashBoard
   - User information data
   ![image](https://user-images.githubusercontent.com/76777800/210073854-c02126a7-c9c4-4bc3-908a-46f81ae24b46.png)
 
   - User orders page
   ![image](https://user-images.githubusercontent.com/76777800/210073686-5e81c881-6542-441d-8716-28c2e5657b1a.png)
   
   - Specific order page
   ![image](https://user-images.githubusercontent.com/76777800/210073775-4c02f638-59da-46f8-8602-cca7cb3b9506.png)

   - Edit Profile page
   ![image](https://user-images.githubusercontent.com/76777800/210073057-0b26ec0a-9f58-426f-8c4f-a9c5307b5cd3.png)
   
   - Change Passoword page
   ![image](https://user-images.githubusercontent.com/76777800/210073581-a56ec6b4-f9e8-47c7-9f9a-210b2ebebdcd.png)
