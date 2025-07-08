import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Home from './pages/Home/home';
import Auth from './pages/Auth/Auth';
import Admin from './pages/Admin/Admin';
import Predictions from './pages/Predictions/Predictions';
import { ToastContainer } from 'react-toastify';

const App = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check localStorage for existing user on first load
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      const parsedUser = JSON.parse(storedUser);
      setUser(parsedUser);

      // Navigate based on role
      if (parsedUser.role.toLowerCase() === 'admin') {
        navigate('/admin');
      } else if (parsedUser.role.toLowerCase() === 'analyst') {
        navigate('/predictions');
      }
    }
  }, [navigate]);

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
    navigate('/'); // Go back to home page after logout
  };

  return (
    <div>
      {user && (
        <button onClick={handleLogout} style={{ position: 'absolute', top: 10, right: 10 }}>
          Logout
        </button>
      )}

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/auth" element={<Auth setUser={setUser} />} />
        <Route path="/admin" element={user?.role.toLowerCase() === 'admin' ? <Admin /> : <Home />} />
        <Route path="/predictions" element={user?.role.toLowerCase() === 'analyst' ? <Predictions /> : <Home />} />
      </Routes>
      <ToastContainer position="top-right" autoClose={3000} theme="colored" />
    </div>
  );
};

export default App;
