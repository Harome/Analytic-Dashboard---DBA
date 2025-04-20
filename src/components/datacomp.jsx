import React, { useState } from 'react';
import './datacomp.css';

const DataComp = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [category, setCategory] = useState("");
  const [region, setRegion] = useState("");

  const handleSearchChange = (e) => setSearchQuery(e.target.value);
  const handleCategoryChange = (e) => setCategory(e.target.value);
  const handleRegionChange = (e) => setRegion(e.target.value);

  return (
    <div className="datacomp-container">
      <header className="school-header">
        <h1>Data Comparison</h1>
      </header>

      <div className="search-bar-container">
        <input
          type="text"
          className="search-input-datacomp"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Search..."
        />
      </div>

      <div className="dropdowns-row">
        <select className="dropdown left-dropdown" value={category} onChange={handleCategoryChange}>
          <option value="">Select Category</option>
          <option value="elementary">Elementary</option>
          <option value="highschool">High School</option>
          <option value="college">College</option>
        </select>

        <select className="dropdown right-dropdown" value={region} onChange={handleRegionChange}>
          <option value="">Select Region</option>
          <option value="ncr">NCR</option>
          <option value="region-iv">Region IV-A</option>
          <option value="region-vii">Region VII</option>
        </select>
      </div>
    </div>
  );
};

export default DataComp;
