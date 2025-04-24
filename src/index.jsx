import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import Login from "./components/login";

const RootComponent = () => {
  const [showApp, setShowApp] = useState(false);

  useEffect(() => {
    const isLoggedIn = localStorage.getItem("isLoggedIn");
    if (isLoggedIn === "true") {
      setShowApp(true);
    }
  }, []);

  const handleLogin = () => {
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("loginTime", Date.now());
    setShowApp(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("loginTime");
    setShowApp(false);
  };

  // timeout logic
  useEffect(() => {
    const interval = setInterval(() => {
      const loginTime = localStorage.getItem("loginTime");
      const timeoutDuration = 10 * 60 * 1000; // 10 minutes
      if (loginTime && Date.now() - loginTime > timeoutDuration) {
        alert("Session expired. Logging out...");
        handleLogout();
      }
    }, 10000); // check every 10 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <BrowserRouter>
      {showApp ? <App onLogout={handleLogout} /> : <Login onLogin={handleLogin} />}
    </BrowserRouter>
  );
};

const root = createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RootComponent />
  </React.StrictMode>
);
