import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom'; // Import useNavigate and useParams
import './schooldata.css';

const SchoolData = () => {
  const navigate = useNavigate();
  const { id } = useParams(); // Retrieve 'id' from the URL (for the expanded view)
  const [zoom, setZoom] = useState(1);
  const [expandedCard, setExpandedCard] = useState(null); // Track which card is expanded
  const [searchQuery, setSearchQuery] = useState(""); // State to handle search input

  // Zoom functionality
  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.1, 2));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.1, 0.5));

  // Handle card click to expand
  const handleCardClick = (id) => {
    setExpandedCard(id); // Set expanded card ID
  };

  // Handle Exit - navigate back to the School Data main page
  const handleExit = () => {
    setExpandedCard(null); // Close the expanded card
    navigate('/school-data'); // Navigate to the main page (always to /school-data)
  };

  // Handle search input change
  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value); // Update search query state
  };

  return (
    <div className="school-data-container">
      <header className="school-header">
        <h1>School Data</h1>

        {/* Search Bar */}
        <input
          type="text"
          className="search-input"
          value={searchQuery}
          onChange={handleSearchChange} // Handle search input change
          placeholder="Search..."
        />
        
        {/* Filter Dropdown */}
        <select className="filter-dropdown">
          <option>Compare by Region</option>
          <option>Compare by Year</option>
          <option>Compare by Enrollment</option>
        </select>
      </header>

      {/* Cards container */}
      <div className="cards-wrapper" style={{ transform: `scale(${zoom})` }}>
        {["container1", "container2", "container3", "container4"].map((id, index) => (
          <div
            key={id}
            className={`school-card ${expandedCard === id ? 'expanded' : ''}`}
            onClick={() => handleCardClick(id)} // Pass unique ID to expand
          >
            {/* Labeling each container with different text */}
            <label>
              {index === 0 && "School Distribution by Sector per region"}
              {index === 1 && "School Distribution by Sub-classification per Region"}
              {index === 2 && "School Distribution by Modified COC per Region"}
              {index === 3 && "School Distribution by District per Region"}
            </label>
          </div>
        ))}
      </div>

      {/* Sidebar Settings, shown when a card is expanded */}
      {expandedCard && (
        <aside className="school-sidebar">
          <button onClick={handleExit}>Exit</button> {/* Click Exit to go back to /school-data */}
          <button onClick={handleZoomIn}>Zoom In</button>
          <button onClick={handleZoomOut}>Zoom Out</button>
          <button onClick={() => alert('Exported successfully!')}>Export</button>
          <button onClick={() => alert('File added!')}>Add File</button>
        </aside>
      )}
    </div>
  );
};

export default SchoolData;
