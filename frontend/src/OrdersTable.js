import React, { useState } from "react";

const OrdersTable = ({ orders, setOrders }) => {
    const updateOrder = async (orderId, newAddress, newPhone) => {
        try {
            const response = await fetch(`http://localhost:8000/update-order/${orderId}?address=${newAddress}&phone=${newPhone}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" }
            });

            if (response.ok) {
                setOrders(orders.map(order =>
                    order.id === orderId ? { ...order, address: newAddress, phone: newPhone } : order
                ));
                alert(`Order ${orderId} updated successfully!`);
            } else {
                alert(`Error updating order ${orderId}`);
            }
        } catch (error) {
            console.error("Error updating order:", error);
        }
    };

    return (
        <table border="1">
            <thead>
                <tr>
                    <th>Order ID</th>
                    <th>Address</th>
                    <th>Phone</th>
                    <th>Update</th>
                </tr>
            </thead>
            <tbody>
                {orders.map(order => (
                    <tr key={order.id}>
                        <td>{order.id}</td>
                        <td><input type="text" defaultValue={order.address} id={`address_${order.id}`} /></td>
                        <td><input type="text" defaultValue={order.phone} id={`phone_${order.id}`} /></td>
                        <td><button onClick={() => updateOrder(order.id, document.getElementById(`address_${order.id}`).value, document.getElementById(`phone_${order.id}`).value)}>🔄 Update</button></td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default OrdersTable;
