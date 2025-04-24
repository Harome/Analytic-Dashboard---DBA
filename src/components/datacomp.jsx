import React, { useState } from 'react';
import './datacomp.css';

const DataComp = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [category, setCategory] = useState("");
  const [region, setRegion] = useState(""); // State for region selection

  const handleCategoryChange = (e) => {
    setCategory(e.target.value);
    // Reset region when category changes
    setRegion("");
  };
  const handleRegionChange = (e) => setRegion(e.target.value);

  // Function to get the iframe source based on category and region
  const getIframeSrc = (selectedCategory, selectedRegion) => {
    if (selectedCategory === "gender") {
      // Pass region as a query parameter to the gender comparison route in app.py
      return `http://localhost:8050/data-comparison-gender?region=${selectedRegion || 'All Regions'}`;
    } else if (selectedCategory === "grade-level") {
      // Pass region as a query parameter to the grade level comparison route in app.py
      return `http://localhost:8050/data-comparison-grade?region=${selectedRegion || 'All Regions'}`;
    }
    return ""; // Default empty source if no category is selected
  };

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
            {/* Add other categories as needed */}
            {/* <option value="grade-division">Grade Division</option> */}
            {/* <option value="sector">Sector</option> */}
            {/* <option value="school-type">School Type</option> */}
          </select>
        </div>

        <div className="datacomp-wrapper">
          <div className="container-with-sticker">
            <div className="container-icon">1</div>
            <div className="left-container">
              {/* Display iframe only when a category is selected */}
              {category && (
                <iframe
                  src={getIframeSrc(category, region)}
                  title={`Dash Data Comparison ${category}`}
                  width="100%"
                  height="400px"
                  style={{ border: 'none' }}
                />
              )}
            </div>
          </div>

          <div className="container-with-sticker">
            <div className="container-icon">2</div>
            <div className="right-container">
               {category && (
                <iframe
                  src={getIframeSrc(category, region)} // Or a different source for comparison
                  title={`Dash Data Comparison ${category} 2`}
                  width="100%"
                  height="400px"
                  style={{ border: 'none' }}
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DataComp;