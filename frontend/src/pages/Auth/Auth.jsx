import React, { useState } from 'react'
import './Auth.css'

function Auth({ setUser }) {
  const [isLogin, setIsLogin] = useState(true)
  const [username, setUsername] = useState('')
  const [govt_id, setGovt_id] = useState('')
  const [password, setPassword] = useState('')
  const [user_type, setUser_type] = useState('')
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (isLogin) {
      // LOGIN FLOW
      const data = {
        govt_id: govt_id,
        password: password,
      }

      try {
        const response = await fetch(`${BACKEND_URL}/user/auth`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })

        if (response.ok) {
          const resData = await response.json()
          setUser({ name: resData.user.username }) 
        } else {
          alert("Wrong credentials")
        }
      } catch (error) {
        console.error("Server error:", error)
        alert("Server Error")
      }
    } else {
      // SIGNUP FLOW
      const data = {
        username: username,
        govt_id: parseInt(govt_id),
        password: password,
        user_type: user_type,
      }

      try {
        const response = await fetch(`${BACKEND_URL}/user/newUser`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })

        if (response.ok) {
            const resData = await response.json()
            setUser({ name: resData.user.username }) 
          } else if (response.status === 409) {
            const errData = await response.json()
            alert(errData.detail)
            setIsLogin(true)
          } else {
            alert("Signup failed")
          }
          
      } catch (error) {
        console.error("Server error:", error)
        alert("Server Error")
      }
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>{isLogin ? 'Login' : 'Sign Up'}</h2>
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required={!isLogin}
              />
            </>
          )}
          <input
            type="text"
            placeholder="Govt ID"
            value={govt_id}
            onChange={(e) => setGovt_id(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {!isLogin && (
            <>
              <input
                type="text"
                placeholder="User Type"
                value={user_type}
                onChange={(e) => setUser_type(e.target.value)}
                required={!isLogin}
              />
            </>
          )}
          <button type="submit">{isLogin ? 'Login' : 'Sign Up'}</button>
        </form>
        <p onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? "Don't have an account? Sign up" : "Already have an account? Login"}
        </p>
      </div>
    </div>
  )
}

export default Auth
