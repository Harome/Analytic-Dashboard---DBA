import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './studentdata.css';

const StudentData = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [searchQuery, setSearchQuery] = useState("");
  const [filter, setFilter] = useState("Region");
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const handleZoomIn = () => {
    setZoomLevel((prev) => Math.min(prev + 0.1, 2)); // Zoom in
  };

  const handleZoomOut = () => {
    setZoomLevel((prev) => Math.max(prev - 0.1, 0.5)); // Zoom out
  };

  const handleImport = () => {
    alert("Import function not implemented yet.");
  };

  const handleExport = () => {
    alert("Export function not implemented yet.");
  };

  useEffect(() => {
    document.documentElement.style.setProperty('--zoom', zoomLevel);
  }, [zoomLevel]);

  const cardsData = [
    { label: "Regional Population Trends", filterType: "Region" },
    { label: "Enrollment Insights", filterType: "Region" },
    { label: "Student Population Patterns", filterType: "Region" },
    { label: "Education Quality Analysis", filterType: "Region" }
  ];

  const filteredCards = cardsData.filter(card =>
    card.label.toLowerCase().includes(searchQuery.toLowerCase()) &&
    (filter === "Region" || card.filterType === filter)
  );

  return (
    <div className="school-data-container">
      <header className="school-header">
        <h1>Student Data</h1>
        <input
          type="text"
          className="search-input"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Search..."
        />
        <select className="filter-dropdown" onChange={handleFilterChange}>
          <option value="Region">Compare by Region</option>
          <option value="Year">Compare by Year</option>
          <option value="Enrollment">Compare by Enrollment</option>
        </select>
      </header>

      <div className="cards-wrapper">
        {filteredCards.map((card, index) => (
          <div
            key={index}
            className="school-card"
            onClick={() => {
              setSelectedCard(card);
              setZoomLevel(1);
            }}
          >
            <label>{card.label}</label>
          </div>
        ))}
      </div>

      {/* Modal */}
      {selectedCard && (
  <div className="modal-overlay" onClick={() => setSelectedCard(null)}>
    <div className="modal-card expanded-modal" onClick={(e) => e.stopPropagation()}>
      <div className="modal-content"
        style={{
          transform: `scale(${zoomLevel})`,
          width: `${100 / zoomLevel}%`,
          height: `${100 / zoomLevel}%`,
        }}
      >
        <h2>{selectedCard.label}</h2>
        {/* Insert graph or data component here */}
      </div>
    </div>

    {/* Right-side settings modal */}
    <div className="side-settings-modal" onClick={(e) => e.stopPropagation()}>
      <button className="modal-exit" onClick={() => setSelectedCard(null)}>Exit</button>
      <div className="zoom-controls">
        <button onClick={handleZoomOut}>Zoom Out</button>
        <button onClick={handleZoomIn}> Zoom In</button>
      </div>
      <div className="import-export-buttons">
        <button onClick={handleImport}>Import</button>
        <button onClick={handleExport}>Export</button>
      </div>
    </div>
  </div>
)}


    </div>
  );
};

export default StudentData;
