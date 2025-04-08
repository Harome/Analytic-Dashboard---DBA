import React from 'react';
import './Home.css';
import { FaArrowLeft, FaArrowRight } from 'react-icons/fa';

function Home() {
  const scrollSlider = (direction) => {
    const slider = document.querySelector('.scrollable-cards');
    if (direction === 'left') {
      slider.scrollBy({ left: -300, behavior: 'smooth' });
    } else {
      slider.scrollBy({ left: 300, behavior: 'smooth' });
    }
  };

  return (
    <main className="main-container">
      <div className="main-title">
        <h2>Dashboard</h2>
      </div>

      <section className="overview-section">
        <div className="section-header">
          <h3>Overview</h3>
          <div className="arrow-buttons">
            <button onClick={() => scrollSlider('left')}><FaArrowLeft /></button>
            <button onClick={() => scrollSlider('right')}><FaArrowRight /></button>
          </div>
        </div>
        <div className="scrollable-cards">
          {[...Array(6)].map((_, idx) => (
            <div className="card" key={idx}>
              <h4>Card {idx + 1}</h4>
              <p>This is an overview item.</p>
            </div>
          ))}
        </div>
      </section>

      <section className="summary-section">
        <div className="section-header">
          <h3>Summary</h3>
          <select>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
        </div>
        <div className="summary-cards">
          <div className="card">Summary Data 1</div>
          <div className="card">Summary Data 2</div>
          <div className="card">Summary Data 3</div>
        </div>
      </section>
    </main>
  );
}

export default Home;
