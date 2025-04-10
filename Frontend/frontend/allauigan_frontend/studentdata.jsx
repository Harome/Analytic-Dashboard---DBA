import React from "react";
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from "react-router-dom";
import { Home, User, School, BarChart2, Settings as SettingsIcon, LogOut } from "lucide-react";

// Sidebar component
const Sidebar = () => {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <div className="w-64 h-screen bg-gradient-to-b from-[#1C1F26] to-[#2E3649] text-white p-6 flex flex-col justify-between shadow-lg">
      <div>
        <h2 className="text-xl font-bold mb-8">DepEd Dashboard</h2>
        <nav className="flex flex-col gap-3">
          <Link to="/" className={`p-3 rounded-lg flex items-center gap-3 transition ${isActive("/") ? 'bg-[#3B4A63]' : 'hover:bg-[#3B4A63]'}`}> <Home size={20} /> Dashboard</Link>
          <Link to="/student-data" className={`p-3 rounded-lg flex items-center gap-3 transition ${isActive("/student-data") ? 'bg-[#3B4A63]' : 'hover:bg-[#3B4A63]'}`}> <User size={20} /> Student Data</Link>
          <Link to="/school-data" className={`p-3 rounded-lg flex items-center gap-3 transition ${isActive("/school-data") ? 'bg-[#3B4A63]' : 'hover:bg-[#3B4A63]'}`}> <School size={20} /> School Data</Link>
          <Link to="/analytics" className={`p-3 rounded-lg flex items-center gap-3 transition ${isActive("/analytics") ? 'bg-[#3B4A63]' : 'hover:bg-[#3B4A63]'}`}> <BarChart2 size={20} /> Analytics</Link>
        </nav>
      </div>
      <div className="space-y-2">
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

// PageHeader component
const PageHeader = ({ title }) => (
  <div className="flex justify-between items-center px-8 pt-6 pb-4 bg-[#DDE8FC] shadow-sm">
    <h1 className="text-3xl font-bold text-[#1C1F26] font-sans">{title}</h1>
    <input type="text" placeholder="Search..." className="px-4 py-2 rounded-lg border border-gray-300 w-72 shadow focus:outline-none" />
  </div>
);

// PageGrid component
const PageGrid = ({ items }) => (
  <div className="grid grid-cols-2 lg:grid-cols-3 gap-6 p-8">
    {items.map((title, index) => (
      <div key={index} className="h-40 bg-[#C7D6F3] p-6 font-semibold text-gray-800 rounded-2xl shadow hover:shadow-lg transition">{title}</div>
    ))}
  </div>
);

// Dashboard component
const Dashboard = () => (
  <div className="bg-[#E3EAFD] min-h-screen w-full">
    <PageHeader title="Dashboard" />
    <PageGrid items={[
      "Total Number of Students",
      "Student Population per Region",
      "Student Population per Year Level on Region",
      "Total Number of Schools",
      "School Population per Region",
      "School Population based on Sector Amongst All Regions"
    ]} />
  </div>
);

// StudentData component
const StudentData = () => (
  <div className="bg-[#E3EAFD] min-h-screen w-full">
    <PageHeader title="Student Data" />
    <PageGrid items={[
      "Student Count by Grade and Gender",
      "Student Distribution by Region and District",
      "Student Population per Grade by Sector",
      "Student Count by Grade Division",
      "Student Distribution by Strand"
    ]} />
  </div>
);

// SchoolData component
const SchoolData = () => (
  <div className="bg-[#E3EAFD] min-h-screen w-full">
    <PageHeader title="School Data" />
    <PageGrid items={[
      "School Distribution by Sector per Region",
      "School Distribution by Subclassification per Region",
      "School Distribution by Modified COC per Region",
      "School Distribution by District per Region"
    ]} />
  </div>
);

// Analytics component
const Analytics = () => (
  <div className="bg-[#E3EAFD] min-h-screen w-full">
    <PageHeader title="Analytics" />
    <PageGrid items={[
      "Regional Population Trends",
      "Enrollment Insights",
      "Student Population Patterns",
      "Education Quality Analysis"
    ]} />
  </div>
);

// SettingsPage component (Renamed from Settings)
const SettingsPage = () => (
  <div className="bg-[#E3EAFD] min-h-screen w-full">
    <PageHeader title="Settings" />
    <PageGrid items={[
      "Profile Settings",
      "Notification Preferences",
      "Account Security",
      "Theme Settings"
    ]} />
  </div>
);

// App component
export default function App() {
  return (
    <Router>
      <div className="flex h-screen font-sans overflow-hidden">
        <Sidebar />
        <div className="flex-1 overflow-y-auto">
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
