import React, { useState } from 'react'
import { Alert, Button, Form, Modal, Spinner } from 'react-bootstrap'
import axios from 'axios'
import { API_BASE_URL } from '../config/api'

function BrokenImageHandler({ post, onUpdate }) {
  const [showModal, setShowModal] = useState(false)
  const [newImageUrl, setNewImageUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleReactivate = async () => {
    if (!newImageUrl) {
      setError('Por favor ingresa una nueva URL de imagen')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const headers = {}
      const userId = sessionStorage.getItem('userId')
      if (userId) {
        headers['X-User-Id'] = userId
      }

      await axios.post(
        `${API_BASE_URL}/api/image-health/reactivate/${post.id}`,
        null,
        {
          params: { new_image_url: newImageUrl },
          headers
        }
      )

      // Actualizar la imagen en el frontend
      if (onUpdate) {
        onUpdate({ ...post, image_url: newImageUrl, is_active: true })
      }

      setShowModal(false)
      alert('¡Post reactivado exitosamente!')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al reactivar el post')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Alert variant="warning" className="mb-2">
        <div className="d-flex justify-content-between align-items-center">
          <div>
            <strong>⚠️ Imagen no disponible</strong>
            <p className="mb-0 small">La imagen de este post ya no está accesible</p>
          </div>
          {post.user_id === sessionStorage.getItem('userId') && (
            <Button 
              size="sm" 
              variant="warning"
              onClick={() => setShowModal(true)}
            >
              Actualizar Imagen
            </Button>
          )}
        </div>
      </Alert>

      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Actualizar Imagen del Post</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>La imagen original ya no está disponible:</p>
          <code className="text-danger small">{post.image_url}</code>
          
          <Form.Group className="mt-3">
            <Form.Label>Nueva URL de Imagen</Form.Label>
            <Form.Control
              type="url"
              placeholder="https://ejemplo.com/nueva-imagen.jpg"
              value={newImageUrl}
              onChange={(e) => setNewImageUrl(e.target.value)}
            />
          </Form.Group>

          {error && (
            <Alert variant="danger" className="mt-3">
              {error}
            </Alert>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Cancelar
          </Button>
          <Button 
            variant="primary" 
            onClick={handleReactivate}
            disabled={loading || !newImageUrl}
          >
            {loading ? (
              <>
                <Spinner size="sm" animation="border" className="me-2" />
                Actualizando...
              </>
            ) : (
              'Actualizar y Reactivar'
            )}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

export default BrokenImageHandler