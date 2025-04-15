import React, { useState } from 'react';
import './home.css';

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState('Region');

  const graphs = [
    { title: 'Graph 1', src: 'http://localhost:8050/graph1' },
    { title: 'Graph 2', src: 'http://localhost:8050/graph2' },
    { title: 'Graph 3', src: 'http://localhost:8050/graph3' },
    { title: 'Graph 4', src: 'http://localhost:8050/graph4' },
    { title: 'Graph 5', src: 'http://localhost:8050/graph5' },
  ];

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Overview</h1>
        <input
          type="text"
          className="search-input"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Search..."
        />
        <select className="filter-dropdown" onChange={handleFilterChange}>
          <option value="Region">Compare by Region</option>
          <option value="Year">Compare by Year</option>
          <option value="Enrollment">Compare by Enrollment</option>
        </select>
      </header>

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
  );
};

export default Home;
