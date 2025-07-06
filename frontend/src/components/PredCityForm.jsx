import React, { useState } from 'react';

const PredCityForm = () => {
  const [city, setCity] = useState('');
  const [predictions, setPredictions] = useState([]);
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch(`${BACKEND_URL}/analyst/predictnext`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ city }),
    });

    if (response.ok) {
      const data = await response.json();
      setPredictions(data);
    } else {
      alert("Failed to fetch predictions");
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <label htmlFor="city">Select your city:</label>
        <select
          id="city"
          name="city"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          required
          style={{ marginLeft: '10px', padding: '5px' }}
        >
          <option value="">--Select--</option>
          <option value="hyderabad">Hyderabad</option>
          <option value="medak">Medak</option>
          <option value="warangal">Warangal</option>
          <option value="rangareddy">Ranga Reddy</option>
          <option value="nalgonda">Nalgonda</option>
        </select>

        <br /><br />

        <button
          type="submit"
          style={{
            padding: '8px 16px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Get Predictions
        </button>
      </form>

      {predictions.length > 0 && (
        <div style={{
          border: '1px solid #ddd',
          borderRadius: '8px',
          padding: '20px',
          maxWidth: '400px',
          backgroundColor: '#f9f9f9',
        }}>
          <h3 style={{ marginBottom: '10px', color: '#333' }}>Predicted Prices</h3>
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {predictions.map((price, index) => (
              <li
                key={index}
                style={{
                  background: '#fff',
                  marginBottom: '8px',
                  padding: '10px',
                  borderRadius: '4px',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                }}
              >
                Day {index + 1}: ₹{price.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default PredCityForm;
