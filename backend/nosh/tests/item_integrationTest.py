from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Restaurant, Item, CustomUser
from django.contrib.auth.models import User

class ItemAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user and restaurant
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        cls.restaurant = Restaurant.objects.create(name='Test Restaurant', owner_id=cls.user.id)
        cls.item = Item.objects.create(name='Test Item', cost=10, description='Test Description', restaurant_id=cls.restaurant)

    def test_add_item(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('add_item')  # Ensure you have named your URL patterns
        data = {
            'userID': self.user.id,
            'name': 'New Test Item',
            'cost': 15,
            'description': 'New Test Description',
            'restaurant_id': self.restaurant.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.latest('id').name, 'New Test Item')

    def test_update_item(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('update_item', args=[self.item.id])  # Ensure you have named your URL patterns and they accept item_id as an argument
        data = {
            'userID': self.user.id,
            'itemID': self.item.id,
            'name': 'Updated Test Item',
            'cost': 20,
            'description': 'Updated Test Description',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Test Item')

    def test_remove_item(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('remove_item')  # Ensure you have named your URL patterns
        data = {
            'userID': self.user.id,
            'itemID': self.item.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 0)
