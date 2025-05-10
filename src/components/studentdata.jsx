import React, { useState, useEffect, useCallback } from 'react';
import './studentdata.css'; // Make sure this CSS file exists

const StudentData = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [refreshKey, setRefreshKey] = useState(Date.now());
  const [role, setRole] = useState('');
  const [uploadFeedback, setUploadFeedback] = useState(''); // For messages from Dash

  const handleImport = () => {
    setUploadFeedback('Please use the dialog to upload your student dataset...');
    setShowUploadModal(true);
  };

  const handleModalCloseAndRefresh = useCallback(() => {
    setShowUploadModal(false);
    setRefreshKey(Date.now());
    console.log("[React] Modal closed or Dash signal received. Refreshing graph iframes.");
    // setUploadFeedback(''); // Clear feedback after action
  }, []);

  useEffect(() => {
    const storedRole = localStorage.getItem('role');
    if (storedRole) {
      setRole(storedRole);
    }
  }, []); // Runs once on mount to get role

  useEffect(() => {
    const handleMessageFromIframe = (event) => {
      // IMPORTANT: Check the origin of the message for security in production!
      // Example: if (event.origin !== "http://localhost:8050") {
      //   console.warn("[React] Message received from unexpected origin:", event.origin);
      //   return;
      // }

      if (event.data && event.data.type === 'dashUploadComplete') {
        const detail = event.data.detail;
        console.log('[React] Received dashUploadComplete message from iframe:', detail);
        
        // The 'status_detail' now comes from the graph update signal
        if (detail.status_detail === 'student_graphs_updated' || detail.status_detail === 'school_graphs_updated') { // Adjust if school uploads have different signal
          setUploadFeedback(`Dash: ${detail.type} data processed and graphs ready! Refreshing view...`);
          handleModalCloseAndRefresh();
        } else if (detail.status_detail === 'error_in_graph_generation' || detail.status_detail === 'error') {
          setUploadFeedback(`Dash Error: Could not generate graphs for ${detail.type} data. ${detail.message || ''}. Please check data or Dash logs.`);
           setShowUploadModal(false); 
        } else {
          setUploadFeedback(`Dash: Received status ${detail.status_detail} for ${detail.type} data.`);
          handleModalCloseAndRefresh(); // Default action if status is unexpected but positive
        }
      }
    };

    window.addEventListener('message', handleMessageFromIframe);
    console.log("[React] Event listener for 'message' from iframe added.");

    return () => {
      window.removeEventListener('message', handleMessageFromIframe);
      console.log("[React] Event listener for 'message' from iframe removed.");
    };
  }, [handleModalCloseAndRefresh]);

  const cardsData = [
    { id: "graph7", label: "Student Population per Grade Level by Gender", src: "http://localhost:8050/graph7" },
    { id: "graph8", label: "Student Distribution per SHS Strand by Sector", src: "http://localhost:8050/graph8" },
    { id: "graph9", label: "Student Distribution by Grade Division and School Sector", src: "http://localhost:8050/graph9" },
  ];

  return (
    <div className="student-data-container">
      <header className="student-header">
        <h1>Student Data (React App)</h1>
      </header>

      {role !== "user" && (
        <div className="import-export-top">
          <button onClick={handleImport}>Add New Student DataSet</button>
        </div>
      )}
      {uploadFeedback && <p style={{ textAlign: 'center', padding: '10px', color: uploadFeedback.includes('Error') ? 'red' : 'green' }}>{uploadFeedback}</p>}

      <div className="cards-wrapper">
        {cardsData.map((card) => (
          <div
            key={card.id}
            className="student-card"
            onClick={() => {
              setSelectedCard(card);
              setZoomLevel(1);
            }}
          >
            <label>{card.label}</label>
            <iframe
              key={`${card.id}-iframe-${refreshKey}`}
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
            <div className="modal-content" style={{ transform: `scale(${zoomLevel})`}}>
              <h2>{selectedCard.label}</h2>
              <iframe
                key={`${selectedCard.id}-modal-iframe-${refreshKey}`}
                src={`${selectedCard.src}?t=${refreshKey}`}
                title={selectedCard.label}
                style={{ width: '100%', height: '100%', border: 'none', borderRadius: '8px' }}
              />
              <div style={{ marginTop: '10px', textAlign: 'center' }}>
                <button onClick={() => setZoomLevel(prev => Math.max(0.5, prev - 0.1))}>Zoom Out</button>
                <button onClick={() => setZoomLevel(prev => Math.min(2, prev + 0.1))}>Zoom In</button>
                <button onClick={() => setZoomLevel(1)}>Reset Zoom</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {showUploadModal && (
        <div className="upload-modal-overlay-student" onClick={() => {
            setShowUploadModal(false);
        }}>
          <div className="upload-modal-student" onClick={(e) => e.stopPropagation()}>
            <h2>Add New Student Dataset</h2>
            <p style={{fontSize: '0.9em', color: '#555'}}><i>Complete the upload in the dialog. Graphs will refresh automatically upon success.</i></p>
            <iframe
              src="http://localhost:8050/upload_student"
              title="Upload Student Dataset (Dash iframe)"
              style={{
                width: '100%',
                height: '300px',
                border: '1px solid #eee',
                borderRadius: '8px',
              }}
            />
            <div className="modal-buttons-student" style={{ marginTop: '10px', textAlign: 'right' }}>
              <button onClick={() => {
                  setShowUploadModal(false);
              }} className="submit-btn-student">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentData;