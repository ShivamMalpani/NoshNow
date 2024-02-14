from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Restaurant, Item, UserMod, ItemDocument
from ..serializers import RestaurantListSerializer, ItemSerializer, OwnerSerializer
from ..connection import mydb
from django.utils import timezone

Cart = mydb["Cart"]
Feedback = mydb["Feedback"]


class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantListSerializer

    def get_queryset(self):
        current_time = timezone.now().time()
        queryset = Restaurant.objects.all()
        is_open = self.request.query_params.get('is_open', None)
        if is_open is not None:
            is_open = is_open.lower() in ['true', '1']
            for restaurant in queryset:
                restaurant.is_open = restaurant.start_time <= current_time <= restaurant.end_time
            queryset = [restaurant for restaurant in queryset if restaurant.is_open == is_open]
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


class ViewRestaurantView(APIView):
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        
        owner = restaurant.owner_id
        owner_details = UserMod.objects.get(pk=owner)
        owner_serializer = OwnerSerializer(owner_details)
        data = {}
        data["owner"] = owner_serializer.data

        entry = Feedback.find_one({"_id": str(restaurant_id)})
        data["feedback_list"] = []
        for i in entry["feedback_list"].keys():
            user = UserMod.objects.get(pk=int(i))
            feedback_dict = {
                "user" : user.first_name+" "+user.last_name,
                "feedback" : entry["feedback_list"][i],
                "id" : int(i)
            }
            data["feedback_list"].append(feedback_dict)
        
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
            
            if data["quantity"] > 0:
                entry["item_list"][str(data["item_id"])] = data["quantity"]
                Cart.update_one({"_id": userID}, {"$set": {"item_list": entry["item_list"]}})
            elif data["quantity"] == 0:
                entry["item_list"].pop(str(data["item_id"]), None)
                if len(entry["item_list"]) == 0:
                    Cart.delete_one({"_id": userID})
                else:
                    Cart.update_one({"_id": userID}, {"$set": {"item_list": entry["item_list"]}})
            else:
                return Response("Quantity should not be negative", status=status.HTTP_400_BAD_REQUEST)
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
                    "amount" : amount,
                    "image" : item.image,
                    "rating" : item.rating
                }
                data["items"].append(item_dict)
            data["total_amount"] = total_amount
            return Response(data, status=status.HTTP_200_OK)

class ItemSearchView(DocumentViewSet):
    document = ItemDocument
    serializer_class = ItemSerializer

    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q:
            return ItemDocument.search().query('multi_match', query=q, fields=['name', 'description'])
        else:
            return ItemDocument.search().query('match_all')