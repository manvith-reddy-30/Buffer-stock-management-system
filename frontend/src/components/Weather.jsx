import React, { useState } from 'react';

const Weather = () => {
  const [city, setCity] = useState('');
  const [weatherData, setWeatherData] = useState([]);
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch(`${BACKEND_URL}/analyst/weather`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ city }),
    });

    if (response.ok) {
      const data = await response.text(); // response is a string
      const parsedData = parseWeatherData(data);
      setWeatherData(parsedData);
    } else {
      console.error('Error fetching weather data');
    }
  };

  const parseWeatherData = (data) => {
    const lines = data.trim().split('\n');
    return lines.map(line => {
      const [dayInfo, weather1, weather2, prob1, prob2, temp, humidity] = line.split(',').map(s => s.trim());
      return {
        dayInfo,
        weather: weather1, // taking only first weather for simplicity
        probability: prob1, // taking only first probability
        temp,
        humidity
      };
    });
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <form onSubmit={handleSubmit}>
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
          Submit
        </button>
      </form>

      {weatherData.length > 0 && (
        <div style={{ marginTop: '30px' }}>
          <h3>7-Day Weather Forecast for {city.charAt(0).toUpperCase() + city.slice(1)}</h3>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            textAlign: 'center'
          }}>
            <thead>
              <tr>
                <th style={thStyle}>Day</th>
                <th style={thStyle}>Weather</th>
                <th style={thStyle}>Probability</th>
                <th style={thStyle}>Temperature</th>
                <th style={thStyle}>Humidity</th>
              </tr>
            </thead>
            <tbody>
              {weatherData.map((item, index) => (
                <tr key={index}>
                  <td style={tdStyle}>{item.dayInfo}</td>
                  <td style={tdStyle}>{item.weather}</td>
                  <td style={tdStyle}>{item.probability}</td>
                  <td style={tdStyle}>{item.temp}</td>
                  <td style={tdStyle}>{item.humidity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

const thStyle = {
  border: '1px solid #ddd',
  padding: '8px',
  backgroundColor: '#4CAF50',
  color: 'white'
};

const tdStyle = {
  border: '1px solid #ddd',
  padding: '8px'
};

export default Weather;
