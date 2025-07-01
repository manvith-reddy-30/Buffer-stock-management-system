import React, { useState } from 'react';

const CityForm = () => {
  const [formData, setFormData] = useState({
    city: '',
    date: '',
    price: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form Data:', formData);
    // Replace this console.log with your API call to send formData to backend
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="city">Select your city:</label>
        <select
          id="city"
          name="city"
          value={formData.city}
          onChange={handleChange}
          required
        >
          <option value="">--Select--</option>
          <option value="hyderabad">Hyderabad</option>
          <option value="medak">Medak</option>
          <option value="warangal">Warangal</option>
          <option value="rangareddy">Ranga Reddy</option>
          <option value="nalgonda">Nalgonda</option>
        </select>
      </div>

      <div>
        <label htmlFor="date">Select date:</label>
        <input
          type="date"
          id="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label htmlFor="price">Enter price:</label>
        <input
          type="number"
          id="price"
          name="price"
          value={formData.price}
          onChange={handleChange}
          required
          min="0"
          step="10"
        />
      </div>

      <br />
      <button type="submit">Submit</button>
    </form>
  );
};

export default CityForm;
