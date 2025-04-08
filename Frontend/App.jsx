import React, { useRef, useState } from 'react'
import Sidebar from './sidebar'
import './App.css'
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa'

function App() {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const sliderRef = useRef(null)

  const toggleSidebar = () => {
    setIsCollapsed(prev => !prev)
  }

  const scrollLeft = () => {
    sliderRef.current.scrollBy({ left: -600, behavior: 'smooth' })
  }

  const scrollRight = () => {
    sliderRef.current.scrollBy({ left: 600, behavior: 'smooth' })
  }

  return (
    <div className="app-layout">
      <Sidebar openSidebarToggle={isCollapsed} OpenSidebar={toggleSidebar} />

      <main className={`main-content ${isCollapsed ? 'collapsed' : ''}`}>
        <header className="main-header">
          <h1>Dashboard Overview</h1>
          <select className="filter-dropdown">
            <option>Filter: All</option>
            <option>Region</option>
            <option>Grade Level</option>
            <option>Gender Distribution</option>
          </select>
        </header>

        <section className="slider-section">
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
        </section>

        <section className="summary-section">
          <h2>Summary</h2>
          <div className="summary-card">
            <p>This section can contain analytics summary or reports.</p>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
