const POSTS_CACHE_KEY = 'visual_board_posts'
const TIMESTAMP_KEY = 'visual_board_timestamp'
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutos

export const cache = {
  // Guardar posts en localStorage con timestamp
  savePosts: (posts) => {
    const timestamp = new Date().toISOString()
    try {
      localStorage.setItem(POSTS_CACHE_KEY, JSON.stringify(posts))
      localStorage.setItem(TIMESTAMP_KEY, timestamp)
      console.log('Posts guardados en caché:', posts.length, 'timestamp:', timestamp)
      return timestamp
    } catch (error) {
      console.error('Error guardando en caché:', error)
      return null
    }
  },

  // Obtener posts del caché
  getCachedPosts: () => {
    try {
      const posts = localStorage.getItem(POSTS_CACHE_KEY)
      const timestamp = localStorage.getItem(TIMESTAMP_KEY)
      
      if (!posts || !timestamp) {
        console.log('No hay posts en caché')
        return { posts: null, timestamp: null }
      }
      
      console.log('Posts encontrados en caché, timestamp:', timestamp)
      return {
        posts: JSON.parse(posts),
        timestamp: timestamp
      }
    } catch (error) {
      console.error('Error al leer caché:', error)
      return { posts: null, timestamp: null }
    }
  },

  // Obtener el timestamp del último caché
  getTimestamp: () => {
    const timestamp = localStorage.getItem(TIMESTAMP_KEY)
    console.log('Timestamp del caché:', timestamp)
    return timestamp
  },

  // Combinar posts del caché con nuevos posts
  mergePosts: (cachedPosts, newPosts) => {
    const postsMap = new Map()
    
    // Primero añadir posts del caché
    if (cachedPosts && Array.isArray(cachedPosts)) {
      cachedPosts.forEach(post => {
        postsMap.set(post.id, post)
      })
    }
    
    // Luego añadir/actualizar con nuevos posts
    if (newPosts && Array.isArray(newPosts)) {
      newPosts.forEach(post => {
        postsMap.set(post.id, post)
      })
    }
    
    // Convertir de vuelta a array y ordenar por fecha
    const mergedPosts = Array.from(postsMap.values()).sort((a, b) => {
      return new Date(b.created_at) - new Date(a.created_at)
    })
    
    console.log('Posts combinados:', mergedPosts.length, 
      '(caché:', cachedPosts?.length || 0, 
      '+ nuevos:', newPosts?.length || 0, ')')
    
    return mergedPosts
  },

  // Verificar si el caché es válido (no ha expirado)
  isCacheValid: () => {
    const timestamp = localStorage.getItem(TIMESTAMP_KEY)
    if (!timestamp) return false
    
    const cacheTime = new Date(timestamp).getTime()
    const now = Date.now()
    const age = now - cacheTime
    const isValid = age < CACHE_DURATION
    
    console.log('Caché válido:', isValid, 'Edad:', Math.round(age / 1000), 'segundos')
    return isValid
  },

  // Limpiar caché
  clear: () => {
    localStorage.removeItem(POSTS_CACHE_KEY)
    localStorage.removeItem(TIMESTAMP_KEY)
    console.log('Caché limpiado')
  },

  // Filtrar posts inactivos del caché
  filterInactivePosts: () => {
    const { posts } = cache.getCachedPosts()
    if (posts && posts.length > 0) {
      // Filtrar solo posts con is_active = true (o undefined para posts antiguos)
      const activePosts = posts.filter(post => post.is_active !== false)
      console.log(`Filtrando posts inactivos: ${posts.length} -> ${activePosts.length}`)
      cache.savePosts(activePosts)
      return activePosts
    }
    return []
  }
}

// Mantener compatibilidad con el código antiguo si es necesario
export const cacheUtils = cache