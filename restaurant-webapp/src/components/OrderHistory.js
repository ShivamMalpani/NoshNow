import React from 'react';
import './OrderHistory.css'; // Import the CSS file for styling

const OrderHistory = () => {
    // Hardcoded dummy data for order history
    const hardcodedData = [
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'John Doe', CreatedAt: '2024-02-09', DeliveredAt: '2024-02-10' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'On Delivery', PaymentStatus: 'Pending', DeliveredBy: 'Jane Doe', CreatedAt: '2024-02-08', DeliveredAt: '' },
        { OrderID: 3, CustomerID: 103, Address: '789 Oak St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'Sam Smith', CreatedAt: '2024-02-07', DeliveredAt: '2024-02-09' },
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'John Doe', CreatedAt: '2024-02-09', DeliveredAt: '2024-02-10' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'On Delivery', PaymentStatus: 'Pending', DeliveredBy: 'Jane Doe', CreatedAt: '2024-02-08', DeliveredAt: '' },
        { OrderID: 3, CustomerID: 103, Address: '789 Oak St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'Sam Smith', CreatedAt: '2024-02-07', DeliveredAt: '2024-02-09' },
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'John Doe', CreatedAt: '2024-02-09', DeliveredAt: '2024-02-10' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'On Delivery', PaymentStatus: 'Pending', DeliveredBy: 'Jane Doe', CreatedAt: '2024-02-08', DeliveredAt: '' },
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'John Doe', CreatedAt: '2024-02-09', DeliveredAt: '2024-02-10' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'On Delivery', PaymentStatus: 'Pending', DeliveredBy: 'Jane Doe', CreatedAt: '2024-02-08', DeliveredAt: '' },
        { OrderID: 3, CustomerID: 103, Address: '789 Oak St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'Sam Smith', CreatedAt: '2024-02-07', DeliveredAt: '2024-02-09' },
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'John Doe', CreatedAt: '2024-02-09', DeliveredAt: '2024-02-10' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'On Delivery', PaymentStatus: 'Pending', DeliveredBy: 'Jane Doe', CreatedAt: '2024-02-08', DeliveredAt: '' },
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'John Doe', CreatedAt: '2024-02-09', DeliveredAt: '2024-02-10' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'On Delivery', PaymentStatus: 'Pending', DeliveredBy: 'Jane Doe', CreatedAt: '2024-02-08', DeliveredAt: '' },
        { OrderID: 3, CustomerID: 103, Address: '789 Oak St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'Sam Smith', CreatedAt: '2024-02-07', DeliveredAt: '2024-02-09' },
        { OrderID: 1, CustomerID: 101, Address: '123 Main St', Status: 'Delivered', PaymentStatus: 'Paid', DeliveredBy: 'John Doe', CreatedAt: '2024-02-09', DeliveredAt: '2024-02-10' },
        { OrderID: 2, CustomerID: 102, Address: '456 Elm St', Status: 'On Delivery', PaymentStatus: 'Pending', DeliveredBy: 'Jane Doe', CreatedAt: '2024-02-08', DeliveredAt: '' },
    ];

    return (
        <div className="order-history-container">
            <h2 className="order-history-heading">Order History</h2>
            <div className="order-history-list">
                {hardcodedData.map(order => (
                    <div key={order.OrderID} className="order-history-item">
                        <p className="order-id">Order ID: {order.OrderID}</p>
                        <p className="customer-id">Customer ID: {order.CustomerID}</p>
                        <p className="address">Address: {order.Address}</p>
                        <div className="status-section">
                            <p>Status: <span className={`status ${order.Status === 'Delivered' ? 'delivered' : 'on-delivery'}`}>{order.Status}</span></p>
                            <p>Payment Status: <span className={`payment-status ${order.PaymentStatus === 'Paid' ? 'paid' : 'pending'}`}>{order.PaymentStatus}</span></p>
                        </div>
                        <p className="delivered-by">Delivered By: {order.DeliveredBy}</p>
                        <p className="created-at">Created At: {order.CreatedAt}</p>
                        <p className="delivered-at">Delivered At: {order.DeliveredAt || 'Not delivered yet'}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default OrderHistory;
