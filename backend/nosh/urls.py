# urls.py
from django.urls import path, include
from .restaurants import ActiveOrderListView, OrderHistoryView

urlpatterns = [
    path('api/restaurants/active_orders/', ActiveOrderListView.as_view(), name='active-order-list'),
    path('api/restaurants/order_history/', OrderHistoryView.as_view(), name='order-history'),
]
