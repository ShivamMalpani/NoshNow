# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order, User, PaymentHistory
from .serializers import OrderSerializer, OrderHistorySerializer, FreezeOrderSerializer, CheckoutSerializer
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
        

class CheckoutByUserIdView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        restaurant = serializer.validated_data['restaurant_id']
        order_value = serializer.validated_data['order_value']
        # Extract other fields from the serializer

        try:
            user = User.objects.get(id=user_id)

            if useWallet and user.account_balance < order_value:
                return Response({'message': 'Insufficient account balance'}, status=status.HTTP_400_BAD_REQUEST)

            payment = PaymentHistory.objects.create(user=user, restaurant=restaurant, amount=order_value)

            # Order.objects.create(order=payment, product_name=cart_item.product_name, quantity=cart_item.quantity)
            
            # Order.objects.create(user=user, restaurant=restaurant, payment=payment)


            return Response({'message': 'Checkout successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Restaurant.DoesNotExist:
            return Response({'message': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)