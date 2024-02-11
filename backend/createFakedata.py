# import os 
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# import django 
# django.setup() 

# from faker import Faker 
# from django.utils import timezone
# from nosh.models import * 
# from model_bakery.recipe import Recipe, foreign_key, RecipeForeignKey

# fake = Faker()

# expiration_time = fake.future_datetime(end_date="+30d", tzinfo=timezone.utc)

# # Create fake data for CustomUser
# for _ in range(10):
#     user = Recipe(CustomUser,
#                   user_type=fake.random_element(elements=[choice[0] for choice in USER_CHOICES]),
#                   mobile_no=fake.phone_number(),
#                   email=fake.email(),
#                   amount=fake.random_number(digits=5),
#                   email_verified=fake.boolean()
#                   )
#     user.make()

# # Create fake data for OTPs
# for user in CustomUser.objects.all():
#     otp = Recipe(OTP,
#                  user=user,
#                  OTP=fake.password(length=10),
#                  expiration_time=fake.future_datetime(end_date="+30d", tzinfo=timezone.utc)
#                  )
#     otp.make()

# # Create fake data for Restaurants
# for _ in range(5):
#     restaurant = Recipe(Restaurant,
#                         name=fake.company(),
#                         image=fake.image_url(),
#                         address=fake.address(),
#                         owner_id=fake.random_number(digits=5),
#                         value=fake.random_number(digits=6),
#                         rating=fake.pyfloat(left_digits=1, right_digits=2),
#                         )
#     restaurant.make()

# # Create fake data for Items
# for restaurant in Restaurant.objects.all():
#     for _ in range(5):
#         item = Recipe(Item,
#                       name=fake.word(),
#                       cost=fake.random_number(digits=3),
#                       description=fake.text(),
#                       restaurant_id=restaurant,
#                       instant_item=fake.boolean(),
#                       available=fake.boolean(),
#                       quantity=fake.random_number(digits=2),
#                       image=fake.image_url(),
#                       rating=fake.pyfloat(left_digits=1, right_digits=2)
#                       )
#         item.make()



# # Create fake data for Orders
# for _ in range(20):
#     order = Recipe(Order,
#                    CustomerID=fake.random_number(digits=5),
#                    Address=fake.address(),
#                    Status=fake.random_element(elements=['Pending', 'Processing', 'Delivered']),
#                    Amount=fake.random_number(digits=4),
#                    PaymentStatus=fake.random_element(elements=['Paid', 'Unpaid']),
#                    PaymentType=fake.random_element(elements=['Credit Card', 'Cash']),
#                    DeliveredBy=fake.random_number(digits=5),
#                    DeliveredAt=fake.past_datetime(start_date="-1d", tzinfo=None),
#                    RestaurantID = RecipeForeignKey(restaurant)
#                    )
#     order.make()

# # Create fake data for UserMods
# for _ in range(5):
#     user_mod = Recipe(UserMod,
#                       first_name=fake.first_name(),
#                       last_name=fake.last_name(),
#                       mobile_no=fake.phone_number(),
#                       email=fake.email(),
#                       profile_pic=fake.image_url(),
#                       amount=fake.random_number(digits=5)
#                       )
#     user_mod.make()

# # Create fake data for PaymentHistory
# for _ in range(30):
#     payment_history = Recipe(PaymentHistory,
#                              UserID=RecipeForeignKey(UserMod.objects.all()).UserID,
#                              Payee=RecipeForeignKey(UserMod.objects.all()).UserID,
#                              Amount=fake.random_number(digits=4),
#                              Timestamp=fake.past_datetime(start_date="-1d", tzinfo=None),
#                              OrderID=RecipeForeignKey(order),
#                              Reason=fake.random_element(elements=[choice[0] for choice in REASON_CHOICES])
#                              )
#     payment_history.make()

# Create fake data for CustomUser

# user_r = Recipe(CustomUser,
#                   user_type=fake.random_element(elements=[choice[0] for choice in USER_CHOICES]),
#                   mobile_no=fake.phone_number(),
#                   email=fake.email(),
#                   amount=fake.random_number(digits=5),
#                   email_verified=fake.boolean()
#                   )


# users = user_r.make(_quantity=10)

# # Create fake data for OTPs
# for user in users:
#     otp = Recipe(OTP,
#                  user=foreign_key(user_r),
#                  OTP=fake.password(length=10),
#                  expiration_time=fake.future_datetime(end_date="+30d", tzinfo=timezone.utc)
#                  ).make()

# # Create fake data for Restaurants
# restaurant_recipe = Recipe(Restaurant,
#                            name=fake.company(),
#                            image=fake.image_url(),
#                            address=fake.address(),
#                            owner_id=fake.random_number(digits=5),
#                            value=fake.random_number(digits=6),
#                            rating=fake.pyfloat(left_digits=1, right_digits=2),
#                            )

# for _ in range(5):
#     restaurant_recipe.make()

# # Create fake data for Items
# for restaurant in Restaurant.objects.all():
#     for _ in range(5):
#         item_recipe = Recipe(Item,
#                              name=fake.word(),
#                              cost=fake.random_number(digits=3),
#                              description=fake.text(),
#                              restaurant_id=foreign_key(restaurant_recipe),
#                              instant_item=fake.boolean(),
#                              available=fake.boolean(),
#                              quantity=fake.random_number(digits=2),
#                              image=fake.image_url(),
#                              rating=fake.pyfloat(left_digits=1, right_digits=2)
#                              )
#         item_recipe.make()

# # Create fake data for Orders

# order_recipe = Recipe(Order,
#                           CustomerID=fake.random_number(digits=5),
#                           Address=fake.address(),
#                           Status=fake.random_element(elements=['Pending', 'Processing', 'Delivered']),
#                           Amount=fake.random_number(digits=4),
#                           PaymentStatus=fake.random_element(elements=['Paid', 'Unpaid']),
#                           PaymentType=fake.random_element(elements=['Credit Card', 'Cash']),
#                           DeliveredBy=fake.random_number(digits=5),
#                           DeliveredAt=fake.past_datetime(start_date="-1d", tzinfo=timezone.utc),
#                           RestaurantID=foreign_key(restaurant_recipe)
#                           )

# for _ in range(20):
#     order_recipe.make()

# # Create fake data for UserMods

# user_mod_recipe = Recipe(UserMod,
#                              first_name=fake.first_name(),
#                              last_name=fake.last_name(),
#                              mobile_no=fake.phone_number(),
#                              email=fake.email(),
#                              profile_pic=fake.image_url(),
#                              amount=fake.random_number(digits=5)
#                              )

# for _ in range(5):
#     user_mod_recipe.make()

# # Create fake data for PaymentHistory
# for _ in range(30):
#     payment_history_recipe = Recipe(PaymentHistory,
#                                     UserID=foreign_key(user_mod_recipe),
#                                     Payee=foreign_key(user_mod_recipe),
#                                     Amount=fake.random_number(digits=4),
#                                     Timestamp=fake.past_datetime(start_date="-1d", tzinfo=timezone.utc),
#                                     OrderID=foreign_key(order_recipe),
#                                     Reason=fake.random_element(elements=[choice[0] for choice in REASON_CHOICES])
#                                     )
#     payment_history_recipe.make()

import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django 
django.setup() 

import random
from django.utils import timezone
from nosh.enum import PaymentReason, UserType
from nosh.models import CustomUser, OTP, Restaurant, Item, Order, UserMod, PaymentHistory, USER_CHOICES, REASON_CHOICES, PaymentReason, UserType
from datetime import timedelta
from faker import Faker
from nosh.models import CustomUser, Restaurant, Item, Order, PaymentHistory
from model_bakery.recipe import Recipe, foreign_key, seq
from nosh.enum import OrderStatus, OrderType, PaymentStatus, PaymentType, Address, PaymentReason, UserType

fake = Faker()

# Create a recipe for CustomUser
# custom_user_recipe = Recipe(
#     CustomUser,
#     username=fake.user_name(),
#     user_type=fake.random_element(elements=[user_type.value for user_type in UserType]),
#     mobile_no=fake.random_number(digits=10, fix_len=True),
#     email=fake.email(),
#     profile_pic=fake.image_url(),
#     amount=fake.random_number(digits=5),
#     email_verified=fake.boolean()
# )

# # Create a recipe for Restaurant
# restaurant_recipe = Recipe(
#     Restaurant,
#     name=fake.company(),
#     image=fake.image_url(),
#     address=fake.address(),
#     owner_id=seq(1),
#     value=fake.random_number(digits=5),
#     rating=fake.pyfloat(min_value=1, max_value=5, right_digits=1),
#     start_time=fake.time(),
#     end_time=fake.time()
# )

# Create a recipe for Item
# item_recipe = Recipe(
#     Item,
#     name=fake.word(),
#     cost=fake.random_number(digits=3),
#     description=fake.text(),
#     restaurant_id=foreign_key(restaurant_recipe),
#     instant_item=fake.boolean(),
#     available=fake.boolean(),
#     quantity=fake.random_number(digits=2),
#     image=fake.image_url(),
#     rating=fake.pyfloat(min_value=1, max_value=5, right_digits=1)
# )

# # Create a recipe for Order
# order_recipe = Recipe(
#     Order,
#     CustomerID=seq(1),
#     Address=fake.address(),
#     Status=fake.random_element(elements=[status.value for status in OrderStatus]),
#     Amount=fake.random_number(digits=3),
#     PaymentStatus=fake.random_element(elements=[payment_status.value for payment_status in PaymentStatus]),
#     PaymentType=fake.random_element(elements=[payment_type.value for payment_type in PaymentType]),
#     DeliveredBy=seq(1),
#     RestaurantID=foreign_key(restaurant_recipe)
# )

# # Create a recipe for PaymentHistory
# payment_history_recipe = Recipe(
#     PaymentHistory,
#     UserID=seq(1),
#     Payee=seq(1),
#     Amount=fake.random_number(digits=3),
#     OrderID=foreign_key(order_recipe),
#     Reason=fake.random_element(elements=[reason.value for reason in PaymentReason])
# )

# otp_recipe = Recipe(
#     OTP,
#     user=foreign_key(custom_user_recipe),
#     OTP=fake.random_number(digits=6, fix_len=True),
#     expiration_time=timezone.now() + timedelta(minutes=10)
# )

# # Create a recipe for UserMod
# user_mod_recipe = Recipe(
#     UserMod,
#     first_name=fake.first_name(),
#     last_name=fake.last_name(),
#     mobile_no=fake.random_number(digits=10, fix_len=True),
#     email=fake.email(),
#     profile_pic=fake.image_url(),
#     amount=fake.random_number(digits=5)
# )


# # Generate the data
# for _ in range(10):
#     custom_user_recipe.make()
#     restaurant_recipe.make()
#     item_recipe.make()
#     order_recipe.make()
#     payment_history_recipe.make()
#     otp_recipe.make()
#     user_mod_recipe.make()




# faker = Faker()

# def create_custom_users(count=10):
#     for i in range(count):
#         user = CustomUser(
#            username = faker.user_name(),  
#            first_name = faker.first_name(),
#            last_name = faker.last_name(),
#            user_type = faker.random_element([t.value for t in UserType]),
#            mobile_no = faker.phone_number(),
#            email = faker.email(),
#            profile_pic = faker.image_url(),
#            amount = faker.random_int(0, 1000), 
#         )
#         user.save()
        
# def create_otps(count=10):
#     for i in range(count):
#         user = foreign_key(CustomUser)   
#         otp = OTP(
#            user=user,    
#            OTP = faker.random_number(digits=6),  
#            expiration_time = faker.date_time_between(start_date="+1d", end_date="+1w")
#         )
#         otp.save()
        
# def create_restaurants(count=10):
#     for i in range(count):
#         restaurant = Restaurant(
#            name = faker.company(),    
#            image = faker.image_url(),
#            address = faker.address(), 
#            owner_id = faker.random_int(1, 10),    
#            rating = faker.random_int(1, 5),
#            start_time = faker.time(),
#            end_time = faker.time() 
#         )
#         restaurant.save()
        
# def create_items(count=10):
#     for i in range(count): 
#         restaurant = foreign_key(Restaurant) 
#         item = Item(
#            name = faker.word(),    
#            cost = faker.random_int(100, 1000),
#            description = faker.text(),
#            restaurant_id = restaurant,  
#            instant_item = faker.boolean(),
#            available = faker.boolean(),
#            quantity = faker.random_int(1, 20),
#            image = faker.image_url(),
#            rating = faker.random_int(1, 5)   
#         )
#         item.save()
        
# def create_orders(count=10):
#     for i in range(count):
#         customer = foreign_key(CustomUser)
#         restaurant = foreign_key(Restaurant)        
#         order = Order(
#             CustomerID = customer,
#             Address = faker.address(),
#             Status = faker.random_element([s.value for s in OrderStatus]),  
#             Amount = faker.random_int(100, 5000),
#             PaymentStatus = faker.random_element([s.value for s in PaymentStatus]),  
#             PaymentType = faker.random_element([p.value for p in PaymentType]),
#             RestaurantID = restaurant,
#             DeliveredAt = faker.date_time_between(start_date="-1y", end_date="now")
#         )
#         order.save()
        
# def create_usermods(count=10):
#     for i in range(count):
#         user = UserMod(
#            first_name = faker.first_name(), 
#            last_name = faker.last_name(),
#            mobile_no = faker.phone_number(),  
#            email = faker.email(),
#            profile_pic = faker.image_url(),
#            amount = faker.random_int(0, 1000)
#         )
#         user.save()
        
# def create_payments(count=10):
#     for i in range(count):
#         user = foreign_key(CustomUser) 
#         order = foreign_key(Order)  
#         payment = PaymentHistory(
#            UserID = user,
#            Payee = faker.random_int(1, 10),    
#            Amount = faker.random_int(100, 5000),
#            OrderID = order,
#            Reason = faker.random_element([r.value for r in PaymentReason])
#         )
#         payment.save()