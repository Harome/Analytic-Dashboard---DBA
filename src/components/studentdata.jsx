import React, { useState, useEffect } from 'react';
import './studentdata.css';

const StudentData = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [file, setFile] = useState(null);

  const handleZoomIn = () => setZoomLevel((prev) => Math.min(prev + 0.1, 2));
  const handleZoomOut = () => setZoomLevel((prev) => Math.max(prev - 0.1, 0.5));

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
    { label: "Regional Population Trends", src: "http://localhost:8050/graph7" },
    { label: "Enrollment Insights", src: "http://localhost:8050/graph8" },
    { label: "Student Population Patterns", src: "http://localhost:8050/graph9" },
  ];

  return (
    <div className="student-data-container">
      <header className="student-header">
        <h1>Student Data</h1>
      </header>

      <div className="import-export-top">
        <button onClick={handleImport}>Add New DataSet</button>
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
                height: '750px',
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
          <div className="modal-card expanded-modal" onClick={(e) => e.stopPropagation()}>
            <div
              className="modal-content"
              style={{
                transform: `scale(${zoomLevel})`,
                width: `${100 / zoomLevel}%`,
                height: `${100 / zoomLevel}%`,
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
                  borderRadius: '8px',
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

      {showUploadModal && (
        <div className="upload-modal-overlay-student" onClick={() => setShowUploadModal(false)}>
          <div className="upload-modal-student" onClick={(e) => e.stopPropagation()}>
            <h2>Add New Dataset</h2>
            <p>Upload a CSV or Excel file:</p>
            <input 
              type="file" 
              onChange={handleFileChange} 
              accept=".csv, .xls, .xlsx" 
            />
            <div className="modal-buttons-student">
              <button onClick={() => setShowUploadModal(false)} className="cancel-btn-student">Cancel</button>
              <button onClick={handleSubmit} className="submit-btn-student">Submit</button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default StudentData;
