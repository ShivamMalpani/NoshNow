# models.py
from django.db import models

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
    cost = models.IntegerField()
    description = models.TextField()
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    instant_item = models.BooleanField()
    quantity = models.IntegerField(null=True, blank=True)
    image = models.URLField(null=True, default=None)
    rating = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant_id.name}"

class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    CustomerID = models.IntegerField()
    Address = models.CharField(max_length=255)
    Status = models.CharField(max_length=50)
    TransactionID = models.CharField(max_length=255)
    PaymentStatus = models.CharField(max_length=50)
    DeliveredBy = models.IntegerField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    DeliveredAt = models.DateTimeField(null=True, blank=True)
    RestaurantID = models.IntegerField()

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

    def __str__(self):
        return f'Transaction ID: {self.TransactionID}, Amount: {self.Amount}, Timestamp: {self.Timestamp}'

