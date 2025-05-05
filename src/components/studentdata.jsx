import React, { useState, useEffect } from 'react';
import './studentdata.css';

const StudentData = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [refreshKey, setRefreshKey] = useState(Date.now());
  const [role, setRole] = useState('');

  const handleImport = () => setShowUploadModal(true);

  const handleSubmit = () => {
    setShowUploadModal(false);
    setRefreshKey(Date.now()); // Refresh iframe by updating key
    console.log("Submit clicked, closing modal and refreshing graphs.");
  };

  useEffect(() => {
    document.documentElement.style.setProperty('--zoom', zoomLevel);
    const storedRole = localStorage.getItem('role');
    setRole(storedRole);
  }, [zoomLevel]);

  const cardsData = [
    { label: "Student Population per Grade Level by Gender", src: "http://localhost:8050/graph7" },
    { label: "Student Distrubution per SHS Strand by Sector", src: "http://localhost:8050/graph8" },
    { label: "Student Distribution by Grade Division and School Sector", src: "http://localhost:8050/graph9" },
  ];

  return (
    <div className="student-data-container">
      <header className="student-header">
        <h1>Student Data</h1>
      </header>

      {role !== "user" && (
        <div className="import-export-top">
          <button onClick={handleImport}>Add New DataSet</button>
        </div>
      )}

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
              src={`${card.src}?t=${refreshKey}`}
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
          <div className="modal-card-expanded-modal" onClick={(e) => e.stopPropagation()}>
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
                src={`${selectedCard.src}?t=${refreshKey}`}
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
        </div>
      )}

      {showUploadModal && (
        <div className="upload-modal-overlay-student" onClick={() => setShowUploadModal(false)}>
          <div className="upload-modal-student" onClick={(e) => e.stopPropagation()}>
            <h2>Add New Dataset</h2>
            <iframe
              src="http://localhost:8050/upload_student"
              title="Upload Student Dataset"
              style={{
                width: '100%',
                height: '300px',
                border: 'none',
                borderRadius: '8px',
              }}
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
