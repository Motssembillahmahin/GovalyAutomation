import React, { useState } from "react";

const SearchBar = ({ onSearch }) => {
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    onSearch(e.target.value);
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <input
        type="text"
        placeholder="Search by Order ID, Customer ID, or Phone"
        value={searchQuery}
        onChange={handleSearch}
        style={{ padding: "8px", width: "300px", marginRight: "10px" }}
      />
    </div>
  );
};

export default SearchBar;
