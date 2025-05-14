import React, { useState, useEffect } from 'react';
import './studentdata.css';

const StudentData = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [iframeKey, setIframeKey] = useState(Date.now());
  const [role, setRole] = useState('');

  const handleImport = () => {
    if (role === 'admin') {
      setShowUploadModal(true);
    } else {
      alert("You don't have permission to add new datasets.");
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://localhost:8050/last_update")
        .then((res) => res.json())
        .then((data) => {
          const lastStudentUpdate = localStorage.getItem("lastStudentUpdate");
          if (data.student.toString() !== lastStudentUpdate) {
            localStorage.setItem("lastStudentUpdate", data.student.toString());
            setIframeKey(Date.now()); // trigger refresh
          }
        });
    }, 10000); // check every 10 seconds
  
    return () => clearInterval(interval);
  }, []);
  

  useEffect(() => {
    document.documentElement.style.setProperty('--zoom', zoomLevel);
    const storedRole = localStorage.getItem('role');
    setRole(storedRole);
  }, [zoomLevel]);

  const cardsData = [
    {
      label: "Student Population per Grade Level by Gender",
      src: "http://localhost:8050/graph7"
    },
    {
      label: "Student Distribution per SHS Strand by Sector",
      src: "http://localhost:8050/graph8"
    },
    {
      label: "Student Distribution by Grade Division and School Sector",
      src: "http://localhost:8050/graph9"
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

      <div className="full-width-card">
        <div
          className="student-card"
          onClick={() => {
            setSelectedCard(cardsData[0]);
            setZoomLevel(1);
          }}
        >
          <label>{cardsData[0].label}</label>
          <iframe
            src={`${cardsData[0].src}?t=${new Date().getTime()}`}
            title={cardsData[0].label}
            className="student-iframe"
            />
        </div>
      </div>

      <div className="grid-two-cards">
        {[cardsData[1], cardsData[2]].map((card, index) => (
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
              src={`${card.src}?t=${iframeKey}`}
              title={card.label}
              className="student-iframe"
            />
          </div>
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
                key={`${iframeKey}-${selectedCard.label}`}
                src={`${selectedCard.src}?t=${new Date().getTime()}`}
                title={selectedCard.label}
                style={{ width: '100%', height: '100%', border: 'none' }}
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
            <div className="modal-buttons-school">
              <button onClick={() => setShowUploadModal(false)} className="cancel-btn-school">Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentData;
