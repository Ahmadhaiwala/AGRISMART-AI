import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import AppLayout from './components/Layout/AppLayout.jsx'
import Dashboard from './pages/Dashboard.jsx'
import DiseaseDetection from './pages/DiseaseDetection.jsx'
import CropRecommendation from './pages/CropRecommendation.jsx'
import SmartIrrigation from './pages/SmartIrrigation.jsx'
import WeatherIntelligence from './pages/WeatherIntelligence.jsx'
import Sustainability from './pages/Sustainability.jsx'
import FarmerAssistant from './pages/FarmerAssistant.jsx'

export default function App() {
  return (
    <div className="app">
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="/disease-detection" element={<DiseaseDetection />} />
          <Route path="/crop-recommendation" element={<CropRecommendation />} />
          <Route path="/smart-irrigation" element={<SmartIrrigation />} />
          <Route path="/weather" element={<WeatherIntelligence />} />
          <Route path="/sustainability" element={<Sustainability />} />
          <Route path="/assistant" element={<FarmerAssistant />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </div>
  )
}
