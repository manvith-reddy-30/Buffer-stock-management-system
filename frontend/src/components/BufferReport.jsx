import React, { useState } from 'react';

const BufferReport = () => {
  const [city, setCity] = useState('');
  const [report, setReport] = useState('');
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${BACKEND_URL}/analyst/buffer/report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ city }),
      });

      if (response.ok) {
        const data = await response.json();
        setReport(data.buffer_stock_report);
      } else {
        setReport('Failed to fetch report. Please try again.');
      }
    } catch (error) {
      console.error('Error fetching buffer report:', error);
      setReport('Error fetching report.');
    }
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

      {report && (
        <div
          style={{
            marginTop: '30px',
            whiteSpace: 'pre-wrap',
            background: '#f9f9f9',
            padding: '20px',
            borderRadius: '8px',
            border: '1px solid #ccc',
          }}
        >
          <h2>Buffer Stock Report</h2>
          <div dangerouslySetInnerHTML={{ __html: report.replace(/\n/g, '<br/>') }} />
        </div>
      )}
    </div>
  );
};

export default BufferReport;
