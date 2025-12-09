import React, { useState, useEffect } from 'react'
import { Form, Button, InputGroup } from 'react-bootstrap'

function UserLogin() {
  const [username, setUsername] = useState('')
  const [currentUser, setCurrentUser] = useState(null)

  useEffect(() => {
    // Cargar usuario desde sessionStorage al montar
    const storedUser = sessionStorage.getItem('userId')
    if (storedUser) {
      setCurrentUser(storedUser)
    }
  }, [])

  const handleLogin = (e) => {
    e.preventDefault()
    if (username.trim()) {
      sessionStorage.setItem('userId', username.trim())
      setCurrentUser(username.trim())
      setUsername('')
      window.location.reload() // Recargar para actualizar los headers
    }
  }

  const handleLogout = () => {
    sessionStorage.removeItem('userId')
    setCurrentUser(null)
    window.location.reload()
  }

  if (currentUser) {
    return (
      <div className="d-flex align-items-center gap-2 text-white">
        <span>👤 {currentUser}</span>
        <Button size="sm" variant="outline-light" onClick={handleLogout}>
          Cerrar Sesión
        </Button>
      </div>
    )
  }

  return (
    <Form onSubmit={handleLogin} className="d-flex">
      <InputGroup size="sm">
        <Form.Control
          type="text"
          placeholder="Tu nombre de usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <Button type="submit" variant="light">
          Ingresar
        </Button>
      </InputGroup>
    </Form>
  )
}

export default UserLogin