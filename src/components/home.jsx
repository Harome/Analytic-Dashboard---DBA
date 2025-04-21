import React, { useState, useEffect } from 'react';
import './home.css';

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [currentDateTime, setCurrentDateTime] = useState(new Date());

  const graphs = [
    { title: 'Graph 1', src: 'http://localhost:8050/graph1' },
    { title: 'Graph 2', src: 'http://localhost:8050/graph2' },
    { title: 'Graph 3', src: 'http://localhost:8050/graph3' },
    { title: 'Graph 4', src: 'http://localhost:8050/graph4' },
    { title: 'Graph 5', src: 'http://localhost:8050/graph5' },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentDateTime(new Date());
    }, 1000);

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const formattedDateTime = currentDateTime.toLocaleString('en-PH', {
    dateStyle: 'medium',
    timeStyle: 'medium',
  });

  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Overview</h1>
        <input
          type="text"
          className="search-input-home"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Search..."
        />
      </header>

      {/* Dashboard Layout */}
      <div className="dashboard-container">
        <div className="left-section">
          {/* Top container for stat boxes */}
          <div className="top-container">
            <div className="stat-box">
              <i className="fas fa-school stat-icon"></i>
              <div>
                <h4>Number of Schools</h4>
                <p>60,157</p>
              </div>
            </div>
            <div className="stat-box">
              <i className="fas fa-user-graduate stat-icon"></i>
              <div>
                <h4>Number of Students</h4>
                <p>27 Million</p>
              </div>
            </div>
            <div className="stat-box">
              <i className="fas fa-map-marker-alt stat-icon"></i>
              <div>
                <h4>Population</h4>
                <p>Region IV-A</p>
              </div>
            </div>
          </div>

          {/* Middle container for graphs */}
          <div className="middle-container">
            <div className="collage-grid">
              {graphs.map((graph, index) => (
                <div
                  key={index}
                  className={`collage-card ${['large', 'wide', 'small', 'small', 'wide'][index % 5]}`}
                >
                  <h3>{graph.title}</h3>
                  <iframe
                    src={graph.src}
                    title={graph.title}
                    className="iframe-graph"
                    style={{
                      width: '100%',
                      height: '100%',
                      border: 'none',
                    }}
                  />
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="right-section">
          <div className="datetime-box">
            <h4 className="datetime-label">Current Date & Time</h4>
            <div className="datetime-value">{formattedDateTime}</div>
          </div>
          <div className="heatmap-box">
            <h4 className="heatmap-label">Heatmap</h4>
            <div className="heatmap-placeholder">
              <iframe
                src="http://localhost:8050/graph6"
                title="Graph 6"
                className="iframe-graph"
                style={{
                  width: '100%',
                  height: '300px',
                  border: 'none',
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;