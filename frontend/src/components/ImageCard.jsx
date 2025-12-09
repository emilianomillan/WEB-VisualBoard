import React from 'react'
import { Card } from 'react-bootstrap'

function ImageCard({ item, onClick }) {
  const { title, image_url, description, tags, author, created_at } = item

  const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    return date.toLocaleDateString('es-MX', { 
      day: 'numeric', 
      month: 'short', 
      year: 'numeric' 
    })
  }

  return (
    <Card className="image-card" onClick={onClick}>
      <Card.Img variant="top" src={image_url} alt={title || 'Visual Board Image'} />
      <div className="image-card-overlay">
        {title && <h6 className="mb-1">{title}</h6>}
        {description && (
          <p className="small mb-1 text-truncate">
            {description}
          </p>
        )}
        <div className="d-flex justify-content-between align-items-center">
          {author && (
            <p className="small mb-0">Por: {author}</p>
          )}
          {created_at && (
            <p className="small mb-0">{formatDate(created_at)}</p>
          )}
        </div>
        {tags && tags.length > 0 && (
          <div className="mt-2">
            {tags.slice(0, 3).map((tag, index) => (
              <span key={index} className="tag-badge me-1">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </Card>
  )
}

export default ImageCard