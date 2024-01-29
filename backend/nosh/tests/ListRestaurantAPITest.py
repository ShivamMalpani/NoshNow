from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.db.models import Count
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import datetime
from ..models import Restaurant
import time

class ListRestaurantAPITest(TestCase):
    def setUp(self):
        # Create some sample data for testing
        self.restaurant1 = Restaurant.objects.create(
            name='Restaurant 1',
            address='Address 1',
            owner_id = 1,
            value=100,
            rating=4.5,
            start_time='10:00',
            end_time='22:00'
        )

        self.restaurant2 = Restaurant.objects.create(
            name='Restaurant 2',
            address='Address 2',
            owner_id = 2,
            value=150,
            rating=4.2,
            start_time='08:00',
            end_time='20:00'
        )

        duplicates = Restaurant.objects.values('name').annotate(name_count=Count('name')).filter(name_count__gt=1)
        if duplicates:
            raise ValueError("Duplicate restaurant names found in test setup.")

    def test_empty_database(self):
        Restaurant.objects.all().delete()
        response = self.client.get(reverse('restaurant_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_large_database(self):
        for i in range(3, 1003):
            Restaurant.objects.create(id=i, name=f'Restaurant {i}', image=f'image{i}.jpg', address=f'Address {i}', owner_id = i,value=i, rating=4.5)
        response = self.client.get(reverse('restaurant_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1002)

    def test_response_time(self):
        start_time = time.time()
        response = self.client.get(reverse('restaurant_list'))
        end_time = time.time()
        
        # Ensure the response status code is as expected
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert that the API response time is within an acceptable range
        max_response_time = 0.01 #0.0012950897216796875
        actual_response_time = end_time - start_time
        self.assertLess(actual_response_time, max_response_time)

    def test_get_restaurant_by_name(self):
        response = self.client.get(reverse('restaurant_list'), {'name': self.restaurant1.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.restaurant1.name)

    def test_get_restaurant_by_minimum_rating(self):
        min_rating = 4.0
        response = self.client.get(reverse('restaurant_list'), {'min_rating': min_rating})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that all restaurants in the response have a rating greater than or equal to the minimum rating
        for restaurant in response.data:
            self.assertGreaterEqual(restaurant['rating'], min_rating)

    def test_get_restaurant_by_maximum_value(self):
        max_value = 150
        response = self.client.get(reverse('restaurant_list'), {'max_value': max_value})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that all restaurants in the response have a value less than or equal to the maximum value
        for restaurant in response.data:
            self.assertLessEqual(restaurant['value'], max_value)

   

    def test_restaurant_list_pagination(self):
        for _ in range(100,115):
            Restaurant.objects.create(
            name=f'Restaurant {_}',
            address=f'Address {_}',
            value=100,
            owner_id = _,
            rating=4.0,
            start_time='12:00',
            end_time='20:00'
        )

        response = self.client.get(reverse('restaurant_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 17) # Pagination size is 17

    def test_get_open_restaurants(self):
        current_time = datetime.now().time()
        open_restaurants_count = sum(
            restaurant.start_time <= current_time <= restaurant.end_time
            for restaurant in Restaurant.objects.all()
        )
        response = self.client.get(reverse('restaurant_list'), {'is_open': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), open_restaurants_count)

    def test_get_closed_restaurants(self):
        current_time = datetime.now().time()
        closed_restaurants_count = sum(
            not (restaurant.start_time <= current_time <= restaurant.end_time)
            for restaurant in Restaurant.objects.all()
        )
        response = self.client.get(reverse('restaurant_list'), {'is_open': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), closed_restaurants_count)
    
        # Add assertions for the number of closed restaurants

    

    def test_unsupported_http_method(self):
        response = self.client.post(reverse('restaurant_list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

   

    def test_non_existent_endpoint(self):
        response = self.client.get('/non_existent_endpoint')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        # Delete objects created during the test setup
        Restaurant.objects.all().delete()
       
    # def test_unauthorized_access(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'INVALID_TOKEN')
    #     response = self.client.get(reverse('restaurant_list'))
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




     # def test_authentication(self):
    #     # Assuming the API requires authentication
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'YOUR_TOKEN')  # Replace 'YOUR_TOKEN' with the actual token
    #     response = self.client.get(reverse('restaurant_list'))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_and_retrieve_restaurant(self):
    #     response = self.client.get(reverse('restaurant_list', kwargs={'pk': self.restaurant1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['name'], self.restaurant1.name)

    # def test_update_restaurant(self):
    #     new_name = 'Updated Restaurant'
    #     response = self.client.patch(reverse('restaurant_list', kwargs={'pk': self.restaurant1.id}), {'name': new_name})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], new_name)

    # def test_delete_restaurant(self):
    #     response = self.client.delete(reverse('restaurant_list', kwargs={'pk': self.restaurant1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_get_restaurant_by_id(self):
    #     response = self.client.get(reverse('restaurant_list', kwargs={'id': self.restaurant1.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], 'Restaurant 1')

    # def test_get_restaurant_by_invalid_id(self):
    #     response = self.client.get(reverse('restaurant_list', kwargs={'id': 999}))
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


     # def test_invalid_data_type(self):
    #     response = self.client.get(reverse('restaurant_list', kwargs={'id': 'invalid'}))
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)







