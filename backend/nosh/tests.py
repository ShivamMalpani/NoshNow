from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Order, UserMod, PaymentHistory
from .enum import OrderStatus

class ActiveOrderListViewTest(APITestCase):
    def setUp(self):
        self.restaurant_id = 1
        self.order = Order.objects.create(
            CustomerID=1, Address='Test Address', Status=OrderStatus.ACTIVE,
            PaymentStatus='Pending', DeliveredBy=1, RestaurantID=self.restaurant_id
        )

    def test_get_active_orders(self):
        url = reverse('active-order-list')
        response = self.client.get(url, {'restaurantID': self.restaurant_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['OrderID'], self.order.OrderID)
        self.assertEqual(response.data[0]['Status'], OrderStatus.ACTIVE)

class OrderHistoryViewTest(APITestCase):
    def setUp(self):
        self.restaurant_id = 1
        self.order = Order.objects.create(
            CustomerID=1, Address='Test Address', Status='Delivered',
            PaymentStatus='Paid', DeliveredBy=1, RestaurantID=self.restaurant_id
        )

    def test_get_order_history(self):
        url = reverse('order-history')
        response = self.client.get(url, {'restaurantID': self.restaurant_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['OrderID'], self.order.OrderID)
        self.assertEqual(response.data[0]['Status'], 'Delivered')

class FreezeOrderViewTest(APITestCase):
    def setUp(self):
        self.order_id = 1
        self.restaurant_id = 1
        self.order = Order.objects.create(
            CustomerID=1, Address='Test Address', Status=OrderStatus.ACTIVE,
            PaymentStatus='Pending', DeliveredBy=1, RestaurantID=self.restaurant_id
        )

    def test_freeze_order(self):
        url = reverse('freeze-order')
        data = {'OrderID': self.order_id, 'RestaurantID': self.restaurant_id, 'freeze': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.Status, OrderStatus.FREEZED)

# class CheckoutByUserIdViewTest(APITestCase):
#     def setUp(self):
#         self.user_id = 1
#         self.user = UserMod.objects.create(
#             first_name='Test', last_name='User', mobile_no='1234567890',
#             email='test@example.com', amount=1000
#         )

#     def test_checkout_by_user_id(self):
#         url = reverse('checkout-by-user-id')
#         data = {'user_id': self.user_id, 'restaurant_id': 1, 'order_value': 50.00, 'useWallet': True}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.user.refresh_from_db()
#         self.assertLessEqual(self.user.amount, 950)  # Assuming the order_value is deducted from the user's wallet

class UndoCheckoutByOrderIDViewTest(APITestCase):
    def setUp(self):
        self.order_id = 1
        self.user_id = 1
        self.user = UserMod.objects.create(
            UserID=self.user_id, first_name='Test', last_name='User', mobile_no='1234567890',
            email='test@example.com', amount=1000
        )
        self.order = Order.objects.create(
            OrderID=self.order_id, CustomerID=self.user_id, Status=OrderStatus.ACTIVE,
            PaymentStatus='Pending', RestaurantID=2, DeliveredBy=1
        )
        self.payment = PaymentHistory.objects.create(
            TransactionID=1, UserID=self.user_id, Payee=2, Amount=50
        )
        self.order.TransactionID = self.payment.TransactionID
        self.order.save()

    def test_undo_checkout_by_order_id(self):
        url = reverse('undo-checkout-by-order-id')
        data = {'order_id': self.order_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.Status, OrderStatus.CANCELLED)
        self.user.refresh_from_db()
        self.assertEqual(self.user.amount, 1050)  # Assuming the order_value is refunded to the user's wallet




class PaymentHistoryViewTest(APITestCase):
    def setUp(self):
        self.user_id = 1
        self.transactionID = 1
        self.payment_history = PaymentHistory.objects.create(
            UserID=self.user_id, Payee=2, Amount=50
        )

    def test_get_payment_history(self):
        url = reverse('payment-history')
        response = self.client.get(url, {'user_id': self.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['TransactionID'], self.payment_history.TransactionID)

class ViewWalletViewTest(APITestCase):
    def setUp(self):
        self.user_id = 1
        self.user = UserMod.objects.create(
            first_name='Test', last_name='User', mobile_no='1234567890',
            email='test@example.com', amount=1000
        )

    def test_view_wallet(self):
        url = reverse('view-wallet')
        response = self.client.get(url, {'user_id': self.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '1000.00')  # Assuming the amount is serialized as a string

