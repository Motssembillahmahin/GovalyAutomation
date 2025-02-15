import React, { useEffect, useState } from "react";
import { fetchOrders } from "./api";
import SearchBar from "./components/SearchBar";
import OrderTable from "./components/OrderTable";

function App() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async (query = "") => {
    const data = await fetchOrders(query);
    setOrders(data);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>📦 GovalyAutomation Order Management</h1>
      <SearchBar onSearch={loadOrders} />
      <OrderTable orders={orders} refreshOrders={() => loadOrders()} />
    </div>
  );
}

export default App;
