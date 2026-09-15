# AgriSmart AI --- Frontend Design Specification

## 1. Purpose

This document defines the frontend design system and UI direction for
**AgriSmart AI --- Intelligent Agriculture for a Sustainable Future**.

The frontend is a lightweight React application intended for the
hackathon demo. Authentication, user management, and other non-essential
infrastructure are intentionally excluded for the first implementation.

The application should present the core crop-disease detection
capability and the selected bonus modules as one coherent farmer-facing
product.

The problem statement requires a minimal interface capable of running a
prediction on a new image, and the evaluation also considers
farmer-friendliness, clarity, accessibility/regional-language effort,
usability, integration, and deployment.

------------------------------------------------------------------------

# 2. Product UI Structure

The application will contain the following primary screens:

1.  Dashboard
2.  Disease Detection
3.  Crop Recommendation
4.  Smart Irrigation
5.  Weather Intelligence
6.  Sustainability Score
7.  AI Farmer Assistant

### Navigation

The main navigation should remain visible throughout the application.

``` text
AgriSmart AI
│
├── Dashboard
├── Disease Detection
├── Crop Recommendation
├── Smart Irrigation
├── Weather Intelligence
├── Sustainability Score
└── AI Farmer Assistant
```

The application does not require authentication during the initial UI
implementation.

------------------------------------------------------------------------

# 3. Design Philosophy

## Visual Direction

The visual language combines:

-   Modern agricultural technology
-   Natural/farm imagery
-   Clean SaaS dashboard structure
-   Soft cream/off-white backgrounds
-   Forest green primary color
-   Fresh green secondary accents
-   Small amounts of lime for emphasis
-   Rounded cards
-   Clear information hierarchy
-   Minimal visual clutter

The interface should feel:

> **Trustworthy + Natural + Intelligent + Practical**

Avoid making the product look like a generic dark AI dashboard.

------------------------------------------------------------------------

# 4. Color System

All colors should be defined as CSS variables in `index.css`.

## Primary Green

``` css
--primary-950: #071C12;
--primary-900: #0B2618;
--primary-800: #103C24;
--primary-700: #155B32;
--primary-600: #1D7540;
--primary-500: #2F914D;
--primary-400: #55AD63;
--primary-300: #83C987;
--primary-200: #B7DFB5;
--primary-100: #DFF1DC;
--primary-50: #EFF8ED;
```

### Usage

-   `950–900`: sidebar / deep branding
-   `800–700`: primary buttons and important actions
-   `600–500`: charts, indicators, active states
-   `300–100`: backgrounds and subtle highlights

------------------------------------------------------------------------

## Accent Lime

``` css
--lime-500: #C8F238;
--lime-400: #D8F75B;
--lime-300: #E7FA91;
--lime-100: #F4FBD5;
```

Use lime sparingly.

Good uses:

-   Small highlights
-   Important CTA accents
-   AI status indicators
-   Selected states
-   Decorative agricultural details

Do not use lime as the main page background.

------------------------------------------------------------------------

## Background

``` css
--background: #F5F7F0;
--background-soft: #EEF3E9;
--surface: #FFFFFF;
--surface-soft: #F8FAF5;
--surface-green: #EDF7E9;
```

The majority of the interface should remain neutral.

------------------------------------------------------------------------

## Text

``` css
--text-primary: #122018;
--text-secondary: #536158;
--text-muted: #7D887F;
--text-light: #A3ACA5;
--text-white: #FFFFFF;
```

Use strong contrast for important information.

------------------------------------------------------------------------

## Status Colors

``` css
--success: #238447;
--success-bg: #E8F6E9;

--warning: #C89016;
--warning-bg: #FFF6DC;

--danger: #D94B45;
--danger-bg: #FDEBEA;

--info: #3D82C4;
--info-bg: #EAF3FB;
```

Status colors should communicate meaning rather than decoration.

Examples:

-   Green = healthy / recommended
-   Yellow = warning / monitor
-   Red = disease / critical issue
-   Blue = weather / information

------------------------------------------------------------------------

# 5. Typography

Use:

-   **DM Sans** for application UI
-   **Playfair Display** for selected large marketing/hero headings

``` css
font-family: 'DM Sans', sans-serif;
```

Display headings:

``` css
font-family: 'Playfair Display', serif;
```

Do not use decorative typography for ordinary dashboard labels.

------------------------------------------------------------------------

# 6. Layout

## Desktop

The primary desktop layout:

``` text
┌──────────────┬─────────────────────────────────────────┐
│              │                                         │
│   Sidebar    │              Main Content               │
│              │                                         │
│              │                                         │
│              │                                         │
│              │                                         │
└──────────────┴─────────────────────────────────────────┘
```

Recommended sidebar width:

``` text
250px
```

Main content should be responsive and occupy the remaining width.

------------------------------------------------------------------------

# 7. Sidebar

The sidebar uses the darkest green.

### Contents

``` text
🌿 AgriSmart AI

Dashboard

Disease Detection

Crop Recommendation

Smart Irrigation

Weather Intelligence

Sustainability Score

AI Farmer Assistant
```

The active navigation item should use a lighter green background.

Example:

``` text
┌────────────────────────┐
│ 🌿 AgriSmart AI        │
│                        │
│ 🏠 Dashboard           │ ← active
│ 🦠 Disease Detection   │
│ 🌾 Crop Recommendation │
│ 💧 Smart Irrigation    │
│ 🌦 Weather Intelligence│
│ ♻ Sustainability       │
│ 🤖 AI Assistant        │
└────────────────────────┘
```

------------------------------------------------------------------------

# 8. Cards

Cards are the primary UI building block.

``` css
background: var(--surface);
border: 1px solid var(--border-light);
border-radius: 20px;
box-shadow: var(--shadow-sm);
```

Cards should not have heavy borders or excessive shadows.

Recommended radius:

-   Small controls: `8px`
-   Inputs/buttons: `12–14px`
-   Cards: `18–20px`
-   Large hero cards: `24–28px`

------------------------------------------------------------------------

# 9. Dashboard UI

The dashboard is the landing page.

## Goal

Give the farmer a quick overview of:

-   Current farm conditions
-   Weather
-   Soil moisture
-   Sustainability
-   Recent disease detection
-   Crop recommendation
-   Important farming actions

The dashboard should summarize information rather than duplicate every
module.

------------------------------------------------------------------------

## Dashboard Header

Example:

``` text
Good afternoon, Farmer 🌱

Here's what's happening with your farm today.
```

Actions:

``` text
[ Explore Modules ]
```

------------------------------------------------------------------------

## Quick Metrics

Use four metric cards.

``` text
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ 🌡 Weather │ │ 💧 Moisture │ │ ♻ Score    │ │ 🌧 Rain    │
│            │ │            │ │            │ │            │
│ 28°C       │ │ 31%        │ │ 82/100     │ │ 30%        │
│ Ahmedabad  │ │ Soil       │ │ Good       │ │ Tomorrow   │
└────────────┘ └────────────┘ └────────────┘ └────────────┘
```

For the first UI pass these values may be mock data.

------------------------------------------------------------------------

# 10. Farm Intelligence Section

Show actionable recommendations from the modules.

Example:

``` text
🌦 Weather Intelligence

Rain likely in the next 24 hours.

Recommendation:
Delay irrigation to avoid unnecessary water use.

[ View Weather ]
```

This section should prioritize actions over raw numbers.

------------------------------------------------------------------------

# 11. Recent Disease Detection

Example:

``` text
Recent Disease Check

Tomato Early Blight

Confidence
92.4%

Status
Disease Detected

[ View Details ]
```

The full image analysis belongs to the Disease Detection page.

------------------------------------------------------------------------

# 12. Crop Recommendation Summary

Example:

``` text
Recommended Crops

1. Cotton       High suitability
2. Groundnut    High suitability
3. Maize        Moderate suitability

[ Get New Recommendation ]
```

------------------------------------------------------------------------

# 13. Disease Detection UI

This is the most important functional screen because crop-disease
detection is the mandatory core task.

The problem statement requires the interface to accept a leaf/crop image
and produce a classification result.

## Layout

``` text
Disease Detection

Upload a leaf image to identify the disease.

┌─────────────────────────┐
│                         │
│       📷 Upload         │
│                         │
│ Drag & drop image here  │
│ or click to upload      │
│                         │
└─────────────────────────┘

              ↓

┌─────────────────────────┐
│ Disease Result          │
│                         │
│ Tomato Early Blight     │
│ Confidence: 92.4%       │
│                         │
│ Recommendations         │
│ ✓ Remove infected leaves│
│ ✓ Avoid overhead water  │
└─────────────────────────┘
```

Include:

-   Image preview
-   Prediction
-   Confidence
-   Disease/healthy status
-   Basic precautionary guidance

------------------------------------------------------------------------

# 14. Crop Recommendation UI

Inputs should reflect the problem statement.

Potential fields:

-   Soil type
-   pH
-   Temperature
-   Humidity
-   Rainfall
-   Water availability
-   Season
-   Location
-   Previous crop

Layout:

``` text
┌─────────────────────────────┬─────────────────────────────┐
│ Farm Information            │ Recommended Crops           │
│                             │                             │
│ Soil Type       [ Loamy ]   │ 🌾 Cotton                   │
│ pH              [ 6.5 ]     │ High suitability            │
│ Temperature     [ 28°C ]    │                             │
│ Humidity        [ 70% ]     │ 🥜 Groundnut                │
│ Rainfall        [ 800mm ]   │ High suitability            │
│ Season          [ Kharif ]  │                             │
│ Location        [ ... ]     │ 🌽 Maize                    │
│ Previous Crop   [ ... ]     │ Moderate suitability        │
│                             │                             │
│ [ Get Recommendations ]     │                             │
└─────────────────────────────┴─────────────────────────────┘
```

------------------------------------------------------------------------

# 15. Smart Irrigation UI

Inputs:

-   Soil moisture
-   Weather forecast
-   Crop type
-   Growth stage

Output should be extremely clear.

Example:

``` text
💧 Irrigation Recommendation

IRRIGATION NOT REQUIRED

Soil moisture: 42%
Rain forecast: High
Crop: Tomato
Growth stage: Vegetative

Reason:
Rainfall is expected within the next 24 hours.

Suggestions:
✓ Delay irrigation
✓ Recheck soil moisture tomorrow
✓ Avoid unnecessary watering
```

The recommendation should be visually more prominent than the raw model
values.

------------------------------------------------------------------------

# 16. Weather Intelligence UI

Show:

-   Current temperature
-   Humidity
-   Rain probability
-   Wind
-   Multi-day forecast
-   Farming actions

Example:

``` text
Ahmedabad, Gujarat

28°C
Partly Cloudy

Humidity     62%
Wind         12 km/h
Rain Chance  30%

Mon  Tue  Wed  Thu  Fri
☀   🌧   🌧   ☀   ☀
28° 27° 26° 29° 30°

┌──────────────────────────────────────────┐
│ 💡 Farming Advice                        │
│ Rain likely in next 24 hours.            │
│ Consider delaying irrigation.            │
└──────────────────────────────────────────┘
```

------------------------------------------------------------------------

# 17. Sustainability Score UI

Show a large overall score with component scores.

Example:

``` text
┌──────────────────────┬─────────────────────────────┐
│                      │ Sustainability Breakdown    │
│       82             │                             │
│      /100             │ Water Efficiency     80    │
│                      │ ███████████████░░            │
│       GOOD           │                             │
│                      │ Resource Use         75    │
│                      │ █████████████░░░             │
│                      │                             │
│                      │ Crop Health          90    │
│                      │ █████████████████░           │
└──────────────────────┴─────────────────────────────┘

Improvement Suggestions

✓ Improve water-use efficiency
✓ Consider drip irrigation
✓ Maintain crop rotation
✓ Monitor soil health
```

The exact scoring formula/rules must be documented and reproducible in
the project documentation.

------------------------------------------------------------------------

# 18. AI Farmer Assistant UI

The assistant should feel like a practical farming companion, not a
generic chatbot.

Example:

``` text
🤖 AI Farmer Assistant

Ask questions about your crops, irrigation,
disease results, weather, or recommendations.

Farmer:
How can I prevent tomato early blight?

AgriSmart:
To reduce the risk of tomato early blight:

• Remove affected leaves
• Avoid overhead watering
• Maintain proper spacing
• Monitor leaves regularly

[ Ask another question... ]
```

Suggested quick prompts:

``` text
[ Explain my disease result ]
[ When should I irrigate? ]
[ Suggest a crop ]
[ Explain today's weather ]
[ Give sustainability tips ]
```

The assistant should eventually use the application's module outputs as
context instead of independently inventing farm facts.

------------------------------------------------------------------------

# 19. Shared Components

Build reusable components instead of duplicating UI.

Suggested structure:

``` text
src/
├── components/
│   ├── Layout/
│   │   ├── Sidebar.jsx
│   │   └── Topbar.jsx
│   │
│   ├── UI/
│   │   ├── Button.jsx
│   │   ├── Card.jsx
│   │   ├── Badge.jsx
│   │   ├── Input.jsx
│   │   ├── Select.jsx
│   │   └── ProgressBar.jsx
│   │
│   ├── Dashboard/
│   │   ├── MetricCard.jsx
│   │   ├── FarmInsight.jsx
│   │   └── RecentDisease.jsx
│   │
│   └── Assistant/
│       ├── ChatMessage.jsx
│       └── ChatInput.jsx
│
├── pages/
│   ├── Dashboard.jsx
│   ├── DiseaseDetection.jsx
│   ├── CropRecommendation.jsx
│   ├── SmartIrrigation.jsx
│   ├── WeatherIntelligence.jsx
│   ├── Sustainability.jsx
│   └── FarmerAssistant.jsx
│
├── services/
│   └── api.js
│
├── App.jsx
└── index.css
```

------------------------------------------------------------------------

# 20. Routing

Use React Router.

Routes:

``` text
/
  → Dashboard

/disease-detection
  → Disease Detection

/crop-recommendation
  → Crop Recommendation

/smart-irrigation
  → Smart Irrigation

/weather
  → Weather Intelligence

/sustainability
  → Sustainability Score

/assistant
  → AI Farmer Assistant
```

Authentication is intentionally excluded from the first implementation.

------------------------------------------------------------------------

# 21. API Integration Strategy

The UI should initially use mock data.

After each page is visually complete:

``` text
React UI
   ↓
Mock function
   ↓
FastAPI endpoint
   ↓
Real module/model
```

Example:

``` javascript
// Initial
const result = mockDiseasePrediction;

// Later
const result = await predictDisease(image);
```

This allows frontend development without waiting for every backend
module to be finished.

------------------------------------------------------------------------

# 22. Loading States

Every module that performs processing should have a loading state.

Example:

``` text
Analyzing leaf...

        ◌

This may take a few seconds.
```

Do not leave the interface frozen during model inference or API calls.

------------------------------------------------------------------------

# 23. Error States

Errors should be understandable to farmers.

Avoid:

``` text
500 Internal Server Error
```

Prefer:

``` text
We couldn't analyze this image.

Please make sure the leaf is clearly visible
and try again.

[ Try Again ]
```

Technical errors can still be logged in the browser/backend console.

------------------------------------------------------------------------

# 24. Responsive Design

The application must work on:

-   Desktop
-   Laptop
-   Tablet
-   Mobile

On smaller screens:

``` text
Sidebar
   ↓
Collapsed navigation / mobile menu
```

Cards should switch from multi-column grids to a single-column layout.

------------------------------------------------------------------------

# 25. Accessibility

Prioritize:

-   High text contrast
-   Clear button labels
-   Large enough touch targets
-   Visible focus states
-   Image alt text
-   Avoiding color as the only indicator
-   Simple language

Example:

Do not communicate:

``` text
🟢
```

alone.

Instead:

``` text
🟢 Irrigation Recommended
```

------------------------------------------------------------------------

# 26. Demo Philosophy

The application is being built for a hackathon demonstration.

The demo should tell a clear story:

``` text
Farmer
  ↓
Uploads leaf
  ↓
Disease detected
  ↓
Farm context added
  ↓
Weather checked
  ↓
Irrigation decision
  ↓
Sustainability impact
  ↓
AI Assistant explains everything
```

The UI should make this flow obvious.

------------------------------------------------------------------------

# 27. Implementation Order

Build the frontend one UI at a time.

Recommended order:

### Phase 1

Dashboard

### Phase 2

Disease Detection

### Phase 3

Crop Recommendation

### Phase 4

Smart Irrigation

### Phase 5

Weather Intelligence

### Phase 6

Sustainability Score

### Phase 7

AI Farmer Assistant

After all screens are complete:

``` text
Mock Data
   ↓
API Integration
   ↓
End-to-End Testing
   ↓
Deployment
   ↓
Demo Video
```

------------------------------------------------------------------------

# 28. Important Constraints

Do not add unnecessary complexity during the initial implementation.

Do NOT implement yet:

-   Authentication
-   User registration
-   Password management
-   Complex database-driven frontend state
-   Notifications infrastructure
-   Payment systems
-   Admin panel

Focus on:

-   Excellent UI
-   Clear farmer workflow
-   Working core prediction
-   Working bonus modules
-   API integration
-   Reliable demo

------------------------------------------------------------------------

# 29. Reference to Challenge Requirements

The mandatory core requirement is crop-disease detection using computer
vision, with a prediction interface that can classify a new image and
provide basic precautionary guidance.

The optional modules include crop recommendation, smart irrigation,
weather-based intelligence, sustainability score, farmer assistant, IoT
integration, and agentic advisory.

The evaluation places particular emphasis on:

-   AI/ML implementation
-   Technical implementation and reproducibility
-   Innovation
-   Sustainability/social impact
-   User experience
-   Problem understanding
-   Presentation/demo

Therefore, the frontend should prioritize a coherent, farmer-friendly
workflow rather than simply presenting a collection of unrelated model
outputs.

------------------------------------------------------------------------

# 30. Current Development Rule

Only build **one UI at a time**.

For the current stage:

> **Build Dashboard UI first.**

Use mock values initially.

Once the Dashboard is visually complete and responsive, move to:

> **Disease Detection UI**

Then continue module by module.

This keeps frontend development independent from backend/model
development and makes debugging significantly easier.
