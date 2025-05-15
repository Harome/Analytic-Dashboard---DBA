import React, { useState, useEffect } from 'react';
import './studentdata.css';

const StudentData = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [role, setRole] = useState('');

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

      {role === 'admin' && (
        <div className="import-export-top">
          <a
            href="http://localhost:8050/student_page"
            target="_blank"
            rel="noopener noreferrer"
            className="upload-link-button"
          >
            Import Dataset
          </a>
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
            src={cardsData[0].src}
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
              src={card.src}
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

export default StudentData;
