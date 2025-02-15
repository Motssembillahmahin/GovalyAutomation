import React, { useState } from "react";
import { updateOrder } from "../api";

const UpdateOrder = ({ orderId, refreshOrders }) => {
  const [loading, setLoading] = useState(false);

  const handleUpdate = async () => {
    const newAddress = document.getElementById(`address-${orderId}`).value;
    const newPhone = document.getElementById(`phone-${orderId}`).value;

    if (!newAddress || !newPhone) {
      alert("Address and Phone cannot be empty!");
      return;
    }

    setLoading(true);
    await updateOrder(orderId, newAddress, newPhone);
    setLoading(false);

    refreshOrders(); // 🔥 Refresh Order Table After Update
  };

  return (
    <button 
      onClick={handleUpdate} 
      style={{
        background: "#4CAF50", 
        color: "white", 
        padding: "5px 10px",
        cursor: loading ? "not-allowed" : "pointer",
        opacity: loading ? 0.5 : 1
      }}
      disabled={loading}
    >
      {loading ? "Updating..." : "✅ Save"}
    </button>
  );
};

export default UpdateOrder;
