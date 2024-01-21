from rest_framework import generics
from ..models import Restaurant
from ..serializers import RestaurantListSerializer
from django.utils import timezone


class RestaurantListView(generics.ListAPIView):
    serializer_class = RestaurantListSerializer

    def get_queryset(self):
        current_time = timezone.now().time()
        queryset = Restaurant.objects.filter(start_time__lte=current_time, end_time__gte=current_time)
        return queryset