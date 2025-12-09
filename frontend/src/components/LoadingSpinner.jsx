import React from 'react'
import { Spinner } from 'react-bootstrap'

function LoadingSpinner({ text = 'Cargando...' }) {
  return (
    <div className="loading-spinner">
      <div className="text-center">
        <Spinner animation="border" variant="primary" />
        <p className="mt-2">{text}</p>
      </div>
    </div>
  )
}

export default LoadingSpinner