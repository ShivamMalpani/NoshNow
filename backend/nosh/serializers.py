# serializers.py
from rest_framework import serializers
from .models import Order, Restaurant, Item, UserMod, PaymentHistory
from .enum import OrderType, PaymentType, Address

class EnumField(serializers.Field):
    def to_representation(self, obj):
        return obj.value
    
class CheckoutByUserIdSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField()
    order_ids = serializers.ListField(child=serializers.IntegerField())


class RestaurantListSerializer(serializers.ModelSerializer):
    is_open = serializers.BooleanField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'image', 'address', 'value', 'rating', 'is_open']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class ItemUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
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

class OrderInputSerializer(serializers.Serializer):
    userID = serializers.IntegerField()
    paymentType = serializers.ChoiceField(choices=[(pt.value, pt.name) for pt in PaymentType])
    orderType = serializers.ChoiceField(choices=[(ot.value, ot.name) for ot in OrderType])
    Address = serializers.ChoiceField(choices=[(ot.value, ot.name) for ot in Address])

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['CustomerID', 'Address', 'Status', 'PaymentStatus', 'PaymentType', 'RestaurantID', 'Amount']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['OrderID', 'CustomerID', 'Address', 'Status', 'PaymentStatus', 'CreatedAt']


class OrderHistorySerializer(serializers.ModelSerializer):
    RestaurantName = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['OrderID', 'CustomerID', 'Address', 'Status', 'Amount', 'PaymentStatus', 'PaymentType', 'DeliveredBy', 'CreatedAt', 'DeliveredAt', 'RestaurantID', 'RestaurantName']
    
    def get_RestaurantName(self, obj):
        return obj.RestaurantID.name

class FreezeOrderSerializer(serializers.Serializer):
    OrderID = serializers.IntegerField()
    RestaurantID = serializers.IntegerField()
    freeze = serializers.BooleanField()

# class CheckoutSerializer(serializers.Serializer):
#     user_id = serializers.IntegerField()
#     restaurant_id = serializers.IntegerField()
#     order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
#     useWallet = serializers.BooleanField()

# class UndoCheckoutSerializer(serializers.Serializer):
#     order_id = serializers.IntegerField()

class PaymentHistorySerializer(serializers.ModelSerializer):
    Reason = EnumField()
    
    class Meta:
        model = PaymentHistory
        fields = '__all__'

class ViewWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)