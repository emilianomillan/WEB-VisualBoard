import React, { useState, useEffect } from 'react'
import { Container, Button, Alert } from 'react-bootstrap'
import MasonryGrid from '../components/MasonryGrid'
import LoadingSpinner from '../components/LoadingSpinner'
import { discoverAPI } from '../services/api'

function Discover() {
  const [images, setImages] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchDiscoverContent = async () => {
    try {
      setLoading(true)
      setError(null)
      console.log('Fetching discover content...')
      
      const response = await discoverAPI.getRandom(30)
      console.log('Discover response:', response)
      
      // La respuesta ya viene como un array directo
      if (response.data && Array.isArray(response.data)) {
        console.log('Setting images:', response.data.length, 'images')
        setImages(response.data)
      } else {
        console.error('Unexpected response format:', response)
        setImages([])
        setError('Formato de respuesta inesperado')
      }
    } catch (err) {
      console.error('Error al cargar discover:', err)
      setError(`Error: ${err.message}`)
      setImages([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDiscoverContent()
  }, [])

  const handleRefresh = () => {
    fetchDiscoverContent()
  }

  const handleImageClick = (item) => {
    if (item.author_url) {
      window.open(item.author_url, '_blank')
    }
  }

  if (loading) {
    return <LoadingSpinner />
  }

  return (
    <Container fluid>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2>Descubrir</h2>
          <p className="text-muted">
            Contenido aleatorio de Unsplash para inspirarte
            {images.length > 0 && ` - ${images.length} imágenes cargadas`}
          </p>
        </div>
        <Button variant="outline-primary" onClick={handleRefresh}>
          🔄 Refrescar
        </Button>
      </div>

      {error && (
        <Alert variant="danger" dismissible onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {images.length === 0 && !error && !loading && (
        <Alert variant="warning">
          No se encontraron imágenes. Intenta refrescar.
        </Alert>
      )}

      {images.length > 0 && (
        <MasonryGrid 
          items={images} 
          onItemClick={handleImageClick}
        />
      )}
    </Container>
  )
}

export default Discover