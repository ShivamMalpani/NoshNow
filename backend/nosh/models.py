# models.py
from django.db import models

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

class User(models.Model):
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

