# serializers.py
from rest_framework import serializers
from .models import Order, Restaurant, Item, UserMod

class RestaurantListSerializer(serializers.ModelSerializer):
    is_open = serializers.BooleanField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'image', 'address', 'value', 'rating', 'is_open']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMod
        fields = ['UserID', 'first_name', 'last_name', 'mobile_no', 'email']

class CartSerializer(serializers.Serializer):
    userID = serializers.IntegerField()
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

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

class CheckoutSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    restaurant_id = serializers.IntegerField()
    order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    useWallet = serializers.BooleanField()

class UndoCheckoutSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class PaymentHistorySerializer(serializers.Serializer):
    TransactionID = serializers.IntegerField()
    UserID = serializers.IntegerField()
    Payee = serializers.IntegerField()
    Amount = serializers.IntegerField()
    Timestamp = serializers.DateTimeField()

class ViewWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)