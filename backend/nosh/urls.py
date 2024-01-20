# urls.py
from django.urls import path, include
from .restaurants import ActiveOrderListView

urlpatterns = [
    path('api/restaurants/active_orders/', ActiveOrderListView.as_view(), name='active-order-list'),
]
