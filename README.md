# This document contains documentation of APIs


# Restaurant Management API

This document provides details on the API endpoints available for managing restaurant items, including adding, updating, and removing items, as well as viewing and updating item details such as status and quantity.

## Add Item


**POST** `/add-item`

- **Request JSON**:
  ```json
  {
    "userID": "user_id",
    "name": "item_name",
    "price": "item_price",
    "description": "item_description"
    // other item details
  }
  ```
- **Condition**: If the restaurant is not found for the given `userID`.
  - **Response**: 
    ```json
    {
      "status": 404,
      "error": "Restaurant not found for the given user ID"
    }
    ```
- **Success Response**:
  - **Response**:
    ```json
    {
      "status": 201,
      "data": {
        // item details
      }
    }
    ```

## Update Item

**POST** `/update-item`

- **Request JSON**:
  ```json
  {
    "userID": "user_id",
    "itemID": "item_id",
    // updated item details
  }
  ```
- **Condition**: If the restaurant or item is not found, or if the restaurant ID does not match the item's restaurant ID.
  - **Response**: 
    ```json
    {
      "status": 404 or 403,
      "error": "Appropriate error message"
    }
    ```
- **Success Response**:
  - **Response**:
    ```json
    {
      "status": 200,
      "data": {
        // updated item details
      }
    }
    ```

## Remove Item

**POST** `/remove-item`

- **Request JSON**:
  ```json
  {
    "userID": "user_id",
    "itemID": "item_id"
  }
  ```
- **Condition**: If the restaurant or item is not found, or if the restaurant ID does not match the item's restaurant ID.
  - **Response**: 
    ```json
    {
      "status": 404 or 403,
      "error": "Appropriate error message"
    }
    ```
- **Success Response**:
  - **Response**:
    ```json
    {
      "status": 200,
      "message": "Item removed successfully"
    }
    ```

## View Item

**GET** `/view-item/{id}`

- **Path Variable**: `id` of the item to view.
- **Condition**: If the item is not found.
  - **Response**: 
    ```json
    {
      "status": 404,
      "error": "Item not found for the given item ID"
    }
    ```
- **Success Response**:
  - **Response**:
    ```json
    {
      "status": 200,
      "data": {
        // item details
      }
    }
    ```

## Update Item Status

**POST** `/update-item-status`

- **Request JSON**:
  ```json
  {
    "userID": "user_id",
    "itemID": "item_id",
    "available": true or false
  }
  ```
- **Condition**: If the restaurant or item is not found, or if the restaurant ID does not match the item's restaurant ID.
  - **Response**: 
    ```json
    {
      "status": 404 or 403,
      "error": "Appropriate error message"
    }
    ```
- **Success Response**:
  - **Response**:
    ```json
    {
      "status": 200,
      "data": {
        // updated item status
      }
    }
    ```

## Update Item Quantity

**POST** `/update-item-quantity`

- **Request JSON**:
  ```json
  {
    "userID": "user_id",
    "itemID": "item_id",
    "quantity": "new_quantity"
  }
  ```
- **Condition**: If the restaurant or item is not found, or if the restaurant ID does not match the item's restaurant ID.
  - **Response**: 
    ```json
    {
      "status": 404 or 403,
      "error": "Appropriate error message"
    }
    ```
- **Success Response**:
  - **Response**:
    ```json
    {
      "status": 200,
      "data": {
        // updated item quantity
      }
    }
    ```
```




```
# Restaurant Management API

This document provides details on the API endpoints available for managing restaurant items, viewing restaurants, handling user carts, and managing feedback.

## Restaurant List

**GET** `/restaurant-list`

- **Query Parameters**: `is_open` (optional) to filter restaurants by their open status.
- **Response**:
  - **Status**: 200
  - **JSON**: List of restaurants serialized using `RestaurantListSerializer`.

## Item List

**GET** `/item-list/{restaurant_id}`

- **Path Variable**: `restaurant_id` to specify which restaurant's items to list.
- **Condition**: If the restaurant is not found.
  - **Response**:
    ```json
    {
      "status": 404,
      "error": "Restaurant not found"
    }
    ```
- **Success Response**:
  - **Status**: 200
  - **JSON**: List of items serialized using `ItemSerializer`.

## View Restaurant

**GET** `/view-restaurant/{restaurant_id}`

- **Path Variable**: `restaurant_id` to view a specific restaurant.
- **Condition**: If the restaurant is not found.
  - **Response**:
    ```json
    {
      "status": 404,
      "error": "Restaurant not found"
    }
    ```
- **Success Response**:
  - **Status**: 200
  - **JSON**: Restaurant details including owner and feedback list.

## Add to Cart

**POST** `/add-cart`

- **Request JSON**:
  ```json
  {
    "userID": "user_id",
    "item_id": "item_id",
    "quantity": quantity
  }
  ```
- **Conditions**:
  - If required fields are missing:
    - **Response**:
      ```json
      {
        "status": 400,
        "error": "Missing required fields"
      }
      ```
  - If the item is not found:
    - **Response**:
      ```json
      {
        "status": 404,
        "error": "Item not found"
      }
      ```
  - If the item is from a different restaurant than the one in the cart:
    - **Response**:
      ```json
      {
        "status": 400,
        "error": "Wrong Restaurant"
      }
      ```
  - If the quantity is negative:
    - **Response**:
      ```json
      {
        "status": 400,
        "error": "Quantity should not be negative"
      }
      ```
- **Success Response**:
  - **Status**: 200
  - **Message**: "Success"

## Clear Cart

**POST** `/clear-cart`

- **Request JSON**:
  ```json
  {
    "userID": "user_id"
  }
  ```
- **Response**:
  - **Status**: 200
  - **Message**: "success"

## View Cart

**GET** `/view-cart/{userID}`

- **Path Variable**: `userID` to view the user's cart.
- **Condition**: If the cart is empty.
  - **Response**:
    ```json
    {
      "status": 200,
      "message": "Cart is Empty"
    }
    ```
- **Success Response**:
  - **Status**: 200
  - **JSON**: Cart details including item list and total amount.
```






```
# Order and Payment Management API

This document outlines the API endpoints for managing orders and payments within a restaurant management system. It includes endpoints for viewing active orders, order history, freezing orders, viewing payment history, and viewing wallet details.

## Active Order List

**GET** `/active-order-list`

- **Query Parameters**: `restaurantID` to filter orders by restaurant.
- **Response**:
  - **Status**: 200 OK
  - **JSON**: List of active orders serialized using `OrderSerializer`.

## Order History

**GET** `/order-history`

- **Query Parameters**: `restaurantID` to filter orders by restaurant.
- **Response**:
  - **Status**: 200 OK
  - **JSON**: List of all orders for the specified restaurant serialized using `OrderHistorySerializer`.

## Freeze Order

**POST** `/freeze-order`

- **Request JSON**:
  ```json
  {
    "OrderID": "order_id",
    "RestaurantID": "restaurant_id",
    "freeze": true or false
  }
  ```
- **Response**:
  - **Status**: 200 OK or 404 Not Found (if order does not exist)
  - **JSON**:
    ```json
    {
      "message": "Success"
    }
    ```

## Payment History

**GET** `/payment-history`

- **Query Parameters**: `user_id` to filter payment history by user.
- **Response**:
  - **Status**: 200 OK
  - **JSON**: List of payment history records serialized using `PaymentHistorySerializer`.

## View Wallet

**GET** `/view-wallet`

- **Query Parameters**: `user_id` to view wallet details for a specific user.
- **Response**:
  - **Status**: 200 OK
  - **JSON**: Wallet details serialized using `ViewWalletSerializer`.

This API documentation provides a comprehensive guide for developers to interact with the order and payment management functionalities of the restaurant management system, including viewing active orders, freezing orders, viewing order and payment history, and accessing wallet details.
```



```
# Order and Payment Management API

This document provides details on the API endpoints available for creating and managing orders, as well as handling payment histories within a restaurant management system.

## Create Order

**POST** `/create-order`

- **Request JSON**:
  ```json
  {
    "userID": "user_id",
    "paymentType": "payment_type",
    "orderType": "order_type",
    "Address": "delivery_address" // Optional based on order type
  }
  ```
- **Response**:
  - **Status**: 200 OK, 400 Bad Request, or 404 Not Found
  - **JSON**:
    ```json
    {
      "message": "Order created successfully"
    }
    ```

## Cancel Order

**POST** `/cancel-order`

- **Request JSON**:
  ```json
  {
    "userID": "user_id",
    "orderID": "order_id"
  }
  ```
- **Response**:
  - **Status**: 200 OK, 400 Bad Request, 403 Forbidden, or 404 Not Found
  - **JSON**:
    ```json
    {
      "message": "Order cancelled"
    }
    ```

## Student Order History

**GET** `/student-order-history/{userID}`

- **Path Variable**: `userID` to filter orders by customer.
- **Response**:
  - **Status**: 200 OK
  - **JSON**: List of orders serialized using `OrderHistorySerializer`.

## View Order

**GET** `/view-order/{orderID}/{userID}`

- **Path Variables**: `orderID` to specify the order and `userID` to verify the customer.
- **Response**:
  - **Status**: 200 OK, 403 Forbidden, or 404 Not Found
  - **JSON**:
    ```json
    {
      "order": {
        // Order details
      },
      "items": [
        {
          "id": "item_id",
          "name": "item_name",
          "quantity": quantity,
          "amount": amount
        }
      ],
      "transactions": [
        {
          // Transaction details
        }
      ]
    }
    ```


