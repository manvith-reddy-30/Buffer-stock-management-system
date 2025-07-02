import { useState, useEffect } from 'react'
import './App.css'
import Admin from './pages/Admin/admin'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home/home'
import Predictions from './pages/Predictions/Predictions'
import Auth from './pages/Auth/Auth'

function App() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [])

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('user')
  }

  const handleSetUser = (userData) => {
    setUser(userData)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  if (!user) {
    return <Auth setUser={handleSetUser} />
  }

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px' }}>
        <span>Welcome, {user.name}</span>
        <button onClick={handleLogout}>Logout</button>
      </div>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/predictions" element={<Predictions />} />
      </Routes>
    </>
  )
}

export default App
