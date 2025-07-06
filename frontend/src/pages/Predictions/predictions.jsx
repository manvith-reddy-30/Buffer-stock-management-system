import React from 'react';
import PredCityForm from '../../components/predCityForm';
import './Predictions.css'; // Import the CSS file
import Weather from '../../components/Weather';
import BufferReport from '../../components/bufferReport';

const Predictions = () => {

  return (
    <div className="predictions-page">
      <h1 className="predictions-header">This is the Predictions Page</h1>
      <div className="predictions-form-container">
        <PredCityForm />
      </div>
      <div className="predictions-form-container">
       <Weather />
      </div>
      <div className="predictions-form-container">
        <BufferReport/>
      </div>
    </div>
  );
};

export default Predictions;
