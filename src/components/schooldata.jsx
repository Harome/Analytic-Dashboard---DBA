import React, { useState, useEffect } from 'react';
import './schooldata.css';

const SchoolData = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [refreshKey, setRefreshKey] = useState(Date.now());
  const [role, setRole] = useState('');

  const handleImport = () => setShowUploadModal(true);

  useEffect(() => {
    document.documentElement.style.setProperty('--zoom', zoomLevel);
    const storedRole = localStorage.getItem('role');
    setRole(storedRole);
  }, [zoomLevel]);

  const cardsData = [
    { label: "School Population per Sector, Sub-Classification, and Modified COC", src: "http://localhost:8050/graph10" },
    { label: "School Count by School Type and Sector", src: "http://localhost:8050/graph11" }
  ];

  const handleSubmit = () => {
    setShowUploadModal(false);
    setRefreshKey(Date.now());
    console.log("Submit clicked, closing modal and attempting graph refresh.");
  };

  return (
    <div className="school-data-container">
      <header className="school-header">
        <h1>School Data</h1>
      </header>

      {role !== "user" && (
        <div className="import-export-sc">
          <button onClick={handleImport}>Add New DataSet</button>
        </div>
      )}

      <div className="cards-wrapper">
        {cardsData.map((card, index) => (
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
              src={`${card.src}?t=${refreshKey}`}
              title={card.label}
              style={{
                width: '100%',
                height: '650px',
                border: '1px solid #ccc',
                borderRadius: '8px',
                marginTop: '10px',
              }}
            />
          </div>
        ))}
      </div>

      {selectedCard && (
        <div className="modal-overlay" onClick={() => setSelectedCard(null)}>
          <div className="modal-cards expanded-modal" onClick={(e) => e.stopPropagation()}>
            <div
              className="modal-content"
              style={{
                transform: `scale(${zoomLevel})`,
                width: '100%',
                height: '100%',
              }}
            >
              <h2>{selectedCard.label}</h2>
              <iframe
                src={`${selectedCard.src}?t=${refreshKey}`}
                title={selectedCard.label}
                style={{
                  width: '100%',
                  height: 'calc(100% - 40px)',
                  border: 'none',
                  transform: `scale(${zoomLevel})`,
                  transformOrigin: 'top left'
                }}
              />
              <div style={{
                position: 'absolute',
                bottom: '10px',
                right: '10px',
                background: 'rgba(255,255,255,0.8)',
                padding: '5px',
                borderRadius: '5px'
              }}>
                <button onClick={() => setZoomLevel(prev => Math.max(0.5, prev - 0.1))}>-</button>
                <span style={{ margin: '0 10px' }}>{Math.round(zoomLevel * 100)}%</span>
                <button onClick={() => setZoomLevel(prev => Math.min(3, prev + 0.1))}>+</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {showUploadModal && (
        <div className="upload-modal-overlay-school" onClick={() => setShowUploadModal(false)}>
          <div className="upload-modal-school" onClick={(e) => e.stopPropagation()}>
            <h2>Add New Dataset</h2>
            <p>Upload a CSV or Excel file:</p>
            <iframe
              src="http://localhost:8050/upload_school"
              title="Upload New Dataset"
              style={{
                width: '100%',
                height: '300px',
                border: 'none',
                borderRadius: '8px',
              }}
            />
            <div className="modal-buttons-school">
              <button onClick={() => setShowUploadModal(false)} className="cancel-btn-school">Cancel</button>
              <button onClick={handleSubmit} className="submit-btn-school">Submit</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SchoolData;
