# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order
from .serializers import *
from .enum import OrderStatus

class CheckoutByUserIdView(generics.CreateAPIView):
    serializer_class = CheckoutByUserIdSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant_id = serializer.validated_data['restaurant_id']
        order_ids = serializer.validated_data['order_ids']
        try:
            orders = Order.objects.filter(OrderID__in=order_ids, RestaurantID=restaurant_id, Status=OrderStatus.FREEZED.value)
            if orders.count() != len(order_ids):
                return Response({'message': 'Not all orders are freezed'}, status=status.HTTP_400_BAD_REQUEST)
            addresses = set(order.address for order in orders)
            if len(addresses) != 1:
                return Response({'message': 'Orders have different addresses'}, status=status.HTTP_400_BAD_REQUEST)
            orders.update(Status=OrderStatus.IN_TRANSIT.value)
            return Response({'message': 'Checkout successful'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)