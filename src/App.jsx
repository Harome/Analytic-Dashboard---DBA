import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Sidebar from './components/sidebar'; // Assuming Sidebar is in the 'components' folder
import './App.css';
import Home from './components/home';
import StudentData from './components/studentdata';
import SchoolData from './components/schooldata';

function App() {
  return (
    <div className="app-layout">
      {/* Sidebar Component */}
      <Sidebar />

      {/* Main Content */}
      <main className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/studentdata" element={<StudentData />} />
          <Route path="/school-data" element={<SchoolData />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
