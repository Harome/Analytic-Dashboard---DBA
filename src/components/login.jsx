import React, { useState } from "react";
import "./Login.css";

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = {};
    if (!username.trim()) validationErrors.username = "Username is required";
    if (!password) validationErrors.password = "Password is required";

    setErrors(validationErrors);

    if (Object.keys(validationErrors).length === 0) {
      onLogin();
    }
  };

  return (
    <>
      {/* DepEd logo positioned at the top left */}
      <img src="/deped.png" alt="DepEd Logo" className="logo-top-left" />

      <div className="login-page">
        <div className="login-left">
          <form className="login-box" onSubmit={handleSubmit}>
            <h1>Welcome</h1>

            <div className="input-group">
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              {errors.username && <span className="error-text">{errors.username}</span>}
            </div>

            <div className="input-group">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              {errors.password && <span className="error-text">{errors.password}</span>}
            </div>

            <button type="submit" className="login-button">
              Log in
            </button>
          </form>
        </div>
        <div className="login-right">
          <img src="/login.png" alt="Background" className="login-image" />
        </div>
      </div>
    </>
  );
};

export default Login;
