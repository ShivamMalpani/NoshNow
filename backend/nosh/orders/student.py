from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Item, UserMod, Restaurant
from ..enum import OrderType, PaymentType, PaymentStatus, OrderStatus
from ..serializers import PaymentHistorySerializer, CreateOrderSerializer, OrderInputSerializer
from ..connection import mydb

Cart = mydb["Cart"]
Order = mydb["Order"]


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
            except UserMod.DoesNotExist:
                return Response("User Not found", status=status.HTTP_404_NOT_FOUND)
            if user.amount < total_amount:
                return Response("Amount insufficient in wallet", status=status.HTTP_400_BAD_REQUEST)
            
            user.amount -= total_amount
            user.save()
            paymentStatus = PaymentStatus.PAID.value

            transaction_dict = {
                "UserID" : userID,
                "Payee" : restaurant.owner_id,
                "Amount" : total_amount,
            }
            payment_history_serializer = PaymentHistorySerializer(data=transaction_dict)
            if payment_history_serializer.is_valid():
                payment_instance = payment_history_serializer.save()
                transaction_id = payment_instance.TransactionID
            else:
                return Response(payment_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif paymentType == PaymentType.COD.value:
            paymentStatus = PaymentStatus.NOT_PAID.value
            transaction_id = 0
        
        order_dict = {
            "CustomerID" : userID,
            "Address" : self.request.data.get("Address"),
            "Status" : OrderStatus.ACTIVE.value,
            "TransactionID" : transaction_id,
            "PaymentStatus" : paymentStatus,
            "PaymentType" : paymentType,
            "RestaurantID" : restaurant.id
        }
        order_serializer = CreateOrderSerializer(data=order_dict)
        if order_serializer.is_valid():
            order_instance = order_serializer.save()
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        restaurant.value += total_amount
        restaurant.save()

        Cart.delete_one({"_id": str(userID)})
        Order.insert_one({"_id": str(order_instance.OrderID), "order_list": entry["item_list"]})

        return Response("Order created successfully", status=status.HTTP_200_OK)