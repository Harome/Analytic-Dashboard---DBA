import React, { useState, useEffect } from 'react';
import './schooldata.css';

const SchoolData = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);

  const handleSearchChange = (e) => setSearchQuery(e.target.value);

  const handleZoomIn = () => setZoomLevel((prev) => Math.min(prev + 0.1, 2));
  const handleZoomOut = () => setZoomLevel((prev) => Math.max(prev - 0.1, 0.5));

  const handleImport = () => alert("Import function not implemented yet.");
  const handleExport = () => alert("Export function not implemented yet.");

  useEffect(() => {
    document.documentElement.style.setProperty('--zoom', zoomLevel);
  }, [zoomLevel]);

  const cardsData = [
    { label: "School Distribution by Sector per region", src: "http://localhost:8050/graph10" },
    { label: "School Distribution by Sub-classification per Region", src: "http://localhost:8050/graph11" }
  ];

  const filteredCards = cardsData.filter(card =>
    card.label.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="school-data-container">
      <header className="school-header">
        <h1>School Data</h1>
        <input
          type="text"
          className="search-int"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Search..."
        />
      </header>
      
      <div className="import-export-sc">
        <button onClick={handleImport}>Import</button>
        <button onClick={handleExport}>Export</button>
      </div>

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
            <iframe
              src={card.src}
              title={card.label}
              style={{
                width: '100%',
                height: '550px',
                border: '1px solid #ccc',
                borderRadius: '8px',
                marginTop: '10px',
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
                  border: 'none'
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

export default SchoolData;