// Configuración de API para diferentes entornos
const isDevelopment = import.meta.env.MODE === 'development'

// URL del backend - Backend desplegado en Render
export const API_BASE_URL = isDevelopment 
  ? 'http://localhost:8000' 
  : 'https://visual-board-api.onrender.com' // Backend en Render

export const getApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`
}

export default {
  API_BASE_URL,
  getApiUrl
}