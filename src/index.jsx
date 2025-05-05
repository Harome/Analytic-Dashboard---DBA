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

if (process.env.NODE_ENV === 'development') {
  localStorage.removeItem('isLoggedIn');
}

const ProtectedRoute = ({ children }) => {
  const isLoggedIn = true; // FORCED TRUE
  console.log("ProtectedRoute - isLoggedIn (FORCED TRUE):", isLoggedIn);
  return isLoggedIn ? children : <Navigate to="/login" />;
};

function RootRoutes() {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  console.log("RootRoutes - isLoggedIn on render:", isLoggedIn);

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
      {/* Make the root path a protected route */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppWrapper />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

function LoginWrapper() {
  const navigate = useNavigate();
  const handleLogin = (role) => {
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("role", role);
    navigate("/home");
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

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <RootRoutes />
    </BrowserRouter>
  </React.StrictMode>
);