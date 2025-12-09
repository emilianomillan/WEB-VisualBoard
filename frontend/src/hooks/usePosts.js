import { useState, useEffect } from 'react'
import { postsAPI } from '../services/api'
import { cache } from '../utils/cache'

export const usePosts = (page = 1, useCache = true) => {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [pagination, setPagination] = useState({
    total: 0,
    totalPages: 0,
    currentPage: page,
    perPage: 20
  })

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true)
        setError(null)

        // 1. Primera carga: verificar si hay datos en localStorage
        const { posts: cachedPosts, timestamp } = cache.getCachedPosts()
        
        if (cachedPosts && cachedPosts.length > 0) {
          console.log('Primera carga: usando posts del caché')
          
          // Mostrar posts del caché inmediatamente
          const startIndex = (page - 1) * 20
          const endIndex = startIndex + 20
          const paginatedPosts = cachedPosts.slice(startIndex, endIndex)
          
          setPosts(paginatedPosts)
          setPagination({
            total: cachedPosts.length,
            totalPages: Math.ceil(cachedPosts.length / 20),
            currentPage: page,
            perPage: 20
          })
          
          // 2. Segunda carga: verificar si hay posts nuevos pasando el timestamp
          console.log('Verificando posts nuevos desde:', timestamp)
          const response = await postsAPI.getAll(1, 1000, timestamp) // Obtener todos los posts nuevos
          const newPosts = response.data.items
          
          if (newPosts && newPosts.length > 0) {
            console.log('Se encontraron', newPosts.length, 'posts nuevos')
            
            // 3. Combinar posts del caché con los nuevos
            const mergedPosts = cache.mergePosts(cachedPosts, newPosts)
            
            // 4. Guardar todos los posts actualizados en caché
            cache.savePosts(mergedPosts)
            
            // 5. Actualizar la vista con los posts paginados
            const newStartIndex = (page - 1) * 20
            const newEndIndex = newStartIndex + 20
            const newPaginatedPosts = mergedPosts.slice(newStartIndex, newEndIndex)
            
            setPosts(newPaginatedPosts)
            setPagination({
              total: mergedPosts.length,
              totalPages: Math.ceil(mergedPosts.length / 20),
              currentPage: page,
              perPage: 20
            })
          } else {
            console.log('No hay posts nuevos')
          }
        } else {
          // Primera vez: no hay caché, obtener todos los posts
          console.log('Sin caché: obteniendo todos los posts')
          const response = await postsAPI.getAll(page, 20)
          const data = response.data
          
          setPosts(data.items)
          setPagination({
            total: data.total,
            totalPages: data.total_pages,
            currentPage: data.page,
            perPage: data.per_page
          })
          
          // Guardar en caché si es la primera página
          if (page === 1 && data.items.length > 0) {
            // Obtener todos los posts para el caché
            const allPostsResponse = await postsAPI.getAll(1, 1000)
            cache.savePosts(allPostsResponse.data.items)
          }
        }
      } catch (err) {
        console.error('Error al cargar posts:', err)
        setError(err.message || 'Error al cargar los posts')
      } finally {
        setLoading(false)
      }
    }

    fetchPosts()
  }, [page, useCache])

  // Función para refrescar manualmente
  const refresh = async () => {
    cache.clear()
    window.location.reload()
  }

  return { posts, loading, error, pagination, refresh }
}