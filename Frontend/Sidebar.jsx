import React from 'react'
import {
  FaHome,
  FaChartBar,
  FaUniversity,
  FaChartPie,
  FaAngleDoubleLeft
} from 'react-icons/fa'
import './Sidebar.css'

function Sidebar({ openSidebarToggle, OpenSidebar }) {
  return (
    <aside
      id="sidebar"
      className={`sidebar ${openSidebarToggle ? 'sidebar-responsive' : ''}`}
    >
      <div className="sidebar-title">
        <div className="sidebar-brand">
          <div className="circle-icon" />
          <span className="welcome-text">Welcome Back!</span>
        </div>
        <span className="icon close_icon" onClick={OpenSidebar}>
          <FaAngleDoubleLeft />
        </span>
      </div>

      <ul className="sidebar-list">
        <li className="sidebar-list-item">
          <a href="#">
            <FaHome className="icon" />
            <span className={openSidebarToggle ? '' : 'sidebar-text'}>Dashboard</span>
          </a>
        </li>
        <li className="sidebar-list-item">
          <a href="#">
            <FaChartBar className="icon" />
            <span className={openSidebarToggle ? '' : 'sidebar-text'}>Student Data</span>
          </a>
        </li>
        <li className="sidebar-list-item">
          <a href="#">
            <FaUniversity className="icon" />
            <span className={openSidebarToggle ? '' : 'sidebar-text'}>School Data</span>
          </a>
        </li>
        <li className="sidebar-list-item">
          <a href="#">
            <FaChartPie className="icon" />
            <span className={openSidebarToggle ? '' : 'sidebar-text'}>Analytics</span>
          </a>
        </li>
      </ul>
    </aside>
  )
}

export default Sidebar
