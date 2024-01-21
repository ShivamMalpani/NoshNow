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
            entry["item_list"][data["item_id"]] = data["quantity"]
            Cart.update_one({"_id": userID}, {"$set": {"item_list": {str(data["item_id"]): data["quantity"]}}})
            return Response("Success", status=status.HTTP_200_OK)
        else:
            Cart.insert_one({"_id": userID, "item_list": {str(data["item_id"]): data["quantity"]}})
            return Response("Success", status=status.HTTP_200_OK)