import React from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";
import App from "./App";
import Login from "./components/login";

const root = createRoot(document.getElementById("root"));

// Check for both auth and role
const ProtectedRoute = ({ children }) => {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  return isLoggedIn ? children : <Navigate to="/login" />;
};

function RootRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginWrapper />} />
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <AppWrapper />
          </ProtectedRoute>
        }
      />
      {/* Default redirect based on role */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <RedirectBasedOnRole />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

function LoginWrapper() {
  const navigate = useNavigate();

  const handleLogin = (role) => {
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("role", role);

    if (role === "admin") {
      navigate("/school-data");
    } else if (role === "user") {
      navigate("/student-data");
    } else {
      navigate("/home"); // fallback
    }
  };

  return <Login onLogin={handleLogin} />;
}

function AppWrapper() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("role");
    navigate("/login");
  };

  return <App onLogout={handleLogout} />;
}

function RedirectBasedOnRole() {
  const role = localStorage.getItem("role");

  if (role === "admin") {
    return <Navigate to="/school-data" replace />;
  } else if (role === "user") {
    return <Navigate to="/student-data" replace />;
  } else {
    return <Navigate to="/home" replace />;
  }
}

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <RootRoutes />
    </BrowserRouter>
  </React.StrictMode>
);
