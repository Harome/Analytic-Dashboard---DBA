import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Sidebar from './components/sidebar';
import './App.css';
import Home from './components/home';
import StudentData from './components/studentdata';
import SchoolData from './components/schooldata';
import DataComp from './components/datacomp';
import About from './components/about';

function App({ onLogout }) {
  const navigate = useNavigate();  // Correct place to use `useNavigate`

  const handleLogout = () => {
    onLogout(); // Handle logout passed from RootComponent
    navigate("/login");  // Redirect to login after logout
  };

  return (
    <div className="app-layout">
      {/* Sidebar with logout */}
      <Sidebar onLogout={handleLogout} />

      {/* Main Content */}
      <main className="content">
        <Routes>
          <Route path="/home" element={<Home />} />
          <Route path="/student-data" element={<StudentData />} />
          <Route path="/school-data" element={<SchoolData />} />
          <Route path="/data-comp" element={<DataComp />} />
          <Route path="/about" element={<About />} />
          <Route path="/" element={<Home />} /> {/* Default route */}
        </Routes>
      </main>
    </div>
  );
}

export default App;