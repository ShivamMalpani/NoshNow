# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order
from .serializers import *
from .enum import OrderStatus
import datetime

class CheckoutByUserIdView(generics.CreateAPIView):
    serializer_class = CheckoutByUserIdSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant_id = serializer.validated_data['restaurant_id']
        order_ids = serializer.validated_data['order_ids']
        user_id = serializer.validated_data['user_id']
        try:
            orders = Order.objects.filter(OrderID__in=order_ids, RestaurantID=restaurant_id, Status=OrderStatus.FREEZED.value)
            if orders.count() != len(order_ids):
                return Response({'message': 'Not all orders are freezed'}, status=status.HTTP_400_BAD_REQUEST)
            addresses = set(order.Address for order in orders)
            if len(addresses) != 1:
                return Response({'message': 'Orders have different addresses'}, status=status.HTTP_400_BAD_REQUEST)
            orders.update(Status=OrderStatus.IN_TRANSIT.value, DeliveredBy=user_id, DeliveredAt=datetime.now())
            return Response({'message': 'Checkout successful'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        

class UndoCheckoutByOrderIdView(generics.CreateAPIView):
    serializer_class = UndoCheckoutByOrderIdSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data['order_id']
        try:
            order = Order.objects.get(OrderID=order_id, Status=OrderStatus.PENDING_ACCEPTANCE.value)
            order.Status = OrderStatus.FREEZED.value
            order.DeliveredBy = None  
            order.DeliveredAt = None  
            order.save()
            return Response({'message': 'Undo Checkout successful'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found or status is not IN_TRANSIT'}, status=status.HTTP_404_NOT_FOUND)
        
class ViewCheckoutByUserIdView(generics.CreateAPIView):
    serializer_class = ViewCheckoutByUserIdSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user_id']
        try:
            orders = Order.objects.filter(DeliveredBy=user_id, Status=OrderStatus.PENDING_ACCEPTANCE.value)
            serialized_data = ViewCheckoutByUserIdSerializer2(orders, many=True).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'message': 'No orders found'}, status=status.HTTP_404_NOT_FOUND)
        
class ConfirmDeliveryByStudentIdView(generics.CreateAPIView):
    serializer_class = ConfirmDeliverySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user_id']
        try:
            orders = Order.objects.filter(DeliveredBy=user_id, Status=OrderStatus.PENDING_ACCEPTANCE.value)
            print(orders.count())
            orders.update(Status=OrderStatus.IN_TRANSIT.value)
            return Response({'message': 'Delivery confirmed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': e})

class ReachedByOrderIDView(generics.CreateAPIView):
    serializer_class = ReachedByOrderIDSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data['user_id']
        try:
            orders = Order.objects.filter(DeliveredBy=user_id, Status=OrderStatus.IN_TRANSIT.value)
            if orders.exists():
                orders.update(Status=OrderStatus.DELIVERED_PERSON_REACHED.value)
                return Response({'message': 'Orders marked as deliveryPersonReached successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No orders found with status IN_TRANSIT for the specified user'}, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist:
            return Response({'message': 'An error occurred while updating orders'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeliveredByUserIDView(generics.CreateAPIView):
    serializer_class = DeliveredByUserIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        try:
            orders = Order.objects.filter(DeliveredBy=user_id, Status__in=[OrderStatus.IN_TRANSIT, OrderStatus.DELIVERED_PERSON_REACHED])

            if orders.exists():
                orders.update(Status=OrderStatus.DELIVERED)
                return Response({'message': 'Orders marked as delivered successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No eligible orders found for the specified user'}, status=status.HTTP_404_NOT_FOUND)

        except Order.DoesNotExist:
            return Response({'message': 'An error occurred while updating orders'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)