/**
 * AgriSmart API Service
 * Centralized Axios instance pointing at the FastAPI backend.
 * Base URL is proxied through Vite to http://localhost:8000 in development.
 */
import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
})

// ─── Request interceptor ────────────────────────────────────────────────────
api.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
)

// ─── Response interceptor ───────────────────────────────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected error occurred'
    return Promise.reject(new Error(message))
  }
)

// ──────────────────────────────────────────────────────────────────────────────
// Disease Detection
// POST /predict  (multipart/form-data, field: file)
// ──────────────────────────────────────────────────────────────────────────────
export const diseaseAPI = {
  predict: (file) => {
    const form = new FormData()
    form.append('file', file)
    return api.post('/predict', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  getDiseases: () => api.get('/diseases'),
  getModelInfo: () => api.get('/model/info'),
}

// ──────────────────────────────────────────────────────────────────────────────
// Crop Recommendation
// POST /test/crop_recommendation
// ──────────────────────────────────────────────────────────────────────────────
export const cropAPI = {
  recommend: (payload) => api.post('/test/crop_recommendation', payload),
  health: () => api.get('/test/crop_recommendation/health'),
}

// ──────────────────────────────────────────────────────────────────────────────
// Smart Irrigation
// POST /irrigation/predict
// ──────────────────────────────────────────────────────────────────────────────
export const irrigationAPI = {
  predict: (payload) => api.post('/irrigation/predict', payload),
  health: () => api.get('/irrigation/health'),
  info: () => api.get('/irrigation/info'),
}

// ──────────────────────────────────────────────────────────────────────────────
// Weather Intelligence
// POST /weather-intelligence
// ──────────────────────────────────────────────────────────────────────────────
export const weatherAPI = {
  getIntelligence: (payload) => api.post('/weather-intelligence', payload),
  sampleLocations: () => api.get('/weather-intelligence/sample-locations'),
  info: () => api.get('/weather-intelligence/info'),
}

// ──────────────────────────────────────────────────────────────────────────────
// Sustainability
// POST /sustainability/score
// POST /sustainability/score/integrated
// ──────────────────────────────────────────────────────────────────────────────
export const sustainabilityAPI = {
  score: (payload) => api.post('/sustainability/score', payload),
  integrated: (payload) => api.post('/sustainability/score/integrated', payload),
  info: () => api.get('/sustainability/info'),
}

// ──────────────────────────────────────────────────────────────────────────────
// Farmer Assistant
// POST /assistant/chat
// ──────────────────────────────────────────────────────────────────────────────
export const assistantAPI = {
  chat: (payload) => api.post('/assistant/chat', payload),
}

// ──────────────────────────────────────────────────────────────────────────────
// Health check
// GET /health  (root of the FastAPI app, not /api/v1)
// ──────────────────────────────────────────────────────────────────────────────
export const healthCheck = () =>
  axios.get('/health', { timeout: 5000 })

export default api
