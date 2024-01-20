# views.py
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer, OrderHistorySerializer
from .enum import OrderStatus

class ActiveOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurantID')
        return Order.objects.filter(RestaurantID=restaurant_id, Status=OrderStatus.ACTIVE)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderHistorySerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurantID')
        return Order.objects.filter(RestaurantID=restaurant_id)