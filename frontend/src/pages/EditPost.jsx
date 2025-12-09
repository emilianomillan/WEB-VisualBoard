import React, { useState, useEffect } from 'react'
import { Container, Form, Button, Card, Alert, ButtonGroup, Spinner } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router-dom'
import { postsAPI } from '../services/api'
import { cache } from '../utils/cache'
import LoadingSpinner from '../components/LoadingSpinner'
import axios from 'axios'
import { API_BASE_URL } from '../config/api'

function EditPost() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)
  const [currentUser, setCurrentUser] = useState(null)
  const [originalPost, setOriginalPost] = useState(null)
  const [updateMode, setUpdateMode] = useState('patch') // 'patch' o 'put'
  const [imageMode, setImageMode] = useState('url') // 'url' o 'upload'
  const [previewUrl, setPreviewUrl] = useState('')
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    image_url: '',
    tags: '',
    image_file: null
  })

  useEffect(() => {
    const user = sessionStorage.getItem('userId')
    if (!user) {
      alert('Debes iniciar sesión para editar posts')
      navigate('/')
    }
    setCurrentUser(user)
    fetchPost()
  }, [id])

  const fetchPost = async () => {
    try {
      const response = await postsAPI.getById(id)
      const post = response.data
      
      // Verificar que el usuario sea el autor
      const currentUserId = sessionStorage.getItem('userId')
      if (post.author !== currentUserId) {
        alert('No tienes permiso para editar este post')
        navigate('/my-posts')
        return
      }
      
      setOriginalPost(post)
      setFormData({
        title: post.title || '',
        description: post.description || '',
        image_url: post.image_url || '',
        tags: post.tags ? post.tags.join(', ') : '',
        image_file: null
      })
      setPreviewUrl(post.image_url || '')
    } catch (error) {
      setError('Error al cargar el post')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    
    // Actualizar preview si es URL
    if (name === 'image_url' && imageMode === 'url') {
      setPreviewUrl(value)
    }
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      // Validar tipo de archivo
      const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
      if (!validTypes.includes(file.type)) {
        setError('Tipo de archivo no válido. Solo se permiten: JPG, PNG, GIF, WebP')
        return
      }
      
      // Validar tamaño (máx 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('El archivo es demasiado grande. Máximo 10MB')
        return
      }
      
      setFormData(prev => ({
        ...prev,
        image_file: file
      }))
      
      // Crear preview local
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreviewUrl(reader.result)
      }
      reader.readAsDataURL(file)
      setError(null)
    }
  }

  const uploadImage = async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      setUploading(true)
      const response = await axios.post(`${API_BASE_URL}/api/upload/image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data.image_url
    } catch (error) {
      console.error('Error al subir imagen:', error)
      throw new Error('Error al subir la imagen')
    } finally {
      setUploading(false)
    }
  }

  const handleModeChange = (mode) => {
    setImageMode(mode)
    if (mode === 'url') {
      // Si cambiamos a URL, restaurar la URL original
      setPreviewUrl(originalPost?.image_url || '')
      setFormData(prev => ({
        ...prev,
        image_url: originalPost?.image_url || '',
        image_file: null
      }))
    } else {
      // Si cambiamos a upload, limpiar preview
      setPreviewUrl('')
      setFormData(prev => ({
        ...prev,
        image_file: null
      }))
    }
    setError(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    let finalImageUrl = formData.image_url
    
    // Validar según el modo de imagen
    if (imageMode === 'url') {
      if (updateMode === 'put' && !formData.image_url) {
        setError('Para reemplazo completo, la URL de la imagen es requerida')
        return
      }
    } else {
      // Si estamos en modo upload y no hay archivo, pero es PATCH, no es error
      if (updateMode === 'put' && !formData.image_file && !originalPost?.image_url) {
        setError('Debes seleccionar una imagen')
        return
      }
    }
    
    // Para PUT, el título es requerido
    if (updateMode === 'put' && !formData.title) {
      setError('Para reemplazo completo, el título es requerido')
      return
    }

    try {
      setSaving(true)
      setError(null)
      
      // Si es modo upload y hay un archivo nuevo, subirlo
      if (imageMode === 'upload' && formData.image_file) {
        finalImageUrl = await uploadImage(formData.image_file)
      } else if (imageMode === 'upload' && !formData.image_file) {
        // En modo upload sin archivo nuevo, mantener la URL original
        finalImageUrl = originalPost?.image_url || ''
      }
      
      const tags = formData.tags
        ? formData.tags.split(',').map(tag => tag.trim()).filter(Boolean)
        : []
      
      if (updateMode === 'patch') {
        // PATCH: Enviar solo campos modificados
        const changedFields = {}
        if (formData.title !== originalPost.title) changedFields.title = formData.title
        if (formData.description !== originalPost.description) changedFields.description = formData.description
        if (finalImageUrl !== originalPost.image_url) changedFields.image_url = finalImageUrl
        if (JSON.stringify(tags) !== JSON.stringify(originalPost.tags || [])) changedFields.tags = tags
        
        if (Object.keys(changedFields).length === 0) {
          alert('No hay cambios para guardar')
          setSaving(false)
          return
        }
        
        await postsAPI.partialUpdate(id, changedFields)
      } else {
        // PUT: Enviar todos los campos
        const dataToSend = {
          title: formData.title,
          description: formData.description,
          image_url: finalImageUrl,
          tags
        }
        await postsAPI.update(id, dataToSend)
      }
      
      cache.clear() // Limpiar caché para reflejar cambios
      alert(`Post ${updateMode === 'patch' ? 'actualizado' : 'reemplazado'} exitosamente`)
      navigate('/my-posts')
    } catch (error) {
      setError(`Error al ${updateMode === 'patch' ? 'actualizar' : 'reemplazar'} el post. ${error.response?.data?.detail || error.message || ''}`)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <Container className="py-4">
      <Card className="mx-auto" style={{ maxWidth: '600px' }}>
        <Card.Body>
          <h2 className="mb-4">Editar Post</h2>
          
          <Form.Group className="mb-3">
            <Form.Label>Tipo de actualización:</Form.Label>
            <div>
              <Form.Check
                inline
                type="radio"
                id="patch"
                label="Actualización parcial (PATCH) - Solo campos modificados"
                checked={updateMode === 'patch'}
                onChange={() => setUpdateMode('patch')}
              />
              <Form.Check
                inline
                type="radio"
                id="put"
                label="Reemplazo completo (PUT) - Todos los campos"
                checked={updateMode === 'put'}
                onChange={() => setUpdateMode('put')}
              />
            </div>
          </Form.Group>
          
          {error && (
            <Alert variant="danger" dismissible onClose={() => setError(null)}>
              {error}
            </Alert>
          )}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Título *</Form.Label>
              <Form.Control
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="Ej: Atardecer en la playa"
                required
                maxLength={200}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Imagen *</Form.Label>
              <ButtonGroup className="d-block mb-3">
                <Button
                  variant={imageMode === 'url' ? 'primary' : 'outline-primary'}
                  onClick={() => handleModeChange('url')}
                  size="sm"
                >
                  📎 URL de Internet
                </Button>
                <Button
                  variant={imageMode === 'upload' ? 'primary' : 'outline-primary'}
                  onClick={() => handleModeChange('upload')}
                  size="sm"
                >
                  📁 Subir Nueva Imagen
                </Button>
              </ButtonGroup>

              {imageMode === 'url' ? (
                <Form.Control
                  type="url"
                  name="image_url"
                  value={formData.image_url}
                  onChange={handleChange}
                  placeholder="https://ejemplo.com/imagen.jpg"
                  required={updateMode === 'put'}
                />
              ) : (
                <>
                  <Form.Control
                    type="file"
                    accept="image/jpeg,image/png,image/gif,image/webp"
                    onChange={handleFileChange}
                    required={updateMode === 'put' && !originalPost?.image_url}
                  />
                  <Form.Text className="text-muted">
                    Formatos permitidos: JPG, PNG, GIF, WebP. Máximo 10MB
                    {originalPost?.image_url && !formData.image_file && (
                      <><br />Imagen actual se mantendrá si no seleccionas una nueva</>
                    )}
                  </Form.Text>
                </>
              )}
            </Form.Group>

            {previewUrl && (
              <div className="mb-3">
                <Form.Label>Vista previa:</Form.Label>
                <div className="border rounded p-2">
                  <img 
                    src={previewUrl} 
                    alt="Vista previa"
                    className="w-100"
                    style={{ maxHeight: '300px', objectFit: 'contain' }}
                    onError={(e) => {
                      if (imageMode === 'url') {
                        e.target.style.display = 'none'
                        setError('No se pudo cargar la imagen. Verifica la URL.')
                      }
                    }}
                    onLoad={(e) => {
                      e.target.style.display = 'block'
                      if (imageMode === 'url') {
                        setError(null)
                      }
                    }}
                  />
                </div>
              </div>
            )}

            <Form.Group className="mb-3">
              <Form.Label>Descripción</Form.Label>
              <Form.Control
                as="textarea"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe tu imagen..."
                rows={3}
              />
            </Form.Group>

            <Form.Group className="mb-4">
              <Form.Label>Etiquetas</Form.Label>
              <Form.Control
                type="text"
                name="tags"
                value={formData.tags}
                onChange={handleChange}
                placeholder="naturaleza, playa, atardecer"
              />
              <Form.Text className="text-muted">
                Separa las etiquetas con comas
              </Form.Text>
            </Form.Group>

            <div className="d-grid gap-2">
              <Button 
                variant="primary" 
                type="submit"
                disabled={saving || uploading}
                size="lg"
              >
                {uploading ? (
                  <>
                    <Spinner size="sm" animation="border" className="me-2" />
                    Subiendo imagen...
                  </>
                ) : saving ? (
                  <>
                    <Spinner size="sm" animation="border" className="me-2" />
                    Guardando cambios...
                  </>
                ) : (
                  'Guardar Cambios'
                )}
              </Button>
              <Button 
                variant="outline-secondary" 
                onClick={() => navigate('/my-posts')}
                disabled={saving || uploading}
              >
                Cancelar
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  )
}

export default EditPost