from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from ..models import Item, UserMod, Restaurant, Order, PaymentHistory
from ..enum import OrderType, PaymentType, PaymentStatus, OrderStatus, PaymentReason
from ..serializers import PaymentHistorySerializer, CreateOrderSerializer, OrderInputSerializer, OrderHistorySerializer
from ..connection import mydb

Cart = mydb["Cart"]
OrderDB = mydb["Order"]


class CreateOrderView(APIView):
    def post(self, request):
        input_serializer = OrderInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        userID = self.request.data.get("userID")
        paymentType = self.request.data.get("paymentType")
        orderType = self.request.data.get("orderType")

        entry = Cart.find_one({"_id": str(userID)})
        if entry is None:
            return Response("Cart is empty", status=status.HTTP_400_BAD_REQUEST)
        
        total_amount = 0
        paymentStatus = ""
        
        check_restaurant = -1
        for i in entry["item_list"].keys():
            try:
                item = Item.objects.get(pk=int(i))
            except Item.DoesNotExist:
                return Response("An Item does not exist please clear your cart", status=status.HTTP_404_NOT_FOUND)
            if check_restaurant == -1:
                check_restaurant = item.restaurant_id
            else:
                if check_restaurant != item.restaurant_id:
                    return Response("Items in your cart belong to different restaurants", status=status.HTTP_400_BAD_REQUEST)
            if item.available == False:
                return Response("Item "+item.name+" is currently not available please remove it from Cart", status=status.HTTP_400_BAD_REQUEST)
            if item.instant_item == True and item.quantity < entry["item_list"][i]:
                return Response("Only "+item.quantity+" "+item.name+" are left", status=status.HTTP_400_BAD_REQUEST)
            total_amount += entry["item_list"][i]*(item.cost)
        
        try:
            restaurant = Restaurant.objects.get(pk=check_restaurant.id)
        except Restaurant.DoesNotExist:
            return Response("Restaurant do not exist, clear the cart", status=status.HTTP_404_NOT_FOUND)
        
        if (orderType in [OrderType.SLOT.value, OrderType.STUDENT.value, OrderType.STUDENT_SLOT.value] and paymentType == PaymentType.COD.value):
            return Response("COD Payment is not accepted for this order", status=status.HTTP_400_BAD_REQUEST)
        
        if paymentType == PaymentType.WALLET.value:
            try:
                user = UserMod.objects.get(UserID = userID)
                restuarant_owner = UserMod.objects.get(UserID = restaurant.owner_id)
            except UserMod.DoesNotExist:
                return Response("User Not found", status=status.HTTP_404_NOT_FOUND)
            if user.amount < total_amount:
                return Response("Amount insufficient in wallet", status=status.HTTP_400_BAD_REQUEST)
            
            user.amount -= total_amount
            user.save()
            restuarant_owner.amount += total_amount
            restuarant_owner.save()
            paymentStatus = PaymentStatus.PAID.value

            transaction_dict = {
                "UserID" : userID,
                "Payee" : restaurant.owner_id,
                "Amount" : total_amount,
                "Reason" : PaymentReason.ORDER_PLACE
            }
            payment_history_serializer = PaymentHistorySerializer(data=transaction_dict)
            if payment_history_serializer.is_valid():
                payment_instance = payment_history_serializer.save()
            else:
                return Response(payment_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif paymentType == PaymentType.COD.value:
            paymentStatus = PaymentStatus.NOT_PAID.value
        
        order_dict = {
            "CustomerID" : userID,
            "Address" : self.request.data.get("Address"),
            "Amount" : total_amount,
            "Status" : OrderStatus.ACTIVE.value,
            "PaymentStatus" : paymentStatus,
            "PaymentType" : paymentType,
            "RestaurantID" : restaurant.id
        }
        order_serializer = CreateOrderSerializer(data=order_dict)
        if order_serializer.is_valid():
            order_instance = order_serializer.save()
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if paymentStatus == PaymentStatus.PAID.value:
            payment_instance.OrderID = order_instance
            payment_instance.save()
        
        restaurant.value += total_amount
        restaurant.save()

        Cart.delete_one({"_id": str(userID)})
        OrderDB.insert_one({"_id": str(order_instance.OrderID), "order_list": entry["item_list"]})

        return Response("Order created successfully", status=status.HTTP_200_OK)
    

class CancelOrderView(APIView):
    def post(self, request):
        userID = self.request.data.get("userID")
        orderID = self.request.data.get("orderID")

        try:
            order = Order.objects.get(OrderID=orderID)
        except Order.DoesNotExist:
            return Response("Order does not exist", status=status.HTTP_400_BAD_REQUEST)
        
        restaurant = order.RestaurantID
        
        if (userID != order.CustomerID and userID != restaurant.owner_id):
            return Response("Unauthorized user", status=status.HTTP_403_FORBIDDEN)
        
        if (userID == order.CustomerID and order.Status != OrderStatus.ACTIVE.value):
            return Response("Only active order can be cancelled", status=status.HTTP_400_BAD_REQUEST)
        
        if (userID == restaurant.owner_id and order.Status != OrderStatus.ACTIVE.value and order.Status != OrderStatus.FREEZED.value):
            return Response("Only active or freezed orders can be cancelled", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            transaction = PaymentHistory.objects.get(OrderID=orderID)
        except PaymentHistory.DoesNotExist:
            transaction = None

        if transaction is not None and order.PaymentStatus == PaymentStatus.PAID.value:
            transaction_dict = {
                "UserID" : transaction.Payee,
                "Payee" : transaction.UserID,
                "Amount" : transaction.Amount,
                "OrderID" : transaction.OrderID.OrderID,
                "Reason" : PaymentReason.ORDER_CANCELLATION
            }
            transaction_serializer = PaymentHistorySerializer(data = transaction_dict)
            if transaction_serializer.is_valid():
                transaction_serializer.save()
            else:
                return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                customer = UserMod.objects.get(UserID=order.CustomerID)
                restaurant_owner = UserMod.objects.get(UserID=restaurant.owner_id)
            except UserMod.DoesNotExist:
                return Response("User do not exist", status=status.HTTP_404_NOT_FOUND)
            
            customer.amount += transaction.Amount
            customer.save()
            restaurant_owner.amount -= transaction.Amount
            restaurant_owner.save()
            order.PaymentStatus = PaymentStatus.REFUND.value
        
        order.Status = OrderStatus.CANCELLED.value
        order.save()
        restaurant.value -= order.Amount
        restaurant.save()
        return Response("order cancelled", status=status.HTTP_200_OK)


class StudentOrderHistoryView(generics.ListAPIView):
    serializer_class = OrderHistorySerializer

    def get_queryset(self):
        userID = self.kwargs.get('userID')
        return Order.objects.filter(CustomerID=userID)