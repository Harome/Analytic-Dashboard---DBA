import React, { useState, useEffect } from 'react';
import './studentdata.css';

const StudentData = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleZoomIn = () => {
    setZoomLevel((prev) => Math.min(prev + 0.1, 2));
  };

  const handleZoomOut = () => {
    setZoomLevel((prev) => Math.max(prev - 0.1, 0.5));
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
    { label: "Regional Population Trends", src: "http://localhost:8050/graph7" },
    { label: "Enrollment Insights", src: "http://localhost:8050/graph8" },
    { label: "Student Population Patterns", src: "http://localhost:8050/graph9" },
  ];

  return (
    <div className="student-data-container">
      <header className="student-header">
        <h1>Student Data</h1>
        <input
          type="text"
          className="search-input-student-data"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Search..."
        />
      </header>

      <div className="import-export-top">
        <button onClick={handleImport}>Import</button>
        <button onClick={handleExport}>Export</button>
      </div>
      
      <div className="cards-wrapper">
        {cardsData.map((card, index) => (
          <div
            key={index}
            className="student-card"
            onClick={() => {
              setSelectedCard(card);
              setZoomLevel(1);
            }}
          >
            <label>{card.label}</label>
            <iframe
              src={card.src}
              title={card.label}
              style={{
                width: '100%',
                height: '550px',
                border: '1px solid #ccc',
                borderRadius: '8px',
                marginTop: '10px'
              }}
            />
          </div>
        ))}
      </div>

      {/* Modal */}
      {selectedCard && (
        <div className="modal-overlay" onClick={() => setSelectedCard(null)}>
          <div className="modal-card expanded-modal" onClick={(e) => e.stopPropagation()}>
            <div
              className="modal-content"
              style={{
                transform: `scale(${zoomLevel})`,
                width: `${100 / zoomLevel}%`,
                height: `${100 / zoomLevel}%`
              }}
            >
              <h2>{selectedCard.label}</h2>
              <iframe
                src={selectedCard.src}
                title={selectedCard.label}
                style={{
                  width: '100%',
                  height: '100%',
                  border: 'none',
                  borderRadius: '8px'
                }}
              />
            </div>
          </div>

          <div className="side-settings-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-exit" onClick={() => setSelectedCard(null)}>Exit</button>
            <div className="zoom-controls">
              <button onClick={handleZoomOut}>Zoom Out</button>
              <button onClick={handleZoomIn}>Zoom In</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentData;
