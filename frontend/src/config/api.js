// Configuración de API para diferentes entornos
const isDevelopment = import.meta.env.MODE === 'development'

// URL del backend - puedes cambiar esto para apuntar a tu backend en producción
export const API_BASE_URL = isDevelopment 
  ? 'http://localhost:8000' 
  : 'https://visual-board-backend.onrender.com' // Cambiar cuando tengas el backend desplegado

export const getApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`
}

export default {
  API_BASE_URL,
  getApiUrl
}