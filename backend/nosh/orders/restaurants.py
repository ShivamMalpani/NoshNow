# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers import *
from ..enum import OrderStatus


class ActiveOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurantID')
        return Order.objects.filter(RestaurantID=restaurant_id, Status=OrderStatus.ACTIVE.value)


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

            if freeze and order.Status == OrderStatus.ACTIVE.value:
                order.Status = OrderStatus.FREEZED.value
                order.save()
            elif freeze is False and order.Status == OrderStatus.FREEZED.value:
                order.Status = OrderStatus.ACTIVE.value
                order.save()

            return Response({'message': 'Success'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        

# class CheckoutByUserIdView(generics.CreateAPIView):
#     serializer_class = CheckoutSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user_id = serializer.validated_data['user_id']
#         restaurant = serializer.validated_data['restaurant_id']
#         order_value = serializer.validated_data['order_value']
#         useWallet = serializer.validated_data['useWallet']
#         # Extract other fields from the serializer

#         try:
#             user = UserMod.objects.get(id=user_id)

#             if useWallet and user.account_balance < order_value:
#                 return Response({'message': 'Insufficient account balance'}, status=status.HTTP_400_BAD_REQUEST)

#             payment = PaymentHistory.objects.create(user=user, restaurant=restaurant, amount=order_value)

#             # Order.objects.create(order=payment, product_name=cart_item.product_name, quantity=cart_item.quantity)
            
#             # Order.objects.create(user=user, restaurant=restaurant, payment=payment)


#             return Response({'message': 'Checkout successful'}, status=status.HTTP_200_OK)
#         except user.DoesNotExist:
#             return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except restaurant.DoesNotExist:
#             return Response({'message': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        

# class UndoCheckoutByOrderIDView(generics.CreateAPIView):
#     serializer_class = UndoCheckoutSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         order_id = serializer.validated_data['order_id']
#         print(order_id)
#         try:
#             order = Order.objects.get(OrderID=order_id)
#             print(order)
#             user_id = order.CustomerID
#             print(type(user_id))
#             print(user_id)
#             user = UserMod.objects.get(UserID=user_id)
#             print(user)
#             transactionID = order.TransactionID
#             print(transactionID)
#             if transactionID is not None:
#                 payment_details = PaymentHistory.objects.get(TransactionID=transactionID)
#                 user.amount += payment_details.Amount
#                 user.save()
#                 payee = order.RestaurantID
#                 restaurant = UserMod.objects.get(UserID = payee)
#                 restaurant.amount -= payment_details.Amount
#                 restaurant.save()
#             order.status = OrderStatus.CANCELLED.value
#             order.save()
#             return Response({'message': 'Undo Checkout successful'}, status=status.HTTP_200_OK)
#         except UserMod.DoesNotExist:
#             return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Order.DoesNotExist:
#             return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentHistorySerializer

    def get_queryset(self):
        UserID = self.request.query_params.get('user_id')
        print(UserID)
        return PaymentHistory.objects.filter(UserID=UserID)
    
class ViewWalletView(generics.RetrieveAPIView):
    serializer_class = ViewWalletSerializer
    queryset = UserMod.objects.all()

    def get_object(self):
        user_id = self.request.query_params.get('user_id')
        user = generics.get_object_or_404(UserMod, UserID=user_id)
        return user