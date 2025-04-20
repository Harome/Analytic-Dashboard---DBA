// Sidebar.jsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaHome, FaUniversity, FaChartBar } from 'react-icons/fa';
import { MdCompare } from "react-icons/md";
import './sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <img src="/deped.png" alt="DepEd" className="deped-logo" />
        <h2>DepEd Dashboard</h2>
      </div>
      <ul className="sidebar-list">
        <li>
          <NavLink to="/" end>
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
            <MdCompare/> Data Comparison
          </NavLink>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
