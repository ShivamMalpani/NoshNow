from django.db import models
from django.contrib.auth.models import AbstractUser
from .enum import PaymentReason, UserType
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.connections import connections


REASON_CHOICES = [(reason.value, reason.name.replace('_', ' ').title()) for reason in PaymentReason]
USER_CHOICES = [(user_type.value, user_type.name.replace('_', ' ').title()) for user_type in UserType]


class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=50, choices=USER_CHOICES, null=True, blank=True)
    mobile_no = models.CharField(max_length=10, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    profile_pic = models.URLField(null=True, blank=True)
    amount = models.IntegerField(default=0)
    email_verified = models.BooleanField(default=False)


class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    OTP = models.CharField(max_length=64)
    expiration_time = models.DateTimeField()


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField(null=True, default=None)
    address = models.CharField(max_length=255)
    owner_id = models.IntegerField()
    value = models.IntegerField(default=0)
    rating = models.FloatField(null=True)
    created_at = models.TimeField(auto_now_add=True)
    start_time = models.TimeField(default='00:00')
    end_time = models.TimeField(default='23:59')

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    cost = models.IntegerField(default=0)
    description = models.TextField()
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    instant_item = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    image = models.URLField(null=True, default=None)
    rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant_id.name}"
    
class ItemDocument(Document):
    class Meta:
        model = Item
        fields = ['name', 'cost', 'description', 'restaurant_id', 'instant_item', 'available', 'quantity', 'image', 'rating', 'created_at']
        index = connections.get_connection().create_index(Item._meta.db_table)

Item.objects.using('default').register(ItemDocument)  


class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    CustomerID = models.IntegerField()
    Address = models.CharField(max_length=255)
    Status = models.CharField(max_length=50)
    Amount = models.IntegerField()
    PaymentStatus = models.CharField(max_length=50)
    PaymentType = models.CharField(max_length=100)
    DeliveredBy = models.IntegerField(null=True, blank=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    DeliveredAt = models.DateTimeField(null=True, blank=True)
    RestaurantID = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class UserMod(models.Model):
    UserID = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    mobile_no = models.TextField()
    email = models.EmailField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    profile_pic = models.URLField()  # Assuming EC2 link is a URL
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class PaymentHistory(models.Model):
    TransactionID = models.AutoField(primary_key=True)
    UserID = models.IntegerField()
    Payee = models.IntegerField()
    Amount = models.IntegerField()
    Timestamp = models.DateTimeField(auto_now_add=True)
    OrderID = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    Reason = models.CharField(max_length=50, choices=REASON_CHOICES)

    def __str__(self):
        return f'Transaction ID: {self.TransactionID}, Amount: {self.Amount}, Timestamp: {self.Timestamp}'

