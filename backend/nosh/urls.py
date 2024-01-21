# urls.py
from django.urls import path, include
from .root import api_root
from .catalogue.students import RestaurantListView, ItemListView
from .orders.restaurants import ActiveOrderListView, OrderHistoryView, FreezeOrderView, CheckoutByUserIdView, UndoCheckoutByOrderIDView, PaymentHistoryView, ViewWalletView

urlpatterns = [
    path("", api_root),
    path('api/catalogue/students/restaurant_list', RestaurantListView.as_view(), name='restaurant_list'),
    path('api/catalogue/students/item_list/<int:restaurant_id>', ItemListView.as_view(), name='item_list'),
    path('api/restaurants/active_orders/', ActiveOrderListView.as_view(), name='active-order-list'),
    path('api/restaurants/order_history/', OrderHistoryView.as_view(), name='order-history'),
    path('api/restaurants/freeze_order/', FreezeOrderView.as_view(), name='freeze-order'),
    path('api/restaurants/checkout/', CheckoutByUserIdView.as_view(), name='checkout-by-user-id'),
    path('api/restaurants/undo_checkout/', UndoCheckoutByOrderIDView.as_view(), name='undo-checkout-by-order-id'),
    path('api/restaurants/payment_history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('api/restaurants/view_wallet/', ViewWalletView.as_view(), name='view-wallet'),
]