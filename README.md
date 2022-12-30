# E-Commerce created in Django.
  Created with: Django, SQLite, HTML, CSS, JS, BootStrap, for Payments i used PayPal.

# Products
 - Shop is able to have products with various variations ( Sizes and Colors of product) and also categories.
 - User could easily search products via Search View. 
 - User could browse by categories.
 - Easy Adding to Cart View.
 - If product quantity is equal to 0 user could not see products.
 - Reviews of authenticated users (Product must be purchased before)
 
# Cart
 - User has a Cart View from which he can increase or decrease amount of specific Product (And of course Delete).
 - If User is not authorized, the cart is saved on Session Key, when if User authorizes, the cart will be assigned to the logged User.
 - When User goes to "Checkout" on "Cart Page" and provide data then goes to "Make Order", his Cart is assigned to the new Order.
 
# Orders
 - Every order has generated unique ID.
 - "Checkout" view uses a "Billing" Form which contains needed data to make a order.
 - "Make Order" is the page with summarized data of the order and cart. User could pay for order via PayPal.
 - When payment is successful User is redirected to "Payment Successful" View.
 - Server sends a confirmation of taking order (To the Order E-mail and Account E-mail)
 
 # Accounts
 - Custom user model
    - To register, use "Register View"
    - To activate account User needs to activate it via e-mail (Verification E-mail via SMTP G-Mail)
    - Imported "Django messages" to send success or error messages 
    - "Forgot Password View" also uses verification e-mail process.
    - Implemented DashBoard with User orders and User contact data (with forms to change them if needed).
    
# Admin Panel
- Created a lot of changes in Admin Panel to make it easier to use.
    

# Screenshots

 ## Store
 
   #### -Home page (Context processors on categories data used in "Category" dropdown menu)
   
   ![image](https://user-images.githubusercontent.com/76777800/210073909-670c7c18-92da-4a9c-a981-d7771f66ef0c.png)
   
   #### -Store page (With Paginator)
   
   ![image](https://user-images.githubusercontent.com/76777800/210075456-197d18a5-a67f-4f62-852e-3ec954ee0d2e.png)
   
   #### -Product detail page
   
   ![image](https://user-images.githubusercontent.com/76777800/210075986-13d099af-b12a-4183-928d-c4464c1a417a.png)

   #### - Reviews of product. (On the same page as Product Detail)
   
   ![image](https://user-images.githubusercontent.com/76777800/210076079-4fd86220-ef29-4184-a53c-b641ee5b760f.png)

   

 ## Cart - Ordering process.
 
   #### -Cart with various variants of product.
   
   ![image](https://user-images.githubusercontent.com/76777800/210076549-bf3b1fc0-685a-4141-a1ca-e62eaf6fed49.png)
   
   #### -Checkout page
   
   ![image](https://user-images.githubusercontent.com/76777800/210076975-ce2cd1d2-b319-4ade-9c5b-501d4ddb78ff.png)

   #### -Place order page
   
   ![image](https://user-images.githubusercontent.com/76777800/210077146-58e689e4-60a2-4abf-96ee-6f5c5eaf082b.png)
   
   #### -Payment with PayPal
   
   ![image](https://user-images.githubusercontent.com/76777800/210077241-96fe6a60-0fa2-46f1-9bda-ed45b346c6f6.png)

   #### -Purchase confirmation
   
   ![image](https://user-images.githubusercontent.com/76777800/210077325-840929d6-4576-48a1-bc33-c98dcb37b35e.png)

   #### -SMTP G-mail order purchase confirmation (Currently no template for E-mail Message)
   
   ![image](https://user-images.githubusercontent.com/76777800/210077508-e69cbc7c-a6a7-4626-bd0d-853052e950c8.png)
   
 ## Login/Registration
   #### -Login (With success Django Message)
   
   ![image](https://user-images.githubusercontent.com/76777800/210077776-597177ae-2823-4ded-ab40-4d5c57408756.png)

   #### -Register
   
   ![image](https://user-images.githubusercontent.com/76777800/210078104-edc4e453-38ad-4243-8948-a30c83131260.png)
   
   #### - Register sucessful
   
   ![image](https://user-images.githubusercontent.com/76777800/210078052-5faac909-47bf-4ebb-a524-ecf0dccd632b.png)

   
 ## DashBoard
 
   #### -User information data
   
   ![image](https://user-images.githubusercontent.com/76777800/210073854-c02126a7-c9c4-4bc3-908a-46f81ae24b46.png)
 
   #### -User orders page
   
   ![image](https://user-images.githubusercontent.com/76777800/210073686-5e81c881-6542-441d-8716-28c2e5657b1a.png)
   
   #### -Specific order page
   
   ![image](https://user-images.githubusercontent.com/76777800/210073775-4c02f638-59da-46f8-8602-cca7cb3b9506.png)

   #### -Edit Profile page
   
   ![image](https://user-images.githubusercontent.com/76777800/210073057-0b26ec0a-9f58-426f-8c4f-a9c5307b5cd3.png)
   
   #### -Change Passoword page
   
   ![image](https://user-images.githubusercontent.com/76777800/210073581-a56ec6b4-f9e8-47c7-9f9a-210b2ebebdcd.png)
