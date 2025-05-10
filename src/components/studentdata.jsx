import React, { useState, useEffect } from 'react';
import './studentdata.css';

const StudentData = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [role, setRole] = useState('');

  const handleImport = () => setShowUploadModal(true);

  useEffect(() => {
    document.documentElement.style.setProperty('--zoom', zoomLevel);
    const storedRole = localStorage.getItem('role');
    setRole(storedRole);
  }, [zoomLevel]);

  const cardsData = [
    {
      label: "Student Population per Grade Level by Gender",
      src: "http://localhost:8050/graph7",
      className: "g1"
    },
    {
      label: "Student Distrubution per SHS Strand by Sector",
      src: "http://localhost:8050/graph8",
      className: "g2"
    },
    {
      label: "Student Distribution by Grade Division and School Sector",
      src: "http://localhost:8050/graph9",
      className: "g3"
    },
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

  {/* Card 1 - Full width */}
  <div className="full-width-card">
    <div
      className="student-card card-style-1"
      onClick={() => {
        setSelectedCard(cardsData[0]);
        setZoomLevel(1);
      }}
    >
      <label>{cardsData[0].label}</label>
      <iframe
        src={cardsData[0].src}
        title={cardsData[0].label}
        className="student-iframe"
      />
    </div>
  </div>

  {/* Cards 2 & 3 - Side by side */}
  <div className="grid-two-cards">
    <div
      className="student-card card-style-2"
      onClick={() => {
        setSelectedCard(cardsData[1]);
        setZoomLevel(1);
      }}
    >
      <label>{cardsData[1].label}</label>
      <iframe
        src={cardsData[1].src}
        title={cardsData[1].label}
        className="student-iframe"
      />
    </div>

    <div
      className="student-card card-style-3"
      onClick={() => {
        setSelectedCard(cardsData[2]);
        setZoomLevel(1);
      }}
    >
      <label>{cardsData[2].label}</label>
      <iframe
        src={cardsData[2].src}
        title={cardsData[2].label}
        className="student-iframe"
        style={{
          width:"600",
          height: "400",
          display: 'block',
          margin: '0 auto',
        }}
      />
    </div>
  </div>


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
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentData;