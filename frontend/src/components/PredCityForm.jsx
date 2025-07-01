import React, { useState } from 'react';

const PredCityForm = () => {
    const [city, setCity] = useState('');

    const handleSubmit = (e) => {
      e.preventDefault();
      console.log('Selected city:', city);
      // You can send `city` to your backend here using fetch or axios
    };
  
    return (
      <form onSubmit={handleSubmit}>
        <label htmlFor="city">Select your city:</label>
        <select
          id="city"
          name="city"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          required
        >
          <option value="">--Select--</option>
          <option value="hyderabad">Hyderabad</option>
          <option value="medak">Medak</option>
          <option value="warangal">Warangal</option>
          <option value="rangareddy">Ranga Reddy</option>
          <option value="nalgonda">Nalgonda</option>
        </select>
        <br /><br />
        <button type="submit">Submit</button>
      </form>
    );
}

export default PredCityForm
