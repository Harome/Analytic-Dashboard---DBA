import React, { useState, useEffect } from 'react';
import './schooldata.css';

const SchoolData = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [file, setFile] = useState(null);
  
  const handleImport = () => setShowUploadModal(true);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleSubmit = () => {
    if (file) {
      const fileExtension = file.name.split('.').pop().toLowerCase();
      if (fileExtension === 'csv' || fileExtension === 'xls' || fileExtension === 'xlsx') {
        // Handle actual file upload here
        console.log('Submitting file:', file.name);
        setShowUploadModal(false);
        setFile(null);
      } else {
        alert("Please select a valid CSV or Excel file.");
      }
    } else {
      alert("Please select a file before submitting.");
    }
  };

  useEffect(() => {
    document.documentElement.style.setProperty('--zoom', zoomLevel);
  }, [zoomLevel]);

  const cardsData = [
    { label: "School Distribution by Sector per region", src: "http://localhost:8050/graph10" },
    { label: "School Distribution by Sub-classification per Region", src: "http://localhost:8050/graph11" }
  ];

  return (
    <div className="school-data-container">
      <header className="school-header">
        <h1>School Data</h1>
      </header>
      
      <div className="import-export-sc">
        <button onClick={handleImport}>Add New DataSet</button>
      </div>

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
              src={card.src}
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

      {/* Modal */}
      {selectedCard && (
        <div className="modal-overlay" onClick={() => setSelectedCard(null)}>
          <div className="modal-cards expanded-modal" onClick={(e) => e.stopPropagation()}>
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
        </div>
      )}

      {showUploadModal && (
        <div className="upload-modal-overlay-school" onClick={() => setShowUploadModal(false)}>
          <div className="upload-modal-school" onClick={(e) => e.stopPropagation()}>
            <h2>Add New Dataset</h2>
            <p>Upload a CSV or Excel file:</p>
            <input 
              type="file" 
              onChange={handleFileChange} 
              accept=".csv, .xls, .xlsx" 
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
