from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Restaurant
from ..serializers import ItemSerializer


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