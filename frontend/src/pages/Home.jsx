import React, { useState, useEffect } from 'react'
import { Container, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import MasonryGrid from '../components/MasonryGrid'
import PostDetailModal from '../components/PostDetailModal'
import LoadingSpinner from '../components/LoadingSpinner'
import EmptyState from '../components/EmptyState'
import { usePosts } from '../hooks/usePosts'

function Home() {
  const [page, setPage] = useState(1)
  const [selectedPost, setSelectedPost] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [currentUser, setCurrentUser] = useState(null)
  const { posts, loading, error, pagination } = usePosts(page)

  useEffect(() => {
    const user = sessionStorage.getItem('userId')
    setCurrentUser(user)
  }, [])

  const handlePostClick = (post) => {
    setSelectedPost(post)
    setShowModal(true)
  }

  const handleCloseModal = () => {
    setShowModal(false)
    setSelectedPost(null)
  }

  if (loading) return <LoadingSpinner />
  
  if (error) {
    return (
      <Container>
        <EmptyState 
          title="Error al cargar" 
          message={error}
        />
      </Container>
    )
  }

  return (
    <Container fluid>
      <section>
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h2>Todos los Posts</h2>
          <Button as={Link} to="/create" variant="primary">
            + Crear Post
          </Button>
        </div>

        {posts.length === 0 ? (
          <EmptyState 
            title="No hay posts todavía"
            message="Sé el primero en compartir contenido visual"
            showCreateButton
          />
        ) : (
          <>
            <MasonryGrid items={posts} onItemClick={handlePostClick} />
            
            {pagination.totalPages > 1 && (
              <div className="d-flex justify-content-center mt-4 gap-2">
                <Button
                  variant="outline-primary"
                  disabled={page === 1}
                  onClick={() => setPage(page - 1)}
                >
                  Anterior
                </Button>
                <span className="align-self-center">
                  Página {page} de {pagination.totalPages}
                </span>
                <Button
                  variant="outline-primary"
                  disabled={page === pagination.totalPages}
                  onClick={() => setPage(page + 1)}
                >
                  Siguiente
                </Button>
              </div>
            )}
          </>
        )}
      </section>

      <PostDetailModal 
        show={showModal}
        onHide={handleCloseModal}
        post={selectedPost}
        currentUser={currentUser}
      />

      <Link to="/create">
        <button className="floating-btn">
          +
        </button>
      </Link>
    </Container>
  )
}

export default Home