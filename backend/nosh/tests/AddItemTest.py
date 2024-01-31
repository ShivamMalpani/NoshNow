from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from ..models import Restaurant, UserMod, Item
from ..serializers import ItemSerializer
import json

class AddItemViewTestCase(TestCase):
    def setUp(self):
        # Create test data for the database
        self.owner = UserMod.objects.create(
            first_name="John",
            last_name="Doe",
            mobile_no="1234567890",
            email="john.doe@example.com",
            profile_pic="https://example.com/profile.jpg",
            amount=100
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Main St",
            owner_id=self.owner.UserID
        )

        # Set up a client for making requests
        self.client = Client()

    def test_add_item_success(self):
        url = reverse('add_item')
        data = {
            "userID": self.owner.UserID,
            "name": "New Item",
            "cost": 20,
            "description": "Delicious food",
            "instant_item": True,
            "available": True,
            "quantity": 10
        }

        
        json_data = json.dumps(data)

        response = self.client.post(url, json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().name, "New Item")

    def test_add_item_missing_exceptUserid(self):
        url = reverse('add_item')
        data = {
            "name": "New Item",
            "userID": 1,
           # "cost": 20,
            "description": "Delicious food",
            #"instant_item": True,
            #"available": True,
            "quantity": 10
        }

        json_data = json.dumps(data)
        response = self.client.post(url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Item.objects.count(), 0)

    def test_add_item_restaurant_not_found(self):
        url = reverse('add_item')
        data = {
            "userID": 999,  # Non-existing user ID
            "name": "New Item",
            "cost": 20,
            "description": "Delicious food",
            "instant_item": True,
            "available": True,
            "quantity": 10
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Item.objects.count(), 0)

    
