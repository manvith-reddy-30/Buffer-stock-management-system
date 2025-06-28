import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Admin from './pages/Admin/Admin'
import { Link, Routes,Route } from 'react-router-dom'
import Home from './pages/Home/home'
import Predictions from './pages/Predictions/Predictions'

function App() {
  

  return (
    <>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/admin" element={<Admin/>} />
        <Route path="/predictions" element={<Predictions/>} />
      </Routes>
    </>
  )
}

export default App
