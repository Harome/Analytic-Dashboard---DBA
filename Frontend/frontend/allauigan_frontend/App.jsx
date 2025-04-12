import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from "react-router-dom";
import { Home, User, School, BarChart2, Settings as SettingsIcon, LogOut, Menu, X, ZoomIn, ZoomOut, Download, Upload, UserCircle, Filter } from "lucide-react";

// Placeholder components for navigation
const StudentData = () => (
  <div className="bg-[#003366] min-h-screen w-full">
    <PageHeader title="Student Data" />
    <div className="p-8">
      <FilterPanel />
      <div className="grid grid-cols-3 gap-6">
        <DataCard 
          title="Student Count by Grade and Gender" 
          content={<div className="h-40 flex items-center justify-center">Grade/Gender Distribution Chart</div>}
        />
        <DataCard 
          title="Student Distribution by Region and District" 
          content={<div className="h-40 flex items-center justify-center">Region/District Map</div>}
        />
        <DataCard 
          title="Student Population per Grade by Sector" 
          content={<div className="h-40 flex items-center justify-center">Grade/Sector Chart</div>}
        />
        <DataCard 
          title="Student Count by Grade Division" 
          content={<div className="h-40 flex items-center justify-center">Grade Division Chart</div>}
        />
        <DataCard 
          title="Student Distribution by Strand" 
          content={<div className="h-40 flex items-center justify-center">Strand Distribution Chart</div>}
        />
      </div>
    </div>
  </div>
);
const SchoolData = () => <div className="p-8">School Data Page</div>;
const Analytics = () => <div className="p-8">Analytics Page</div>;
const SettingsPage = () => <div className="p-8">Settings Page</div>;

// Sidebar component
const Sidebar = ({ isOpen, toggleSidebar }) => {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <div className={`${isOpen ? 'w-64' : 'w-0'} transition-all duration-300 h-screen bg-gradient-to-b from-[#1C1F26] to-[#2E3649] text-white flex flex-col justify-between shadow-lg overflow-hidden`}>
      <div className="p-6">
        <h2 className="text-xl font-bold mb-8">DepEd Dashboard</h2>
        <nav className="flex flex-col gap-3">
          <Link to="/" className={`p-3 rounded-lg flex items-center gap-3 transition ${isActive("/") ? 'bg-[#3B4A63]' : 'hover:bg-[#3B4A63]'}`}> <Home size={20} /> Dashboard</Link>
          <Link to="/student-data" className={`p-3 rounded-lg flex items-center gap-3 transition ${isActive("/student-data") ? 'bg-[#3B4A63]' : 'hover:bg-[#3B4A63]'}`}> <User size={20} /> Student Data</Link>
          <Link to="/school-data" className={`p-3 rounded-lg flex items-center gap-3 transition ${isActive("/school-data") ? 'bg-[#3B4A63]' : 'hover:bg-[#3B4A63]'}`}> <School size={20} /> School Data</Link>
          <Link to="/analytics" className={`p-3 rounded-lg flex items-center gap-3 transition ${isActive("/analytics") ? 'bg-[#3B4A63]' : 'hover:bg-[#3B4A63]'}`}> <BarChart2 size={20} /> Analytics</Link>
        </nav>
      </div>
      <div className="p-6 space-y-2">
        <Link to="/settings" className={`p-3 rounded-lg flex items-center gap-3 transition ${isActive("/settings") ? 'bg-[#3B4A63]' : 'hover:bg-[#3B4A63]'}`}>
          <SettingsIcon size={20} /> Settings
        </Link>
        <button className="p-3 rounded-lg flex items-center gap-3 hover:bg-[#3B4A63] text-left transition w-full">
          <LogOut size={20} /> Log out
        </button>
      </div>
    </div>
  );
};

// FilterPanel component
const FilterPanel = () => (
  <div className="bg-gradient-to-r from-[#FDE68A] to-[#FCA5A5] p-4 rounded-lg shadow-lg mb-6 border border-yellow-300">
    <h3 className="text-xl font-semibold text-[#1F2937] mb-4">Filter Control Panel</h3>
    <div className="flex flex-wrap gap-4">
      <div className="flex items-center gap-2">
        <Filter size={20} className="text-gray-800" />
        <span className="text-sm font-medium text-gray-800">School Year:</span>
        <select className="px-3 py-2 rounded border border-gray-300 bg-white text-gray-800">
          <option>2022-2023</option>
          <option>2023-2024</option>
          <option>2024-2025</option>
        </select>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-gray-800">Education Level:</span>
        <select className="px-3 py-2 rounded border border-gray-300 bg-white text-gray-800">
          <option>Elementary</option>
          <option>Junior High</option>
          <option>Senior High</option>
        </select>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-gray-800">School Type:</span>
        <select className="px-3 py-2 rounded border border-gray-300 bg-white text-gray-800">
          <option>Public</option>
          <option>Private</option>
        </select>
      </div>
    </div>
  </div>
);

// DataCard component
const DataCard = ({ title, content, type = "square" }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const baseClasses = "bg-white p-6 shadow-lg transition-all duration-300 hover:shadow-xl cursor-pointer";
  const shapeClasses = {
    circle: "aspect-square rounded-full flex items-center justify-center",
    square: "rounded-xl min-h-[200px]"
  };

  return (
    <div className={`${baseClasses} ${shapeClasses[type]} relative cursor-pointer hover:shadow-xl`} onClick={() => setIsExpanded(true)}>
      {isExpanded ? (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg w-3/4 h-3/4 p-6 relative">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">{title}</h3>
              <div className="flex gap-2">
                <button className="p-2 hover:bg-gray-100 rounded"><ZoomIn size={20} /></button>
                <button className="p-2 hover:bg-gray-100 rounded"><ZoomOut size={20} /></button>
                <button className="p-2 hover:bg-gray-100 rounded"><Download size={20} /></button>
                <button className="p-2 hover:bg-gray-100 rounded"><Upload size={20} /></button>
                <button onClick={(e) => { e.stopPropagation(); setIsExpanded(false) }} className="p-2 hover:bg-gray-100 rounded">
                  <X size={20} />
                </button>
              </div>
            </div>
            <div className="h-[calc(100%-4rem)] overflow-auto">
              {content}
            </div>
          </div>
        </div>
      ) : (
        <div>
          <h3 className="font-semibold text-gray-800">{title}</h3>
          <div className="mt-2">{content}</div>
        </div>
      )}
    </div>
  );
};

// PageHeader component
const PageHeader = ({ title }) => (
  <div className="flex justify-between items-center px-8 pt-6 pb-4 bg-[#DDE8FC] shadow-sm">
    <h1 className="text-3xl font-bold text-[#1C1F26] font-sans">{title}</h1>
    <div className="flex items-center gap-4">
      <input type="text" placeholder="Search..." className="px-4 py-2 rounded-lg border border-gray-300 w-72 shadow focus:outline-none" />
      <button className="flex items-center gap-2 px-4 py-2 bg-[#3B4A63] text-white rounded-lg hover:bg-[#2E3649] transition">
        <UserCircle size={20} />
        Admin Login
      </button>
    </div>
  </div>
);

// Dashboard component
const Dashboard = () => (
  <div className="bg-[#003366] min-h-screen w-full">
    <PageHeader title="Dashboard" />
    <div className="p-8">
      <FilterPanel />
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white mb-6">Overview</h2>
        <div className="grid grid-cols-3 gap-6">
          <div>
            <DataCard 
              title="Total Number of Students" 
              content={<div className="text-2xl font-bold">0000</div>}
              type="circle"
            />
          </div>
          <DataCard 
            title="Student Population per Region" 
            content={<div className="h-40 flex items-center justify-center">Population Chart</div>}
          />
          <DataCard 
            title="Student Population per Year Level on Region" 
            content={<div className="h-40 flex items-center justify-center">Year Level Data</div>}
          />
        </div>
      </div>
      <div>
        <h2 className="text-3xl font-bold text-white mb-6">Summary</h2>
        <div className="grid grid-cols-3 gap-6">
          <div>
            <DataCard 
              title="Total Number of Schools" 
              content={<div className="text-2xl font-bold">0000</div>}
              type="circle"
            />
          </div>
          <DataCard 
            title="School Population per Region" 
            content={<div className="h-40 flex items-center justify-center">Region Data</div>}
          />
          <DataCard 
            title="School Population based on Sector Amongst All Regions" 
            content={<div className="h-40 flex items-center justify-center">Sector Data</div>}
          />
        </div>
      </div>
    </div>
  </div>
);

// App component
export default function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <Router>
      <div className="flex h-screen font-sans overflow-hidden">
        <Sidebar isOpen={isSidebarOpen} toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
        <div className="flex-1 overflow-y-auto relative">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="absolute top-4 left-4 z-10 p-2 rounded-lg bg-white shadow-md hover:bg-gray-100"
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/student-data" element={<StudentData />} />
            <Route path="/school-data" element={<SchoolData />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}
