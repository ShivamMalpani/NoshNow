from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Restaurant, Item
from ..serializers import RestaurantListSerializer, ItemSerializer
from django.utils import timezone


class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantListSerializer

    def get_queryset(self):
        current_time = timezone.now().time()
        queryset = Restaurant.objects.filter(start_time__lte=current_time, end_time__gte=current_time)
        return queryset


class ItemListView(APIView):
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {}
        restaurant_serializer = RestaurantListSerializer(restaurant)
        data = restaurant_serializer.data        
        items = Item.objects.filter(restaurant_id=restaurant_id)
        item_serializer = ItemSerializer(items, many=True)
        data['items'] = item_serializer.data

        return Response(data, status=status.HTTP_200_OK)