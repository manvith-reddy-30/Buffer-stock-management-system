import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  const moveToAuth = (role) => {
    navigate('/auth', { state: { role } }); // Pass role as state
  };

  return (
    <div>
      <button onClick={() => moveToAuth('Admin')}>Admin</button>
      <button onClick={() => moveToAuth('Analyst')}>Analyst</button>
    </div>
  );
};

export default Home;