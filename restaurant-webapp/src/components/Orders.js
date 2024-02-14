import React, { useState } from 'react';
import './Orders.css'; // Import the CSS file for styling

const Order = () => {
    // Hardcoded dummy data for active orders
    const hardcodedData = [
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Pending', PaymentStatus: 'Paid', CreatedAt: '2024-02-09' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'Processing', PaymentStatus: 'Pending', CreatedAt: '2024-02-08' },
        { OrderID: 3, CustomerID: 103, Address: '789 Oak St', Status: 'Delivered', PaymentStatus: 'Paid', CreatedAt: '2024-02-07' },
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Pending', PaymentStatus: 'Paid', CreatedAt: '2024-02-09' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'Processing', PaymentStatus: 'Pending', CreatedAt: '2024-02-08' },
        { OrderID: 3, CustomerID: 103, Address: '789 Oak St', Status: 'Delivered', PaymentStatus: 'Paid', CreatedAt: '2024-02-07' },
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Pending', PaymentStatus: 'Paid', CreatedAt: '2024-02-09' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'Processing', PaymentStatus: 'Pending', CreatedAt: '2024-02-08' },
        { OrderID: 3, CustomerID: 103, Address: '789 Oak St', Status: 'Delivered', PaymentStatus: 'Paid', CreatedAt: '2024-02-07' },
        
    ];

    // State to store active orders
    const [activeOrders] = useState(hardcodedData);

    // Function to freeze an order
    const freezeOrder = (orderID) => {
        console.log(`Freezing order ${orderID}`);
        // Implement freeze order logic
    };

    // Function to cancel an order
    const cancelOrder = (orderID) => {
        console.log(`Cancelling order ${orderID}`);
        // Implement cancel order logic
    };

    // Function to scroll to a specific order
    const scrollToOrder = (orderID) => {
        const orderElement = document.getElementById(`order-${orderID}`);
        if (orderElement) {
            orderElement.scrollIntoView({ behavior: 'smooth' });
        }
    };

    return (
        <div className="order-container active-orders">
            <h2>Active Orders</h2>
            <div className="scrollable-list">
                {activeOrders.map(order => (
                    <div key={order.OrderID} id={`order-${order.OrderID}`} className="order-details">
                        <p>Order ID: {order.OrderID}</p>
                        <p>Customer ID: {order.CustomerID}</p>
                        <p>Address: {order.Address}</p>
                        <p>Status: {order.Status}</p>
                        <p>Payment Status: {order.PaymentStatus}</p>
                        <p>Created At: {order.CreatedAt}</p>
                        <button className='freezeButton' onClick={() => freezeOrder(order.OrderID)}>Freeze</button>
                        <button className='freezeButton' onClick={() => cancelOrder(order.OrderID)}>Cancel</button>
                    </div>
                ))}
            </div>
            <div className="scroll-to-order-buttons">
                {activeOrders.map(order => (
                    <button key={order.OrderID} onClick={() => scrollToOrder(order.OrderID)}>Scroll to Order {order.OrderID}</button>
                ))}
            </div>
        </div>
    );
};

export default Order;
