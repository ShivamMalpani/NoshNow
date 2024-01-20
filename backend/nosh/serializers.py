# serializers.py
from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['OrderID', 'CustomerID', 'Address', 'Status', 'PaymentStatus', 'CreatedAt']


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['OrderID', 'CustomerID', 'Address', 'Status', 'PaymentStatus', 'DeliveredBy', 'CreatedAt', 'DeliveredAt', 'RestaurantID']

class FreezeOrderSerializer(serializers.Serializer):
    OrderID = serializers.IntegerField()
    RestaurantID = serializers.IntegerField()
    freeze = serializers.BooleanField()