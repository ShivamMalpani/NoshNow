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
