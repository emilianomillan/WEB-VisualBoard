import React from 'react'
import { Modal, Button, Badge } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { API_BASE_URL } from '../config/api'

function PostDetailModal({ show, onHide, post, currentUser }) {
  const navigate = useNavigate()
  
  if (!post) return null

  const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString('es-MX', { 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const isOwner = currentUser && post.author === currentUser

  const handleEdit = () => {
    onHide()
    navigate(`/edit/${post.id}`)
  }

  const handleDelete = async () => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este post?')) {
      try {
        const response = await fetch(`${API_BASE_URL}/api/posts/${post.id}`, {
          method: 'DELETE',
          headers: {
            'X-User-Id': currentUser
          }
        })

        if (response.ok) {
          alert('Post eliminado exitosamente')
          onHide()
          window.location.reload()
        } else {
          alert('No tienes permiso para eliminar este post')
        }
      } catch (error) {
        console.error('Error al eliminar post:', error)
        alert('Error al eliminar el post')
      }
    }
  }

  return (
    <Modal show={show} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>{post.title || 'Detalle del Post'}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <img 
          src={post.image_url} 
          alt={post.title || 'Visual Board Image'} 
          className="w-100 mb-3 rounded"
        />
        
        {post.id && (
          <p className="text-muted small">ID: {post.id}</p>
        )}
        
        {post.description && (
          <p className="mb-3">{post.description}</p>
        )}
        
        <div className="mb-3">
          <strong>Autor:</strong> {post.author || 'Anónimo'}
        </div>
        
        {post.created_at && (
          <div className="mb-3">
            <strong>Fecha de creación:</strong> {formatDate(post.created_at)}
          </div>
        )}
        
        {post.tags && post.tags.length > 0 && (
          <div className="mb-3">
            <strong>Etiquetas:</strong>
            <div className="mt-2">
              {post.tags.map((tag, index) => (
                <Badge key={index} bg="secondary" className="me-2">
                  {tag}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </Modal.Body>
      <Modal.Footer>
        {isOwner && (
          <>
            <Button variant="warning" onClick={handleEdit}>
              ✏️ Editar
            </Button>
            <Button variant="danger" onClick={handleDelete}>
              🗑️ Eliminar
            </Button>
          </>
        )}
        <Button variant="secondary" onClick={onHide}>
          Cerrar
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

export default PostDetailModal