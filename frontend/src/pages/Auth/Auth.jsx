import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Auth.css';

const Auth = ({ setUser }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const roleFromState = location.state?.role || 'User';

  const [govt_id, setGovtId] = useState('');
  const [password, setPassword] = useState('');

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      govt_id,
      password,
      user_type: roleFromState.toLowerCase(), // include user_type
    };

    try {
      const response = await fetch(`${BACKEND_URL}/user/auth`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const resData = await response.json();

        // Store user in localStorage for persistence
        const user = { username: resData.user.username, role: roleFromState };
        localStorage.setItem('user', JSON.stringify(user));
        setUser(user);

        // Navigate based on role
        if (roleFromState.toLowerCase() === 'admin') {
          navigate('/admin');
        } else if (roleFromState.toLowerCase() === 'analyst') {
          navigate('/predictions');
        } else {
          navigate('/');
        }
      } else {
        const errorData = await response.json();
        alert(errorData.detail);
      }
    } catch (error) {
      console.error("Server error:", error);
      alert("Server Error");
    }
  };

  return (
    <div className="auth-container">
      <h1>Login as {roleFromState}</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="govt_id">Govt ID:</label>
          <input
            type="text"
            id="govt_id"
            name="govt_id"
            value={govt_id}
            onChange={(e) => setGovtId(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Auth;
