from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Restaurant, Item
from ..serializers import ItemSerializer, ItemUpdateSerializer


class AddItemView(APIView):
    def post(self, request):
        userID = self.request.data.get("userID")

        try:
            restaurant = Restaurant.objects.get(owner_id=userID)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found for the given user ID'}, status=status.HTTP_404_NOT_FOUND)
        
        item_data = request.data
        item_data['restaurant_id'] = restaurant.id
        serializer = ItemSerializer(data=item_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateItemView(APIView):
    def post(self, request):
        item_id = self.request.data.get("itemID")
        user_id = self.request.data.get("userID")

        try:
            restaurant = Restaurant.objects.get(owner_id=user_id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found for the given user ID'}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found for the given item ID'}, status=status.HTTP_404_NOT_FOUND)
        
        if restaurant != item.restaurant_id:
            return Response({'error': 'Restaurant ID of the user does not match the restaurant ID of the item'},
                            status=status.HTTP_403_FORBIDDEN)

        item_data = request.data
        item_data['restaurant_id'] = restaurant.id
        serializer = ItemUpdateSerializer(instance=item, data=item_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RemoveItemView(APIView):
    def post(self, request):
        userID = request.data.get("userID")
        item_id = request.data.get("itemID")

        try:
            restaurant = Restaurant.objects.get(owner_id=userID)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found for the given user ID'}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found for the given item ID'}, status=status.HTTP_404_NOT_FOUND)
        
        if restaurant != item.restaurant_id:
            return Response({'error': 'Restaurant ID of the user does not match the restaurant ID of the item'},
                            status=status.HTTP_403_FORBIDDEN)

        item.delete()
        return Response({'message': 'Item removed successfully'}, status=status.HTTP_200_OK)


class ViewItemAPIView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'


class UpdateItemStatusView(APIView):
    def post(self, request):
        userID = request.data.get("userID")
        item_id = request.data.get("itemID")
        available = request.data.get("available")

        try:
            restaurant = Restaurant.objects.get(owner_id=userID)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found for the given user ID'}, status=status.HTTP_404_NOT_FOUND)
    
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found for the given item ID'}, status=status.HTTP_404_NOT_FOUND)
        
        if restaurant != item.restaurant_id:
            return Response({'error': 'Restaurant ID of the user does not match the restaurant ID of the item'},
                            status=status.HTTP_403_FORBIDDEN)

        item_data = {
            "available" : available,
            "restaurant_id" : item.restaurant_id.id
        }
        serializer = ItemUpdateSerializer(instance=item, data=item_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateItemQuantityView(APIView):
    def post(self, request):
        userID = request.data.get("userID")
        item_id = request.data.get("itemID")
        quantity = request.data.get("quantity")

        try:
            restaurant = Restaurant.objects.get(owner_id=userID)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found for the given user ID'}, status=status.HTTP_404_NOT_FOUND)
    
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found for the given item ID'}, status=status.HTTP_404_NOT_FOUND)
        
        if restaurant != item.restaurant_id:
            return Response({'error': 'Restaurant ID of the user does not match the restaurant ID of the item'},
                            status=status.HTTP_403_FORBIDDEN)

        item_data = {
            "quantity" : quantity,
            "restaurant_id" : item.restaurant_id.id
        }
        serializer = ItemUpdateSerializer(instance=item, data=item_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)