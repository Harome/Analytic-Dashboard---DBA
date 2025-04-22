import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import Login from "./components/login";

const RootComponent = () => {
  const [showApp, setShowApp] = useState(false);

  return (
    <BrowserRouter>
      {showApp ? <App /> : <Login onLogin={() => setShowApp(true)} />}
    </BrowserRouter>
  );
};

const root = createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RootComponent />
  </React.StrictMode>
);
