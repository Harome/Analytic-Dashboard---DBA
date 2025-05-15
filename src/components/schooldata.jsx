import React, { useState, useEffect } from 'react';
import './schooldata.css';

const SchoolCard = ({ label, src, onClick }) => (
  <div className="school-card" onClick={onClick}>
    <label>{label}</label>
    <iframe
      src={src}
      title={label}
      className="school-card-iframe"
    />
  </div>
);

const SchoolData = () => {
  const [selectedCard, setSelectedCard] = useState(null);  
  const [zoomLevel, setZoomLevel] = useState(1);  

  const role = localStorage.getItem("role"); 

  useEffect(() => {
    document.documentElement.style.setProperty('--zoom', zoomLevel); 
  }, [zoomLevel]);

  const cardsData = [
    { label: "School Population per Sector, Sub-Classification, and Modified COC", src: "http://localhost:8050/graph10" },
    { label: "School Count by School Type and Sector", src: "http://localhost:8050/graph11" }
  ];

  return (
    <div className="school-data-container">
      <header className="school-header">
        <h1>School Data</h1>
      </header>

      {role === 'admin' && (
        <div className="import-export-sc">
          <a
            href="http://localhost:8050/school_page"
            target="_blank"
            rel="noopener noreferrer"
            className="upload-link-button"
          >
            Import Dataset
          </a>
        </div>
      )}

      <div className="school-cards-wrapper">
        {cardsData.map((card, index) => (
          <SchoolCard
            key={index}
            label={card.label}
            src={card.src}
            onClick={() => {
              setSelectedCard(card);
              setZoomLevel(1);
            }}
          />
        ))}
      </div>

      {selectedCard && (
        <div className="modal-overlay" onClick={() => setSelectedCard(null)}>
          <div className="expanded-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-title">
              <h2>{selectedCard.label}</h2>
            </div>
            <div className="modal-content">
              <iframe
                src={selectedCard.src}
                title={selectedCard.label}
                style={{ width: '100%', height: '100%', border: 'none' }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SchoolData;
