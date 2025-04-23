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
      <header className="datacomp-header">
        <h1>Data Comparison</h1>
      </header>

      <div className="outer-container">
        <div className="dropdowns-row">
          <select className="dropdown left-dropdown" value={category} onChange={handleCategoryChange}>
            <option value="">Select Category</option>
            <option value="gender">Gender</option>
            <option value="grade-level">Grade Level</option>
            <option value="grade-division">Grade Division</option>
            <option value="sector">Sector</option>
            <option value="school-type">School Type</option>
          </select>
        </div>

        <div className="datacomp-wrapper">
          <div className="container-with-sticker">
            <div className="container-icon">1</div>
            <div className="left-container">
              {/* Left content */}
            </div>
          </div>

          <div className="container-with-sticker">
            <div className="container-icon">2</div>
            <div className="right-container">
              {/* Right content */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DataComp;
