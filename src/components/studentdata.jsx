import React, { useState, useEffect } from 'react';
import './studentdata.css';

const StudentData = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [file, setFile] = useState(null);
  const [role, setRole] = useState('');
  const [iframeKey, setIframeKey] = useState(Date.now());

  const handleImport = () => setShowUploadModal(true);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleSubmit = async () => {
    if (file) {
      const fileExtension = file.name.split('.').pop().toLowerCase();

      if (['csv', 'xls', 'xlsx'].includes(fileExtension)) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('type', 'student');

        try {
          const response = await fetch('http://localhost:8050/upload_dataset', {
            method: 'POST',
            body: formData
          });

          const result = await response.json();

          if (result.status === 'success') {
            alert(result.message);
            setIframeKey(Date.now());
            setSelectedCard(null);
          } else {
            alert("Upload failed: " + result.message);
          }
        } catch (error) {
          console.error('Error uploading file:', error);
          alert("An error occurred during upload.");
        }

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
            key={iframeKey}
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
              key={iframeKey + index + 1}
              src={`${card.src}?t=${new Date().getTime()}`}
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
        <div className="upload-modal-overlay-student">
          <div className="upload-modal-student">
            <h2>Upload Student Dataset</h2>
            <input type="file" accept=".csv, .xls, .xlsx" onChange={handleFileChange} />
            <div style={{ marginTop: "20px", display: "flex", justifyContent: "flex-end", gap: "10px" }}>
              <button className="cancel-btn-student" onClick={() => setShowUploadModal(false)}>Cancel</button>
              <button className="submit-btn-student" onClick={handleSubmit}>Submit</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentData;