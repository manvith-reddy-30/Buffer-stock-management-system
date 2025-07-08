import React, { useState } from 'react';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css'; // Import Toastify CSS
import './CityForm.css';

const CityForm = () => {
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  const [formData, setFormData] = useState({
    city: '',
    date: '',
    price: ''
  });

  const [bufferFormData, setBufferFormData] = useState({
    city: '',
    date: '',
    buffer_quantity: ''
  });

  // Handle input changes for price form
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Handle input changes for buffer form
  const handleBufferChange = (e) => {
    setBufferFormData({
      ...bufferFormData,
      [e.target.name]: e.target.value
    });
  };

  // Submit price data
  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      date: formData.date,
      price: parseFloat(formData.price),
    };

    try {
      const response = await fetch(`${BACKEND_URL}/admin/${formData.city}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        toast.success("✅ Daily Price Data Submitted Successfully!");
        setFormData({ city: '', date: '', price: '' }); // clear form
      } else if (response.status === 409) {
        const resData = await response.json();
        toast.error(resData.detail || "❌ Daily Price Entry already exists for this date and city.");
      } else {
        toast.error("❌ Daily Price Submission Failed. Please try again.");
      }
    } catch (error) {
      console.error("Error submitting price:", error);
      toast.error("❌ Daily Price Server Error. Please try again later.");
    }
  };

  // Submit buffer quantity data
  const handleBufferSubmit = async (e) => {
    e.preventDefault();

    const data = {
      city: bufferFormData.city,
      user_type: "tomato",
      last_modified_date: bufferFormData.date,
      quantity: parseFloat(bufferFormData.buffer_quantity),
    };

    try {
      const response = await fetch(`${BACKEND_URL}/admin/buffer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        toast.success("✅ Buffer Quantity Data Submitted Successfully!");
        setBufferFormData({ city: '', date: '', buffer_quantity: '' }); // clear form
      } else if (response.status === 409) {
        const resData = await response.json();
        toast.error(resData.detail || "❌ Buffer Quantity Entry already exists for this date and city.");
      } else {
        toast.error("❌ Buffer Quantity Submission Failed. Please try again.");
      }
    } catch (error) {
      console.error("Error submitting buffer:", error);
      toast.error("❌ Buffer Quantity Server Error. Please try again later.");
    }
  };

  return (
    <div className="city-form-container">

      {/* Price Form */}
      <form onSubmit={handleSubmit} className="form-card">
        <h2 className="form-title">Enter Daily Price Data</h2>

        <div className="form-group">
          <label htmlFor="city-price">Select City:</label>
          <select
            id="city-price"
            name="city"
            value={formData.city}
            onChange={handleChange}
            required
            className="form-control"
          >
            <option value="">-- Select City --</option>
            <option value="hyderabad">Hyderabad</option>
            <option value="medak">Medak</option>
            <option value="warangal">Warangal</option>
            <option value="rangareddy">Ranga Reddy</option>
            <option value="nalgonda">Nalgonda</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="date-price">Select Date:</label>
          <input
            type="date"
            id="date-price"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
            className="form-control"
          />
        </div>

        <div className="form-group">
          <label htmlFor="price">Enter Price (INR):</label>
          <input
            type="number"
            id="price"
            name="price"
            value={formData.price}
            onChange={handleChange}
            required
            min="0"
            step="1"
            className="form-control"
            placeholder="e.g., 500"
          />
        </div>

        <button type="submit" className="submit-button">Submit Price</button>
      </form>

      {/* Buffer Quantity Form */}
      <form onSubmit={handleBufferSubmit} className="form-card">
        <h2 className="form-title">Enter Buffer Quantity Data</h2>

        <div className="form-group">
          <label htmlFor="city-buffer">Select City:</label>
          <select
            id="city-buffer"
            name="city"
            value={bufferFormData.city}
            onChange={handleBufferChange}
            required
            className="form-control"
          >
            <option value="">-- Select City --</option>
            <option value="hyderabad">Hyderabad</option>
            <option value="medak">Medak</option>
            <option value="warangal">Warangal</option>
            <option value="rangareddy">Ranga Reddy</option>
            <option value="nalgonda">Nalgonda</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="date-buffer">Select Date:</label>
          <input
            type="date"
            id="date-buffer"
            name="date"
            value={bufferFormData.date}
            onChange={handleBufferChange}
            required
            className="form-control"
          />
        </div>

        <div className="form-group">
          <label htmlFor="buffer_quantity">Enter Buffer Quantity (Tons):</label>
          <input
            type="number"
            id="buffer_quantity"
            name="buffer_quantity"
            value={bufferFormData.buffer_quantity}
            onChange={handleBufferChange}
            required
            min="0"
            step="1"
            className="form-control"
            placeholder="e.g., 100"
          />
        </div>

        <button type="submit" className="submit-button">Submit Buffer Quantity</button>
      </form>
    </div>
  );
};

export default CityForm;
