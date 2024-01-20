# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, OrderHistorySerializer, FreezeOrderSerializer
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
    

class FreezeOrderView(generics.CreateAPIView):
    serializer_class = FreezeOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['OrderID']
        restaurant_id = serializer.validated_data['RestaurantID']
        freeze = serializer.validated_data['freeze']

        try:
            order = Order.objects.get(OrderID=order_id, RestaurantID=restaurant_id)

            if freeze and order.Status == OrderStatus.ACTIVE:
                order.Status = OrderStatus.FREEZE
                order.save()
            elif freeze is False and order.Status == OrderStatus.FREEZE:
                order.Status = OrderStatus.ACTIVE
                order.save()

            return Response({'message': 'Success'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)