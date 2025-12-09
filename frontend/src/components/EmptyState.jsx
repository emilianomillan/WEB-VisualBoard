import React from 'react'
import { Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'

function EmptyState({ 
  title = 'No hay contenido', 
  message = 'No se encontraron elementos para mostrar',
  showCreateButton = false
}) {
  return (
    <div className="empty-state">
      <h3>{title}</h3>
      <p>{message}</p>
      {showCreateButton && (
        <Button as={Link} to="/create" variant="primary" className="mt-3">
          Crear mi primer post
        </Button>
      )}
    </div>
  )
}

export default EmptyState