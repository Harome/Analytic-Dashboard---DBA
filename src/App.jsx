import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/sidebar';
import './App.css';
import Home from './components/home';
import StudentData from './components/studentdata';
import SchoolData from './components/schooldata';
import DataComp from './components/datacomp';

function App() {
  return (
    <div className="app-layout">
      {/* Sidebar Component */}
      <Sidebar />

      {/* Main Content */}
      <main className="content">
        <Routes>
          <Route path="/home" element={<Home />} /> {/* ✅ Updated path */}
          <Route path="/student-data" element={<StudentData />} />
          <Route path="/school-data" element={<SchoolData />} />
          <Route path="/data-comp" element={<DataComp />} />
          {/* Optional: Default route redirects to /home */}
          <Route path="/" element={<Home />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
