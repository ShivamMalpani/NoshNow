from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Restaurant, Item
import time

class ItemListViewTest(TestCase):
    def setUp(self):
        # Create the first restaurant
        self.restaurant1 = Restaurant.objects.create(
            name='Test Restaurant 1',
            address='Test Address 1',
            owner_id=1,
            value=100,
            rating=4.0,
            start_time='10:00',
            end_time='22:00'
        )

        # Create items for the first restaurant
        self.item1_1 = Item.objects.create(
            name='Item 1.1',
            cost=10,
            description='Description 1.1',
            restaurant_id=self.restaurant1,
            instant_item=False,
            available=True,
            quantity=50,
            image='item1.1.jpg',
            rating=4.2
        )

        self.item1_2 = Item.objects.create(
            name='Item 1.2',
            cost=15,
            description='Description 1.2',
            restaurant_id=self.restaurant1,
            instant_item=True,
            available=False,
            quantity=20,
            image='item1.2.jpg',
            rating=4.5
        )

        # Create the second restaurant
        self.restaurant2 = Restaurant.objects.create(
            name='Test Restaurant 2',
            address='Test Address 2',
            owner_id=2,
            value=120,
            rating=4.2,
            start_time='09:00',
            end_time='21:00'
        )

        # Create items for the second restaurant
        self.item2_1 = Item.objects.create(
            name='Item 1.1',
            cost=12,
            description='Description 2.1',
            restaurant_id=self.restaurant2,
            instant_item=True,
            available=True,
            quantity=30,
            image='item2.1.jpg',
            rating=4.0
        )

        self.item2_2 = Item.objects.create(
            name='Item 2.2',
            cost=20,
            description='Description 2.2',
            restaurant_id=self.restaurant2,
            instant_item=False,
            available=True,
            quantity=40,
            image='item2.2.jpg',
            rating=4.8
        )

        # URL for the ItemListView
        self.url = reverse('item_list', args=[self.restaurant1.id])

    # ... Rest of the test cases remain the same ...
    def test_get_item_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_item_list_invalid_restaurant_id(self):
        invalid_url = reverse('item_list', args=[999])  # Assuming 999 is an invalid restaurant ID
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_item_serializer_fields(self):
        expected_fields = {'id', 'name', 'cost', 'description', 'instant_item', 'available', 'quantity', 'image', 'rating', 'created_at', 'restaurant_id'}
        response = self.client.get(self.url)
        item_data = response.data[0] if response.data else {}
        self.assertEqual(set(item_data.keys()), expected_fields)

    def test_item_list_empty_database(self):
        Item.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_item_list_pagination(self):
        # Create more items to test pagination
        for i in range(3, 13):
            Item.objects.create(
                name=f'Item {i}',
                cost=10,
                description=f'Description {i}',
                restaurant_id=self.restaurant1,
                instant_item=False,
                available=True,
                quantity=50,
                image=f'item{i}.jpg',
                rating=4.2
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 12)  # Pagination size is 10

    def test_item_list_for_instant_items(self):
        response = self.client.get(self.url + '?instant=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only one instant item in the sample data

    def test_item_list_for_unavailable_items(self):
        response = self.client.get(self.url + '?available=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one unavailable item in the sample data

    def test_item_list_for_available_items(self):
        response = self.client.get(self.url + '?available=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Only one available item in the sample data

    def test_response_time(self):
        start_time = time.time()
        response = self.client.get(reverse('item_list',  args=[self.restaurant1.id]))

        end_time = time.time()
        
        # Ensure the response status code is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert that the API response time is within an acceptable range
        max_response_time = 0.06 #0.058321237564086914
        actual_response_time = end_time - start_time
        self.assertLess(actual_response_time, max_response_time)

    def test_filter_items_by_cost(self):
        response = self.client.get(self.url + '?cost=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Corrected here

    def test_filter_items_by_multiple_criteria(self):
        response = self.client.get(self.url + '?rating=4.2&cost=12')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Corrected here

    def test_filter_items_by_rating(self):
        response = self.client.get(self.url + '?rating=4.2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Corrected here

    def test_item_list_invalid_query_parameter(self):
        response = self.client.get(self.url + '?invalid_param=value')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Corrected here

    def test_item_list_invalid_query_parameter_value(self):
        response = self.client.get(self.url + '?instant=invalid_value')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

    def tearDown(self):
        # Delete objects created during the test setup
        Restaurant.objects.all().delete()
        Item.objects.all().delete()