import React, { useState, useEffect } from 'react'
import { Container, Button, Modal } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom'
import MasonryGrid from '../components/MasonryGrid'
import LoadingSpinner from '../components/LoadingSpinner'
import EmptyState from '../components/EmptyState'
import { postsAPI } from '../services/api'
import { cache } from '../utils/cache'

function MyPosts() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedPost, setSelectedPost] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const navigate = useNavigate()

  const fetchMyPosts = async () => {
    try {
      setLoading(true)
      const response = await postsAPI.getMyPosts()
      setPosts(response.data.items)
    } catch (error) {
      console.error('Error fetching my posts:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMyPosts()
  }, [])

  const handleDelete = async () => {
    if (selectedPost) {
      try {
        await postsAPI.delete(selectedPost.id)
        setPosts(posts.filter(p => p.id !== selectedPost.id))
        cache.clear() // Limpiar caché para reflejar cambios
        setShowModal(false)
        setSelectedPost(null)
      } catch (error) {
        alert('Error al eliminar el post')
      }
    }
  }

  const handlePostClick = (post) => {
    setSelectedPost(post)
    setShowModal(true)
  }

  if (loading) return <LoadingSpinner />

  return (
    <Container fluid>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Mis Posts</h2>
        <Button as={Link} to="/create" variant="primary">
          + Crear Post
        </Button>
      </div>

      {posts.length === 0 ? (
        <EmptyState 
          title="No tienes posts aún"
          message="Crea tu primer post y compártelo con el mundo"
          showCreateButton
        />
      ) : (
        <MasonryGrid items={posts} onItemClick={handlePostClick} />
      )}

      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>{selectedPost?.title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedPost && (
            <>
              <img 
                src={selectedPost.image_url} 
                alt={selectedPost.title}
                className="w-100 mb-3"
                style={{ borderRadius: '8px' }}
              />
              {selectedPost.description && (
                <p>{selectedPost.description}</p>
              )}
              {selectedPost.tags && selectedPost.tags.length > 0 && (
                <div>
                  {selectedPost.tags.map((tag, index) => (
                    <span key={index} className="tag-badge me-1">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button 
            variant="outline-primary" 
            onClick={() => {
              setShowModal(false)
              navigate(`/edit/${selectedPost.id}`)
            }}
          >
            Editar
          </Button>
          <Button variant="danger" onClick={handleDelete}>
            Eliminar
          </Button>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  )
}

export default MyPosts