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
          {[...Array(6)].map((_, index) => (
            <div key={index} className="card">
              <h3>Card {index + 1}</h3>
              <p>This is a container in the slider.</p>
            </div>
          ))}
        </div>

        <button className="arrow-button right" onClick={scrollRight}>
          <FaChevronRight />
        </button>
      </div>
    </div>
  );
};

export default Home;
