import React from 'react'
import CityForm from '../../components/CityForm'
import './admin.css' 

const Admin = () => {
  return (
    <div className="admin-container">
      <h1 className="admin-title">This is admin page</h1>
      <div className='predictions-form-container'>
       <CityForm />
      </div>

    </div>
  )
}

export default Admin