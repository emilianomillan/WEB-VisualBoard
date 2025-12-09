import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Navbar, Nav, Container, Button } from 'react-bootstrap'
import UserAuth from './UserAuth'
import ImageHealthChecker from './ImageHealthChecker'

function Navigation() {
  const location = useLocation()
  const [showHealthChecker, setShowHealthChecker] = useState(false)
  
  return (
    <header>
      <Navbar bg="dark" variant="dark" expand="lg" className="navbar-custom mb-4">
        <Container>
          <Navbar.Brand as={Link} to="/">
            📌 Visual Board
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link 
                as={Link} 
                to="/" 
                active={location.pathname === '/'}
              >
                Inicio
              </Nav.Link>
              <Nav.Link 
                as={Link} 
                to="/discover" 
                active={location.pathname === '/discover'}
              >
                Descubrir
              </Nav.Link>
              <Nav.Link 
                as={Link} 
                to="/my-posts" 
                active={location.pathname === '/my-posts'}
              >
                Mis Posts
              </Nav.Link>
            </Nav>
            <Nav className="align-items-center gap-3">
              <Button 
                variant="outline-warning" 
                size="sm"
                onClick={() => setShowHealthChecker(true)}
                title="Verificar salud de imágenes"
              >
                🔍 Verificar Imágenes
              </Button>
              <UserAuth />
              <Nav.Link as={Link} to="/create" className="btn btn-light text-primary px-3">
                + Crear Post
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      
      <ImageHealthChecker 
        show={showHealthChecker} 
        onHide={() => setShowHealthChecker(false)}
        userOnly={false}
      />
    </header>
  )
}

export default Navigation