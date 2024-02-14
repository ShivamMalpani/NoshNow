from behave import given, when, then
from rest_framework.test import APIClient
from nosh.models import Restaurant, Item
import os
from django.conf import settings
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
client = APIClient()

@given('a user with ID "{user_id}" owns a restaurant')
def step_impl(context, user_id):
    # Assuming a Restaurant model with an owner_id field
    Restaurant.objects.create(name="Test Restaurant", owner_id=user_id)

@when('the user adds an item with name "{name}" and price "{price}"')
def step_impl(context, name, price):
    data = {"userID": "1", "name": name, "price": price}
    context.response = client.post('http://127.0.0.1:8000/api/catalogue/restaurant/add_item', data)

@then('the item should be added successfully')
def step_impl(context):
    assert context.response.status_code == 201
    # Additional assertions can be added to verify the response content
