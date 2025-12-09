import React, { useState } from 'react'
import { Button, Modal, Alert, Spinner, Badge, ProgressBar } from 'react-bootstrap'
import axios from 'axios'
import { cache } from '../utils/cache'
import { API_BASE_URL } from '../config/api'

function ImageHealthChecker({ show, onHide, userOnly = false }) {
  const [checking, setChecking] = useState(false)
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)

  const checkImages = async () => {
    setChecking(true)
    setError(null)
    
    try {
      // Iniciar verificación en segundo plano
      const headers = {}
      if (userOnly) {
        const userId = sessionStorage.getItem('userId')
        if (userId) {
          headers['X-User-Id'] = userId
        }
      }

      const response = await axios.post(
        `${API_BASE_URL}/api/image-health/check`,
        {},
        { headers }
      )

      // Obtener estado actual
      const statusResponse = await axios.get(`${API_BASE_URL}/api/image-health/status`)
      setStatus(statusResponse.data)

      // Esperar un poco para que el proceso en segundo plano avance
      setTimeout(async () => {
        const finalStatus = await axios.get(`${API_BASE_URL}/api/image-health/status`)
        setStatus(finalStatus.data)
        setChecking(false)
        
        // Si se desactivaron posts, limpiar el caché para forzar recarga
        if (finalStatus.data.inactive_posts > 0) {
          console.log('Posts inactivos detectados, limpiando caché...')
          cache.clear()
          // Recargar la página después de un breve delay
          setTimeout(() => {
            window.location.reload()
          }, 1000)
        }
      }, 2000)

    } catch (err) {
      setError('Error al verificar imágenes')
      setChecking(false)
    }
  }

  const getHealthColor = (percentage) => {
    if (percentage >= 90) return 'success'
    if (percentage >= 70) return 'warning'
    return 'danger'
  }

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>
          🔍 Verificación de Salud de Imágenes
        </Modal.Title>
      </Modal.Header>
      
      <Modal.Body>
        {error && (
          <Alert variant="danger" dismissible onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {status && (
          <div className="mb-3">
            <h6>Estado Actual del Sistema:</h6>
            <div className="d-flex justify-content-between mb-2">
              <span>Posts Activos:</span>
              <Badge bg="success">{status.active_posts}</Badge>
            </div>
            <div className="d-flex justify-content-between mb-2">
              <span>Posts Inactivos:</span>
              <Badge bg="danger">{status.inactive_posts}</Badge>
            </div>
            <div className="d-flex justify-content-between mb-2">
              <span>Sin Verificar:</span>
              <Badge bg="warning">{status.unchecked_posts}</Badge>
            </div>
            <div className="mt-3">
              <label>Salud General:</label>
              <ProgressBar 
                now={status.health_percentage} 
                variant={getHealthColor(status.health_percentage)}
                label={`${status.health_percentage}%`}
              />
            </div>
          </div>
        )}

        <div className="text-muted small mt-3">
          <p>
            Esta herramienta verifica la disponibilidad de las imágenes en todos los posts.
            Los posts con imágenes no disponibles serán marcados como inactivos automáticamente.
          </p>
          {userOnly && (
            <p className="text-info">
              <strong>Modo Usuario:</strong> Solo se verificarán tus propios posts.
            </p>
          )}
        </div>
      </Modal.Body>
      
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Cerrar
        </Button>
        <Button 
          variant="primary" 
          onClick={checkImages}
          disabled={checking}
        >
          {checking ? (
            <>
              <Spinner size="sm" animation="border" className="me-2" />
              Verificando...
            </>
          ) : (
            <>🔍 Iniciar Verificación</>
          )}
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

export default ImageHealthChecker