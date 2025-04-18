import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/sidebar'; // Assuming Sidebar is in the 'components' folder
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
          <Route path="/" element={<Home />} />
          <Route path="/student-data" element={<StudentData />} />
          <Route path="/school-data" element={<SchoolData />} />
          <Route path="/data-comp" element={<DataComp />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
