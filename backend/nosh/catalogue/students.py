from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Restaurant, Item
from ..serializers import RestaurantListSerializer, ItemSerializer
from ..connection import mydb
from django.utils import timezone

Cart = mydb["Cart"]


class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantListSerializer

    def get_queryset(self):
        current_time = timezone.now().time()
        queryset = Restaurant.objects.all()
        for restaurant in queryset:
            restaurant.is_open = restaurant.start_time <= current_time <= restaurant.end_time
        return queryset



class ItemListView(APIView):
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {} 
        items = Item.objects.filter(restaurant_id=restaurant_id)
        item_serializer = ItemSerializer(items, many=True)
        data = item_serializer.data

        return Response(data, status=status.HTTP_200_OK)
    

class AddCartView(APIView):
    def post(self, request):
        userID = str(self.request.data.get("userID"))
        entry = Cart.find_one({"_id": userID})
        data = request.data

        try:
            item = Item.objects.get(id=data["item_id"])
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        if entry is not None:
            check_item = list(entry["item_list"].keys())[0]
            check_item_restaurant = Item.objects.get(pk=int(check_item)).restaurant_id
            current_restaurant = item.restaurant_id
            if (check_item_restaurant != current_restaurant):
                return Response("Wrong Restaurant", status=status.HTTP_400_BAD_REQUEST)
            
            entry["item_list"][data["item_id"]] = data["quantity"]
            Cart.update_one({"_id": userID}, {"$set": {"item_list": {str(data["item_id"]): data["quantity"]}}})
            return Response("Success", status=status.HTTP_200_OK)
        else:
            Cart.insert_one({"_id": userID, "item_list": {str(data["item_id"]): data["quantity"]}})
            return Response("Success", status=status.HTTP_200_OK)
        

class ClearCartView(APIView):
    def post(self, request):
        userID = str(self.request.data.get("userID"))
        Cart.delete_one({"_id": userID})
        return Response("success")


class ViewCartView(APIView):
    def get(self, request, userID):
        entry = Cart.find_one({"_id": str(userID)})

        if entry is None:
            return Response({"message" : "Cart is Empty"}, status=status.HTTP_200_OK)
        
        else:
            total_amount = 0
            data = {}
            data["items"] = []
            for i in entry["item_list"].keys():
                item = Item.objects.get(pk = int(i))
                amount = entry["item_list"][i]*(item.cost)
                total_amount += amount
                item_dict = {
                    "id" : i,
                    "name" : item.name,
                    "quantity" : entry["item_list"][i],
                    "amount" : amount
                }
                data["items"].append(item_dict)
            data["total_amount"] = total_amount
            return Response(data, status=status.HTTP_200_OK)
