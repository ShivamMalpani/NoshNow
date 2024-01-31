# from django.test import TestCase, Client
# import pymongo
# from django.urls import reverse
# from rest_framework import status
# from ..models import Restaurant, UserMod
# from ..serializers import OwnerSerializer


# class ViewRestaurantViewTestCase(TestCase):
#     def setUp(self):
#         # Create test data for SQLite
#         self.owner = UserMod.objects.create(
#             first_name="John",
#             last_name="Doe",
#             mobile_no="1234567890",
#             email="john.doe@example.com",
#             profile_pic="https://example.com/profile.jpg",
#             amount=100
#         )
#         self.restaurant = Restaurant.objects.create(
#             name="Test Restaurant",
#             address="123 Main St",
#             owner_id=self.owner.UserID
#         )

#         # Create a MongoDB connection
#         client = pymongo.MongoClient('x')
#         # Select your MongoDB database
#         mydb = client['Feedback']

#         # Create test data for MongoDB collection 'Feedback'
#         self.feedback_data = {
#             "_id": str(self.restaurant.id),
#             "feedback_list": {
#                 str(self.owner.UserID): "Great restaurant!"
#             }
#         }
#         mydb["Feedback"].insert_one(self.feedback_data)

#         # Set up a client for making requests
#         self.client = Client()

#     def test_view_restaurant_success(self):
#         url = reverse('view_restaurant', args=[self.restaurant.id])
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertContains(response, "owner")
#         self.assertContains(response, "feedback_list")
#         self.assertEqual(response.data["owner"]["first_name"], self.owner.first_name)
#         # Add more assertions based on your expected response structure

#     def test_view_restaurant_not_found(self):
#         url = reverse('view_restaurant', args=[999])  # Non-existing restaurant ID
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertContains(response, "error")

#     def test_view_restaurant_invalid_id(self):
#         url = reverse('view_restaurant', args=['invalid_id'])  # Invalid restaurant ID
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertContains(response, "error")

#     def test_view_restaurant_empty_feedback(self):
#         # Remove feedback for the test
#         self.feedback_entry.feedback_list = {}
#         self.feedback_entry.save()

#         url = reverse('view_restaurant', args=[self.restaurant.id])
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertContains(response, "owner")
#         self.assertContains(response, "feedback_list")
#         self.assertEqual(len(response.data["feedback_list"]), 0)

#     def test_view_restaurant_multiple_feedback(self):
#         # Add multiple feedback entries for the test
#         user2 = UserMod.objects.create(
#             first_name="Jane",
#             last_name="Doe",
#             mobile_no="9876543210",
#             email="jane.doe@example.com",
#             profile_pic="https://example.com/jane.jpg",
#             amount=50
#         )
#         self.feedback_entry.feedback_list[str(user2.UserID)] = "Another great review!"
#         self.feedback_entry.save()

#         url = reverse('view_restaurant', args=[self.restaurant.id])
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertContains(response, "owner")
#         self.assertContains(response, "feedback_list")
#         self.assertEqual(len(response.data["feedback_list"]), 2)

    # Additional test cases can be added based on your specific requirements

# Adjust the reverse('view_restaurant') according to your actual URL configuration in urls.py
