// Sidebar.jsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaHome, FaUniversity, FaChartBar, FaSignOutAlt, FaInfoCircle } from 'react-icons/fa';
import { MdCompare } from "react-icons/md";
import './sidebar.css';

const Sidebar = ({ onLogout }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <img src="/deped.png" alt="DepEd" className="deped-logo" />
        <h2>DepEd Dashboard</h2>
      </div>
      <ul className="sidebar-list">
        <li>
          <NavLink to="/home" end>
            <FaHome /> Home
          </NavLink>
        </li>
        <li>
          <NavLink to="/student-data">
            <FaChartBar /> Student Data
          </NavLink>
        </li>
        <li>
          <NavLink to="/school-data">
            <FaUniversity /> School Data
          </NavLink>
        </li>
        <li>
          <NavLink to="/data-comp">
            <MdCompare /> Data Comparison
          </NavLink>
        </li>
        <li>
          <NavLink to="/about">
            <FaInfoCircle /> About
          </NavLink>
        </li>
        <li>
          <button onClick={onLogout} className="logout-btn">
            <FaSignOutAlt /> Logout
          </button>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;