import React from "react";
import UpdateOrder from "./UpdateOrder";

const OrderTable = ({ orders, refreshOrders }) => {
  return (
    <table border="1" width="100%" cellPadding="8">
      <thead>
        <tr>
          <th>Order ID</th>
          <th>Order Name</th>
          <th>Customer ID</th>
          <th>Total Amount</th>
          <th>Fulfillment Status</th>
          <th>Address</th>
          <th>Phone</th>
          <th>Update</th>
        </tr>
      </thead>
      <tbody>
        {orders.length > 0 ? (
          orders.map((order) => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.order_name || "N/A"}</td>
              <td>{order.customer_id}</td>
              <td>{order.total_amount} BDT</td>
              <td>{order.fulfillment_status || "Pending"}</td>
              <td>
                <input type="text" defaultValue={order.address} id={`address-${order.id}`} />
              </td>
              <td>
                <input type="text" defaultValue={order.phone} id={`phone-${order.id}`} />
              </td>
              <td>
                <UpdateOrder orderId={order.id} refreshOrders={refreshOrders} />
              </td>
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan="8" style={{ textAlign: "center" }}>No orders found</td>
          </tr>
        )}
      </tbody>
    </table>
  );
};

export default OrderTable;
