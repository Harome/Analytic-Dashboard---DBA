import React, { useRef } from 'react';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';
import './home.css';

const Home = () => {
  const sliderRef = useRef(null);

  const scrollLeft = () => {
    sliderRef.current.scrollBy({ left: -300, behavior: 'smooth' });
  };

  const scrollRight = () => {
    sliderRef.current.scrollBy({ left: 300, behavior: 'smooth' });
  };

  return (
    <div className="home-content">
      <h2>Overview</h2>
      <div className="slider-wrapper">
        <button className="arrow-button left" onClick={scrollLeft}>
          <FaChevronLeft />
        </button>

        <div className="card-slider" ref={sliderRef}>
          <div className="card">
              <h3>Graph 1</h3>
              <iframe
                src="http://localhost:8050/graph1"
                title="Graph 1"
                style={{ width: '50%', height: '400px', border: 'none' }}
              />
          </div>
          <div className="card">
            <h3>Graph 2</h3>
            <iframe
              src="http://localhost:8050/graph2"
              title="Graph 2"
              style={{ width: '50%', height: '400px', border: 'none' }}
            />
          </div>

          <div className="card">
            <h3>Graph 3</h3>
            <iframe
              src="http://localhost:8050/graph3"
              title="Graph 3"
              style={{ width: '50%', height: '400px', border: 'none' }}
            />
          </div>

          <div className="card">
            <h3>Graph 4</h3>
            <iframe
              src="http://localhost:8050/graph4"
              title="Graph 4"
              style={{ width: '50%', height: '400px', border: 'none' }}
            />
          </div>
        </div>

        <button className="arrow-button right" onClick={scrollRight}>
          <FaChevronRight />
        </button>
      </div>
    </div>
  );
};

export default Home;
