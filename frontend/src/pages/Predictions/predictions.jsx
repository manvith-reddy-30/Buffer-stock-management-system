import React from 'react';
import PredCityForm from '../../components/predCityForm';
import './Predictions.css'; // Import the CSS file

const Predictions = () => {
  return (
    <div className="predictions-page">
      <h1 className="predictions-header">This is the Predictions Page</h1>
      <div className="predictions-form-container">
        <PredCityForm />
      </div>
      <div>
        <button>AI generated report for maintaining the buffer qualtity </button>
      </div>
    </div>
  );
};

export default Predictions;
