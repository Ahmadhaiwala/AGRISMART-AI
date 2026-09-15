"""
Dashboard router
Serves a single landing page that links out to every module (core +
bonus), and embeds live "try it" forms for the modules that don't have a
dedicated UI page yet (Sustainability, Smart Irrigation).
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AgriSmart AI - Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --paper: #F2F4EC;
    --ink: #1B2A1E;
    --forest: #1F4632;
    --forest-light: #2E5F45;
    --wheat: #C99A2E;
    --soil: #7A4B26;
    --line: #D6DCC9;
    --white: #FFFFFF;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: 'IBM Plex Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  a { color: inherit; }

  h1, h2, h3 { font-family: 'Fraunces', serif; margin: 0; }

  .wrap {
    max-width: 960px;
    margin: 0 auto;
    padding: 0 28px;
  }

  /* --- Top bar --- */
  .topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 22px 0;
    border-bottom: 1px solid var(--line);
  }
  .brand {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 20px;
    letter-spacing: 0.2px;
  }
  .topbar nav a {
    text-decoration: none;
    font-size: 14px;
    color: var(--forest);
    border-bottom: 1px solid transparent;
  }
  .topbar nav a:hover { border-bottom-color: var(--forest); }

  /* --- Hero --- */
  .hero {
    padding: 64px 0 44px;
    max-width: 620px;
  }
  .hero h1 {
    font-size: 40px;
    line-height: 1.15;
    font-weight: 500;
    color: var(--forest);
  }
  .hero p {
    margin-top: 18px;
    font-size: 16px;
    line-height: 1.6;
    color: #3B4A3E;
    max-width: 520px;
  }

  /* --- Core task feature band --- */
  .core-band {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    background: var(--forest);
    color: var(--white);
    border-radius: 4px;
    padding: 28px 30px;
    margin: 8px 0 40px;
  }
  .core-band .tag {
    display: inline-block;
    font-size: 12px;
    letter-spacing: 0.4px;
    padding: 3px 9px;
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 3px;
    margin-bottom: 10px;
  }
  .core-band h2 {
    font-size: 22px;
    font-weight: 500;
    color: var(--white);
  }
  .core-band p {
    margin: 8px 0 0;
    font-size: 14px;
    color: #DCE6DD;
    max-width: 420px;
  }
  .core-band .btn-light {
    flex-shrink: 0;
    background: var(--wheat);
    color: var(--ink);
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    padding: 11px 20px;
    border-radius: 3px;
    white-space: nowrap;
  }

  /* --- Module grid --- */
  .grid-label {
    font-size: 13px;
    color: var(--soil);
    margin-bottom: 14px;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 56px;
  }
  .card {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 4px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .code {
    font-size: 12px;
    display: inline-block;
    padding: 2px 7px;
    border-radius: 3px;
    width: fit-content;
  }
  .card .code {
    color: var(--soil);
    border: 1px solid var(--line);
  }
  .card h3 { font-size: 17px; font-weight: 500; color: var(--forest); }
  .card p { margin: 0; font-size: 13.5px; line-height: 1.5; color: #556354; flex-grow: 1; }
  .card a.action {
    text-decoration: none;
    font-size: 13.5px;
    font-weight: 600;
    color: var(--forest);
    border-bottom: 1px solid var(--forest);
    width: fit-content;
  }

  /* --- Try-it section --- */
  .try-it {
    border-top: 1px solid var(--line);
    padding: 44px 0 70px;
  }
  .try-it h2 {
    font-size: 24px;
    font-weight: 500;
    color: var(--forest);
    margin-bottom: 6px;
  }
  .try-it > p {
    color: #556354;
    font-size: 14px;
    margin: 0 0 30px;
  }
  .panels {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  .panel {
    background: var(--white);
    border: 1px solid var(--line);
    border-radius: 4px;
    overflow: hidden;
    scroll-margin-top: 20px;
  }
  .panel-header {
    padding: 18px 22px;
    background: var(--forest);
  }
  .panel-header.wheat { background: var(--wheat); }
  .panel-header .code {
    border: 1px solid rgba(255,255,255,0.55);
    color: var(--white);
  }
  .panel-header.wheat .code { border-color: rgba(27,42,30,0.4); color: var(--ink); }
  .panel-header h3 {
    color: var(--white);
    font-size: 18px;
    font-weight: 500;
    margin-top: 8px;
  }
  .panel-header.wheat h3 { color: var(--ink); }
  .panel-body { padding: 22px; }
  .field { margin-bottom: 12px; }
  .field label {
    display: block;
    font-size: 12.5px;
    color: var(--soil);
    margin-bottom: 4px;
  }
  .field input, .field select {
    width: 100%;
    padding: 8px 9px;
    font-size: 13.5px;
    border: 1px solid var(--line);
    border-radius: 3px;
    font-family: inherit;
    background: var(--paper);
    color: var(--ink);
  }
  .row2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

  .submit-btn {
    margin-top: 6px;
    width: 100%;
    background: var(--forest);
    color: var(--white);
    border: none;
    padding: 10px;
    font-size: 14px;
    font-weight: 600;
    border-radius: 3px;
    cursor: pointer;
    font-family: inherit;
  }
  .submit-btn:hover { background: var(--forest-light); }
  .submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }

  .result {
    margin-top: 16px;
    padding: 14px;
    border-radius: 3px;
    font-size: 13.5px;
    line-height: 1.6;
    display: none;
  }
  .result.show { display: block; }
  .result.ok { background: #EAF3EA; border: 1px solid #BFDCC0; }
  .result.err { background: #FBEAEA; border: 1px solid #E9BEBE; color: #7A2020; }
  .result .headline { font-weight: 600; margin-bottom: 4px; }
  .result ul { margin: 6px 0 0; padding-left: 18px; }

  footer {
    border-top: 1px solid var(--line);
    padding: 20px 0 40px;
    font-size: 12.5px;
    color: #7A8A7C;
  }

  @media (max-width: 760px) {
    .grid { grid-template-columns: 1fr; }
    .panels { grid-template-columns: 1fr; }
    .core-band { flex-direction: column; align-items: flex-start; }
    .hero h1 { font-size: 32px; }
  }
</style>
</head>
<body>

<div class="wrap">
  <div class="topbar">
    <div class="brand">AgriSmart AI</div>
    <nav><a href="/docs" target="_blank">API reference</a></nav>
  </div>

  <div class="hero">
    <h1>One field, four ways to see it.</h1>
    <p>A leaf photo, a soil reading, a fertilizer log &mdash; each tells you something
    different about the same crop. Pick where you want to start.</p>
  </div>

  <a href="/api/v1/predict" style="text-decoration:none;">
    <div class="core-band">
      <div>
        <span class="tag">Core task</span>
        <h2>Diagnose a leaf</h2>
        <p>Upload a photo and get a disease classification with a confidence score
        and precaution guidance.</p>
      </div>
      <span class="btn-light">Open &rarr;</span>
    </div>
  </a>

  <div class="grid-label">Bonus modules</div>
  <div class="grid">
    <a href="/docs#/Crop%20Recommendation" target="_blank" style="text-decoration:none;">
      <div class="card">
        <span class="code">Module A</span>
        <h3>Crop recommendation</h3>
        <p>Suggests a suitable crop from soil type, pH, temperature, humidity, and rainfall.</p>
        <span class="action">Open in API reference</span>
      </div>
    </a>

    <a href="#sustainability-panel" style="text-decoration:none;">
      <div class="card">
        <span class="code">Module D</span>
        <h3>Sustainability score</h3>
        <p>Scores water efficiency, resource use, and crop health, with improvement tips.</p>
        <span class="action">Try it below</span>
      </div>
    </a>

    <a href="#irrigation-panel" style="text-decoration:none;">
      <div class="card">
        <span class="code">Module B</span>
        <h3>Smart irrigation</h3>
        <p>Predicts whether to irrigate now from soil moisture, forecast, crop and stage.</p>
        <span class="action">Try it below</span>
      </div>
    </a>
  </div>

  <div class="try-it">
    <h2>Try the bonus modules</h2>
    <p>These run live against this server &mdash; no image upload needed.</p>

    <div class="panels">

      <div class="panel" id="sustainability-panel">
        <div class="panel-header">
          <span class="code">Module D</span>
          <h3>Sustainability score</h3>
        </div>
        <div class="panel-body">
        <div class="row2">
          <div class="field">
            <label>Water used (L)</label>
            <input type="number" id="s_water_used" value="120">
          </div>
          <div class="field">
            <label>Water required (L)</label>
            <input type="number" id="s_water_required" value="100">
          </div>
        </div>
        <div class="row2">
          <div class="field">
            <label>Fertilizer used (kg)</label>
            <input type="number" id="s_fert_used" value="5">
          </div>
          <div class="field">
            <label>Fertilizer recommended (kg)</label>
            <input type="number" id="s_fert_rec" value="4">
          </div>
        </div>
        <div class="field">
          <label>Crop health</label>
          <select id="s_healthy">
            <option value="true">Healthy</option>
            <option value="false" selected>Disease detected</option>
          </select>
        </div>
        <button class="submit-btn" onclick="runSustainability()">Compute score</button>
        <div class="result" id="s_result"></div>
        </div>
      </div>

      <div class="panel" id="irrigation-panel">
        <div class="panel-header wheat">
          <span class="code">Module B</span>
          <h3>Smart irrigation</h3>
        </div>
        <div class="panel-body">
        <div class="row2">
          <div class="field">
            <label>Crop</label>
            <input type="text" id="i_crop" value="Tomato">
          </div>
          <div class="field">
            <label>Growth stage</label>
            <select id="i_stage">
              <option value="seedling">Seedling</option>
              <option value="vegetative" selected>Vegetative</option>
              <option value="flowering">Flowering</option>
              <option value="fruiting">Fruiting</option>
            </select>
          </div>
        </div>
        <div class="row2">
          <div class="field">
            <label>Soil moisture (%)</label>
            <input type="number" id="i_moisture" value="28">
          </div>
          <div class="field">
            <label>Rain chance next 24h (%)</label>
            <input type="number" id="i_rain_prob" value="10">
          </div>
        </div>
        <div class="row2">
          <div class="field">
            <label>Forecast rain (mm, 24h)</label>
            <input type="number" id="i_rain_mm" value="0">
          </div>
          <div class="field">
            <label>Plot area (m&sup2;)</label>
            <input type="number" id="i_area" value="10">
          </div>
        </div>
        <button class="submit-btn" onclick="runIrrigation()">Check irrigation</button>
        <div class="result" id="i_result"></div>
        </div>
      </div>

    </div>
  </div>

  <footer>
    Built for the SIH 2026 internal hackathon &mdash; AgriSmart AI.
    Full endpoint list at <a href="/docs">/docs</a>.
  </footer>
</div>

<script>
async function runSustainability() {
  const btn = document.querySelector('#sustainability-panel .submit-btn');
  const box = document.getElementById('s_result');
  btn.disabled = true; btn.textContent = 'Computing...';
  box.className = 'result';

  const healthy = document.getElementById('s_healthy').value === 'true';
  const payload = {
    water_used_liters: Number(document.getElementById('s_water_used').value),
    water_required_liters: Number(document.getElementById('s_water_required').value),
    fertilizer_used_kg: Number(document.getElementById('s_fert_used').value),
    fertilizer_recommended_kg: Number(document.getElementById('s_fert_rec').value),
    pesticide_used_kg: 0,
    pesticide_recommended_kg: 0,
    is_healthy: healthy,
    disease_confidence: healthy ? 0 : 0.9
  };

  try {
    const res = await fetch('/api/v1/sustainability/score', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Request failed');

    box.className = 'result show ok';
    box.innerHTML = `
      <div class="headline">Score: ${data.overall_score} / 100 &middot; Grade ${data.grade}</div>
      Water ${data.sub_scores.water_efficiency} &middot;
      Resources ${data.sub_scores.resource_use} &middot;
      Health ${data.sub_scores.crop_health}
      <ul>${data.suggestions.map(s => `<li>${s}</li>`).join('')}</ul>
    `;
  } catch (e) {
    box.className = 'result show err';
    box.innerHTML = `<div class="headline">Couldn't compute the score</div>${e.message}`;
  } finally {
    btn.disabled = false; btn.textContent = 'Compute score';
  }
}

async function runIrrigation() {
  const btn = document.querySelector('#irrigation-panel .submit-btn');
  const box = document.getElementById('i_result');
  btn.disabled = true; btn.textContent = 'Checking...';
  box.className = 'result';

  const payload = {
    crop_type: document.getElementById('i_crop').value,
    growth_stage: document.getElementById('i_stage').value,
    soil_moisture_percent: Number(document.getElementById('i_moisture').value),
    rain_probability_percent: Number(document.getElementById('i_rain_prob').value),
    forecast_rain_mm_24h: Number(document.getElementById('i_rain_mm').value),
    area_sqm: Number(document.getElementById('i_area').value)
  };

  try {
    const res = await fetch('/api/v1/irrigation/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Request failed');

    const d = data.decision;
    const verdict = d.irrigation_required ? 'Irrigate now' : 'No irrigation needed';
    box.className = 'result show ok';
    box.innerHTML = `
      <div class="headline">${verdict} &middot; ${d.urgency} urgency</div>
      Status: ${d.soil_moisture_status.replace('_', ' ')} &middot;
      Recommended: ${d.recommended_water_liters} L
      <ul>${data.reasons.map(r => `<li>${r}</li>`).join('')}</ul>
    `;
  } catch (e) {
    box.className = 'result show err';
    box.innerHTML = `<div class="headline">Couldn't get a prediction</div>${e.message}`;
  } finally {
    btn.disabled = false; btn.textContent = 'Check irrigation';
  }
}
</script>

</body>
</html>
"""


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard() -> HTMLResponse:
    """Landing page linking to every module, with live forms for the ones without a UI."""
    return HTMLResponse(content=DASHBOARD_HTML)
