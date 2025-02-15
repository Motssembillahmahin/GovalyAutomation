import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export const fetchOrders = async (searchQuery = "") => {
  try {
    const response = await axios.get(`${API_BASE_URL}/orders?search=${searchQuery}`);
    return response.data.orders;
  } catch (error) {
    console.error("Error fetching orders:", error);
    return [];
  }
};

export const updateOrder = async (orderId, address, phone) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/update-order/${orderId}`, null, {
      params: { address, phone },
    });

    if (response.status === 200) {
      console.log(`✅ Order ${orderId} updated successfully!`);
    }
  } catch (error) {
    console.error("Error updating order:", error);
  }
};
