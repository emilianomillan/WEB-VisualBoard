import React from 'react'
import Masonry from 'react-masonry-css'
import ImageCard from './ImageCard'

function MasonryGrid({ items, onItemClick }) {
  const breakpointColumns = {
    default: 5,
    1400: 4,
    1100: 3,
    700: 2,
    500: 1
  }

  // Filtrar posts que no tienen is_active = false
  // El backend ya debería filtrarlos, pero agregamos esta capa adicional de seguridad
  const activeItems = items.filter(item => item.is_active !== false)

  return (
    <Masonry
      breakpointCols={breakpointColumns}
      className="masonry-grid"
      columnClassName="masonry-grid-column"
    >
      {activeItems.map(item => (
        <ImageCard 
          key={item.id} 
          item={item}
          onClick={() => onItemClick && onItemClick(item)}
        />
      ))}
    </Masonry>
  )
}

export default MasonryGrid