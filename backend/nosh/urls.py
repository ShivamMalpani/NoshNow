# urls.py
from django.urls import path, include
from .root import api_root
from rest_framework_simplejwt.views import TokenRefreshView
from .user.user import RegistrationView, VerifyEmailOTP, SendEmailOtpView, LoginView, LogoutView
from .catalogue.students import RestaurantListView, ItemListView, AddCartView, ClearCartView, ViewCartView, ViewRestaurantView
from .catalogue.restaurant import AddItemView, UpdateItemView, RemoveItemView, ViewItemAPIView, UpdateItemStatusView, UpdateItemQuantityView
from .orders.student import CreateOrderView, CancelOrderView, StudentOrderHistoryView, ViewOrderView
from .orders.restaurants import ActiveOrderListView, OrderHistoryView, FreezeOrderView, PaymentHistoryView, ViewWalletView
from .delivery import *

urlpatterns = [
    path("", api_root),
    path('api/user/user/register_user', RegistrationView.as_view(), name='register_user'),
    path('api/user/user/verify_email_otp', VerifyEmailOTP.as_view(), name='verify_email_otp'),
    path('api/user/user/send_email_otp', SendEmailOtpView.as_view(), name='send_email_otp'),
    path('api/user/user/login', LoginView.as_view(), name='login'),
    path('api/user/user/logout', LogoutView.as_view(), name='logout'),
    path('api/user/user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/catalogue/students/restaurant_list', RestaurantListView.as_view(), name='restaurant_list'),
    path('api/catalogue/students/item_list/<int:restaurant_id>', ItemListView.as_view(), name='item_list'),
    path('api/catalogue/students/view_restaurant/<int:restaurant_id>', ViewRestaurantView.as_view(), name='view_restaurant'),
    path('api/catalogue/students/add_cart', AddCartView.as_view(), name='add_cart'),
    path('api/catalogue/students/clear_cart', ClearCartView.as_view(), name='clear_cart'),
    path('api/catalogue/students/view_cart/<int:userID>', ViewCartView.as_view(), name='view_cart'),
    path('api/catalogue/restaurant/add_item', AddItemView.as_view(), name='add_item'),
    path('api/catalogue/restaurant/update_item', UpdateItemView.as_view(), name='update_item'),
    path('api/catalogue/restaurant/delete_item', RemoveItemView.as_view(), name='delete_item'),
    path('api/catalogue/restaurant/view_item/<int:id>', ViewItemAPIView.as_view(), name='view_item'),
    path('api/catalogue/restaurant/update_item_status', UpdateItemStatusView.as_view(), name='update_item_status'),
    path('api/catalogue/restaurant/update_item_quantity', UpdateItemQuantityView.as_view(), name='update_item_quantity'),
    path('api/order/student/create_order', CreateOrderView.as_view(), name='create_order'),
    path('api/order/student/cancel_order', CancelOrderView.as_view(), name='cancel_order'),
    path('api/order/student/view_order_history/<int:userID>', StudentOrderHistoryView.as_view(), name='view_order_history'),
    path('api/order/student/view_order/<int:orderID>/<int:userID>/', ViewOrderView.as_view(), name='view_order'),
    path('api/restaurants/active_orders/', ActiveOrderListView.as_view(), name='active-order-list'),
    path('api/checkout_by_user/', CheckoutByUserIdView.as_view(), name='checkout-by-user-id'),
    path('api/undo_checkout_by_order/', UndoCheckoutByOrderIdView.as_view(), name='undo-checkout-by-order-id'),
    path('api/restaurants/order_history/', OrderHistoryView.as_view(), name='order-history'),
    path('api/restaurants/freeze_order/', FreezeOrderView.as_view(), name='freeze-order'),
    path('api/list_checkout_by_user/', ListCheckoutByUserIdView.as_view(), name='view-checkout-by-user-id'),
    path('api/confirm_delivery_by_student/', ConfirmDeliveryByStudentIdView.as_view(), name='confirm-delivery-by-student-id'),
    path('api/reached_by_order/', ReachedByOrderIDView.as_view(), name='reached-by-order-id'),
    path('api/delivered_by_user/', DeliveredByUserIDView.as_view(), name='delivered-by-user-id'),
    # path('api/restaurants/checkout/', CheckoutByUserIdView.as_view(), name='checkout-by-user-id'),
    # path('api/restaurants/undo_checkout/', UndoCheckoutByOrderIDView.as_view(), name='undo-checkout-by-order-id'),
    path('api/restaurants/payment_history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('api/restaurants/view_wallet/', ViewWalletView.as_view(), name='view-wallet'),
]