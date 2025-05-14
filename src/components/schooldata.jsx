import React, { useState, useEffect } from 'react';
import './schooldata.css';

const SchoolCard = ({ label, src, onClick, iframeKey }) => (
  <div className="school-card" onClick={onClick}>
    <label>{label}</label>
    <iframe
      key={iframeKey}
      src={`${src}?t=${new Date().getTime()}`}
      title={label}
      className="school-card-iframe"
    />
  </div>
);

const SchoolData = () => {
  const [selectedCard, setSelectedCard] = useState(null);  
  const [zoomLevel, setZoomLevel] = useState(1);  
  const [showUploadModal, setShowUploadModal] = useState(false);  

  const role = localStorage.getItem("role"); 

  const handleImport = () => {
    if (role === 'admin') {
      setShowUploadModal(true);
    } else {
      alert("You don't have permission to add new datasets.");
    }
  };

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
          <button onClick={handleImport}>Add New DataSet</button>
        </div>
      )}

      <div className="school-cards-wrapper">
        {cardsData.map((card, index) => (
          <SchoolCard
            key={index}
            label={card.label}
            src={card.src}
            iframeKey={iframeKey + index}
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
                key={iframeKey}
                src={`${selectedCard.src}?t=${new Date().getTime()}`}
                title={selectedCard.label}
                style={{ width: '100%', height: '100%', border: 'none' }}
              />
            </div>
          </div>
        </div>
      )}
      
      {showUploadModal && (
        <div className="upload-modal-overlay-school">
          <div className="upload-modal-school">
            <h2>Upload School Dataset</h2>
            <iframe
              src="http://localhost:8050/upload_student"
              title="Upload New Dataset"
              style={{
                width: '100%',
                height: '300px',
                border: 'none',
                borderRadius: '8px',
              }}
            />
            <div style={{ marginTop: "20px", display: "flex", justifyContent: "flex-end", gap: "10px" }}>
              <button className="cancel-btn-school" onClick={() => setShowUploadModal(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SchoolData;