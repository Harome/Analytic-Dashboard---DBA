// Sidebar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaUniversity, FaChartBar, FaChartPie } from 'react-icons/fa';
import './sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>DepEd Enrollment Data</h2>
      </div>
      <ul className="sidebar-list">
        <li>
          <Link to="/">
            <FaHome /> Home
          </Link>
        </li>
        <li>
          <Link to="/student-data">
            <FaChartBar /> Student Data
          </Link>
        </li>
        <li>
          <Link to="/school-data">
            <FaUniversity /> School Data
          </Link>
        </li>
        <li>
          <Link to="/analytics">
            <FaChartPie /> Analytics
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
