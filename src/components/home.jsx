import React, { useState, useEffect } from 'react';
import { FaSchool, FaMapMarkerAlt } from 'react-icons/fa';
import { IoMdPerson } from "react-icons/io";
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

  // Filtered graphs based on search query
  const filteredGraphs = graphs.filter((graph) =>
    graph.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentDateTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const formattedDate = currentDateTime.toLocaleDateString('en-PH', {
    timeZone: 'Asia/Manila',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const formattedTime = currentDateTime.toLocaleTimeString('en-PH', {
    timeZone: 'Asia/Manila',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
    hour12: true,
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
          placeholder="Search graphs"
        />
      </header>

      <div className="dashboard-container">
        <div className="left-section">
          <div className="top-container">
            <div className="stat-box">
              <FaSchool className="stat-icon" />
              <div>
                <h4>Number of Schools</h4>
                <p>60,157</p>
              </div>
            </div>
            <div className="stat-box">
              <IoMdPerson className="stat-icon" />
              <div>
                <h4>Number of Students</h4>
                <p>27,081,292</p>
              </div>
            </div>
            <div className="stat-box">
              <FaMapMarkerAlt className="stat-icon" />
              <div>
                <h4>Biggest Number of School and Students</h4>
                <p>Region IV-A</p>
              </div>
            </div>
          </div>

          <div className="middle-container">
            <div className="collage-grid">
              {filteredGraphs.length > 0 ? (
                filteredGraphs.map((graph, index) => (
                  <div
                    key={index}
                    className={`collage-card ${['wide', 'wide', 'small', 'small', 'wide'][index % 5]}`}
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
                ))
              ) : (
                <p>No graphs match your search.</p>
              )}
            </div>
          </div>
        </div>

        <div className="right-section">
          <div className="datetime-box">
            <h4 className="datetime-label">Current Date & Time</h4>
            <div className="datetime-value">
              <div className="time-text">{formattedTime}</div>
              <div className="date-text">{formattedDate}</div>
            </div>
          </div>
          <div className="heatmap-box">
            <div className="heatmap-placeholder">
              <iframe
                src="http://localhost:8050/graph6"
                title="Graph 6"
                className="iframe-graph"
                style={{
                  width: '100%',
                  height: '800px',
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
