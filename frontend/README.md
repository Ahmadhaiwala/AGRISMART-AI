# AgriSmart AI — Frontend

React + Vite frontend for the AgriSmart AI hackathon project.

## Quick Start

```bash
# 1. Install dependencies (already done)
npm install

# 2. Start the development server
npm run dev
```

Then open **http://localhost:5173** in your browser.

> The Vite dev server proxies all `/api` requests to `http://localhost:8000`.
> Make sure the FastAPI backend is running before using any module.

## Start the Backend

```bash
# From the backend/ directory
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Build for Production

```bash
npm run build      # outputs to frontend/dist/
npm run preview    # preview the production build locally
```

## Pages & Routes

| Route                  | Page                   | Backend API                          |
|------------------------|------------------------|--------------------------------------|
| `/`                    | Dashboard              | GET /health                          |
| `/disease-detection`   | Disease Detection      | POST /api/v1/predict                 |
| `/crop-recommendation` | Crop Recommendation    | POST /api/v1/test/crop_recommendation|
| `/smart-irrigation`    | Smart Irrigation       | POST /api/v1/irrigation/predict      |
| `/weather`             | Weather Intelligence   | POST /api/v1/weather-intelligence    |
| `/sustainability`      | Sustainability Score   | POST /api/v1/sustainability/score    |
| `/assistant`           | AI Farmer Assistant    | POST /api/v1/assistant/chat          |

## Project Structure

```
src/
├── components/
│   ├── Layout/
│   │   ├── AppLayout.jsx    # Shell: Sidebar + Topbar + Outlet
│   │   ├── Sidebar.jsx      # Dark-green nav with mobile drawer
│   │   └── Topbar.jsx       # Page title, search, notifications, user
│   └── UI/
│       ├── MetricCard.jsx
│       ├── Badge.jsx
│       ├── ProgressBar.jsx
│       ├── LoadingState.jsx
│       ├── EmptyState.jsx
│       ├── ErrorState.jsx
│       ├── SectionHeader.jsx
│       └── Card.jsx
├── pages/
│   ├── Dashboard.jsx
│   ├── DiseaseDetection.jsx
│   ├── CropRecommendation.jsx
│   ├── SmartIrrigation.jsx
│   ├── WeatherIntelligence.jsx
│   ├── Sustainability.jsx
│   └── FarmerAssistant.jsx
├── services/
│   └── api.js               # Axios instance + per-module API helpers
├── App.jsx                  # React Router routes
├── main.jsx                 # ReactDOM entry point
└── index.css                # AgriSmart design system
```
