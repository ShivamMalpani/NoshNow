Feature: Item management
  Scenario: Add an item to a restaurant
    Given a user with ID "1" owns a restaurant
    When the user adds an item with name "Pizza" and price "10.99"
    Then the item should be added successfully