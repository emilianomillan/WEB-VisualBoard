import axios from 'axios'
import { API_BASE_URL } from '../config/api'

const API_URL = import.meta.env.VITE_API_URL || API_BASE_URL

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para añadir el X-User-Id desde sessionStorage
api.interceptors.request.use((config) => {
  const userId = sessionStorage.getItem('userId')
  if (userId) {
    config.headers['X-User-Id'] = userId
  } else {
    // Si no hay usuario, usar uno por defecto (solo para lectura)
    config.headers['X-User-Id'] = 'anonymous'
  }
  return config
})

// Posts API
export const postsAPI = {
  getAll: (page = 1, perPage = 20, minDate = null) => {
    const params = { page, per_page: perPage }
    if (minDate) {
      params.min_date = minDate
    }
    return api.get('/api/posts', { params })
  },
  
  getMyPosts: (page = 1, perPage = 20) => {
    const userId = sessionStorage.getItem('userId')
    return api.get('/api/posts', { params: { page, per_page: perPage, user_id: userId } })
  },
  
  getById: (id) => 
    api.get(`/api/posts/${id}`),
  
  create: (data) => 
    api.post('/api/posts', data),
  
  update: (id, data) => 
    api.put(`/api/posts/${id}`, data),
  
  partialUpdate: (id, data) => 
    api.patch(`/api/posts/${id}`, data),
  
  delete: (id) => 
    api.delete(`/api/posts/${id}`)
}

// Discover API
export const discoverAPI = {
  getRandom: (count = 30) => 
    api.get('/api/discover', { params: { count } })
}

// Health API
export const healthAPI = {
  check: () => 
    api.get('/health')
}

export default api