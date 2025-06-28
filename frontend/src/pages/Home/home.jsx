import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  const moveToAdmin = () => {
    navigate('/admin');
  };

  const moveToPredictions = () => {
    navigate('/predictions');
  };

  return (
    <div>
      <button onClick={moveToAdmin}>Admin</button>
      <button onClick={moveToPredictions}>See predictions</button>
    </div>
  );
};

export default Home;
