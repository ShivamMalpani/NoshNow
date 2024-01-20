# urls.py
from django.urls import path, include
from .restaurants import ActiveOrderListView, OrderHistoryView, FreezeOrderView

urlpatterns = [
    path('api/restaurants/active_orders/', ActiveOrderListView.as_view(), name='active-order-list'),
    path('api/restaurants/order_history/', OrderHistoryView.as_view(), name='order-history'),
    path('api/restaurants/freeze_order/', FreezeOrderView.as_view(), name='freeze-order'),
]
