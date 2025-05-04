import React from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";
import App from "./App"; // Corrected import for App.jsx
import Login from "./components/login";

const root = createRoot(document.getElementById("root"));

// Conditionally clear isLoggedIn during development
if (process.env.NODE_ENV === 'development') {
  localStorage.removeItem('isLoggedIn');
}

// Protect routes from unauthenticated access
const ProtectedRoute = ({ children }) => {
  // TEMPORARY: Force isLoggedIn to true for debugging
  const isLoggedIn = true;
  console.log("ProtectedRoute - isLoggedIn (FORCED TRUE):", isLoggedIn);
  return isLoggedIn ? children : <Navigate to="/login" />;
};

function RootRoutes() {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  console.log("RootRoutes - isLoggedIn on render:", isLoggedIn);

  return (
    <Routes>
      {/* Public Login Route */}
      <Route path="/login" element={<LoginWrapper />} />

      {/* Protected Routes */}
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <AppWrapper />
          </ProtectedRoute>
        }
      />

      {/* Redirect root path to /home if logged in, otherwise to /login */}
      <Route
        path="/"
        element={<Navigate to={isLoggedIn ? "/home" : "/login"} />}
      />

      {/* Catch-all route to redirect any unknown paths to login */}
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}


function LoginWrapper() {
  const navigate = useNavigate();

  const handleLogin = (role) => {
    console.log("handleLogin called with role:", role);
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("role", role);
    console.log("isLoggedIn set to true in localStorage");
    navigate("/home"); // Redirect to home after login
  };

  return <Login onLogin={handleLogin} />;
}

function AppWrapper() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("role");
    navigate("/login"); // Redirect to login after logout
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