import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django 
django.setup() 



import factory
from django.utils import timezone
from nosh.models import CustomUser, OTP, Restaurant, Item, Order, UserMod, PaymentHistory
from nosh.enum import PaymentReason, UserType, OrderStatus, PaymentStatus, PaymentType

# Assuming enums are defined in .enum as shown in the question

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker('user_name')
    user_type = factory.Faker('random_element', elements=[user_type.value for user_type in UserType])
    mobile_no = factory.Faker('numerify', text='##########')
    email = factory.Faker('email')
    profile_pic = factory.Faker('image_url')
    amount = factory.Faker('random_number', digits=4)
    email_verified = factory.Faker('boolean')

class OTPFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OTP

    user = factory.SubFactory(CustomUserFactory)
    OTP = factory.Faker('numerify', text='######')
    expiration_time = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(minutes=5))

class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.Faker('company')
    image = factory.Faker('image_url')
    address = factory.Faker('address')
    owner_id = factory.Faker('random_int', min=1, max=1000)
    value = factory.Faker('random_number', digits=3)
    rating = factory.Faker('pyfloat', right_digits=1, positive=True, min_value=1, max_value=5)
    start_time = factory.Faker('time')
    end_time = factory.Faker('time')

class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Faker('word')
    cost = factory.Faker('random_number', digits=3)
    description = factory.Faker('text')
    restaurant_id = factory.SubFactory(RestaurantFactory)
    instant_item = factory.Faker('boolean')
    available = factory.Faker('boolean')
    quantity = factory.Faker('random_int', min=1, max=100)
    image = factory.Faker('image_url')
    rating = factory.Faker('pyfloat', right_digits=1, positive=True, min_value=1, max_value=5)

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    CustomerID = factory.Faker('random_int', min=1, max=1000)
    Address = factory.Faker('address')
    Status = factory.Faker('random_element', elements=[status.value for status in OrderStatus])
    Amount = factory.Faker('random_number', digits=4)
    PaymentStatus = factory.Faker('random_element', elements=[payment_status.value for payment_status in PaymentStatus])
    PaymentType = factory.Faker('random_element', elements=[payment_type.value for payment_type in PaymentType])
    DeliveredBy = factory.Faker('random_int', min=1, max=1000)
    RestaurantID = factory.SubFactory(RestaurantFactory)

class UserModFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserMod

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    mobile_no = factory.Faker('numerify', text='##########')
    email = factory.Faker('email')
    profile_pic = factory.Faker('image_url')
    amount = factory.Faker('random_number', digits=4)

class PaymentHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentHistory

    UserID = factory.Faker('random_int', min=1, max=1000)
    Payee = factory.Faker('random_int', min=1, max=1000)
    Amount = factory.Faker('random_number', digits=4)
    Timestamp = factory.LazyFunction(timezone.now)
    OrderID = factory.SubFactory(OrderFactory)
    Reason = factory.Faker('random_element', elements=[reason.value for reason in PaymentReason])


# Generate 10 instances for each model
for _ in range(10):
    CustomUserFactory.create()
    OTPFactory.create()
    RestaurantFactory.create()
    ItemFactory.create()
    OrderFactory.create()
    UserModFactory.create()
    PaymentHistoryFactory.create()
