import React, { useState } from 'react'
import {
  CloudSun, MapPin, Thermometer, Droplets, Wind,
  CloudRain, CheckCircle, AlertTriangle, Info,
  RotateCcw, Clock, Shield,
} from 'lucide-react'
import { weatherAPI } from '../services/api.js'
import Badge from '../components/UI/Badge.jsx'
import LoadingState from '../components/UI/LoadingState.jsx'
import ErrorState from '../components/UI/ErrorState.jsx'

/* ─── Sample locations from backend ───────────────────────────────────────── */
const SAMPLE_LOCATIONS = [
  { name: 'Ahmedabad, Gujarat',   lat: 23.0225, lon: 72.5714 },
  { name: 'Delhi, India',         lat: 28.6139, lon: 77.2090 },
  { name: 'Punjab, India',        lat: 30.7333, lon: 76.7794 },
  { name: 'Maharashtra, India',   lat: 19.7515, lon: 75.7139 },
  { name: 'Iowa, USA',            lat: 41.8780, lon: -93.0977 },
]

const CROP_TYPES   = ['Wheat', 'Rice', 'Tomato', 'Cotton', 'Sugarcane', 'Potato', 'Maize']
const GROWTH_STAGES = ['Germination', 'Seedling', 'Vegetative', 'Flowering', 'Maturation', 'Harvest']

const DEFAULTS = {
  latitude: 23.0225,
  longitude: 72.5714,
  locationName: 'Ahmedabad, Gujarat',
  crop_type: 'Wheat',
  growth_stage: 'Vegetative',
  soil_moisture: 45,
  has_irrigation: true,
  disease_detected: false,
  recent_fertilization: false,
  forecast_days: 7,
}

function priorityVariant(p) {
  if (p === 'critical') return 'danger'
  if (p === 'high')     return 'danger'
  if (p === 'medium')   return 'warning'
  if (p === 'low')      return 'info'
  return 'info'
}

function weatherIcon(temp) {
  if (temp >= 35) return '🌡️'
  if (temp >= 25) return '☀️'
  if (temp >= 15) return '⛅'
  return '🌧️'
}

const DAY_LABELS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

export default function WeatherIntelligence() {
  const [form, setForm]       = useState(DEFAULTS)
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [error, setError]     = useState(null)

  const set = (k, v) => setForm(p => ({ ...p, [k]: v }))

  const setLocation = (loc) => setForm(p => ({
    ...p, latitude: loc.lat, longitude: loc.lon, locationName: loc.name,
  }))

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true); setError(null); setResult(null)
    try {
      const payload = {
        latitude: Number(form.latitude),
        longitude: Number(form.longitude),
        forecast_days: form.forecast_days,
        farm_conditions: {
          crop_type: form.crop_type,
          growth_stage: form.growth_stage,
          soil_moisture: Number(form.soil_moisture),
          has_irrigation: form.has_irrigation,
          disease_detected: form.disease_detected,
          recent_fertilization: form.recent_fertilization,
        },
      }
      const { data } = await weatherAPI.getIntelligence(payload)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const reset = () => { setForm(DEFAULTS); setResult(null); setError(null) }

  const ws = result?.weather_summary

  return (
    <div className="page-enter">
      <p style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 24, maxWidth: 620 }}>
        Combines live weather data with your farm conditions to produce prioritised
        farming actions, irrigation guidance and disease risk alerts.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: result ? '340px 1fr' : '480px 1fr', gap: 24, alignItems: 'start' }}>

        {/* ── Form ──────────────────────────────────────────────── */}
        <form onSubmit={submit} noValidate>
          <div className="card" style={{ padding: '22px 24px' }}>
            <h3 style={{ fontSize: 15, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
              <MapPin size={15} color="var(--primary-600)" /> Location & Conditions
            </h3>

            {/* Quick location picker */}
            <div style={{ marginBottom: 14 }}>
              <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: 6 }}>
                Quick Locations
              </label>
              <div className="chip-list">
                {SAMPLE_LOCATIONS.map(loc => (
                  <button key={loc.name} type="button"
                    className="chip"
                    style={form.locationName === loc.name ? { background: 'var(--primary-100)', borderColor: 'var(--primary-400)', color: 'var(--primary-800)' } : {}}
                    onClick={() => setLocation(loc)}
                  >
                    {loc.name.split(',')[0]}
                  </button>
                ))}
              </div>
            </div>

            {/* Lat/lon */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 14 }}>
              {[['Latitude', 'latitude', -90, 90], ['Longitude', 'longitude', -180, 180]].map(([label, field, min, max]) => (
                <div key={field} style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
                  <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>{label}</label>
                  <input type="number" className="input" value={form[field]} min={min} max={max} step={0.0001}
                    onChange={e => set(field, e.target.value)} style={{ padding: '9px 12px', fontSize: 13 }} />
                </div>
              ))}
            </div>

            <div style={{ borderTop: '1px solid var(--border-light)', margin: '14px 0' }} />

            {/* Crop info */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 14 }}>
              {[['Crop Type', 'crop_type', CROP_TYPES], ['Growth Stage', 'growth_stage', GROWTH_STAGES]].map(([label, field, opts]) => (
                <div key={field} style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
                  <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>{label}</label>
                  <select className="select" value={form[field]} onChange={e => set(field, e.target.value)}
                    style={{ padding: '9px 12px', fontSize: 13 }}>
                    {opts.map(o => <option key={o}>{o}</option>)}
                  </select>
                </div>
              ))}
            </div>

            {/* Soil moisture slider */}
            <div style={{ marginBottom: 14 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 5 }}>
                <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>Soil Moisture</label>
                <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--info)' }}>{form.soil_moisture}%</span>
              </div>
              <input type="range" min={0} max={100} value={form.soil_moisture}
                onChange={e => set('soil_moisture', Number(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--info)' }}
                aria-label="Soil moisture" />
            </div>

            {/* Checkboxes */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 18 }}>
              {[
                ['has_irrigation', 'Has irrigation system'],
                ['disease_detected', 'Disease recently detected'],
                ['recent_fertilization', 'Fertilized in last 7 days'],
              ].map(([field, label]) => (
                <label key={field} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, cursor: 'pointer' }}>
                  <input type="checkbox" checked={form[field]} onChange={e => set(field, e.target.checked)}
                    style={{ accentColor: 'var(--primary-600)', width: 15, height: 15 }} />
                  {label}
                </label>
              ))}
            </div>

            {error && <div style={{ marginBottom: 14 }}><ErrorState message={error} /></div>}

            <div style={{ display: 'flex', gap: 10 }}>
              <button type="submit" className="btn btn-primary" disabled={loading} style={{ flex: 1 }}>
                {loading ? 'Fetching…' : 'Get Weather Intelligence'}
              </button>
              <button type="button" className="btn btn-outline" onClick={reset} aria-label="Reset form">
                <RotateCcw size={14} />
              </button>
            </div>
          </div>
        </form>

        {/* ── Results ────────────────────────────────────────────── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {loading && <div className="card" style={{ padding: 0 }}><LoadingState message="Fetching live weather & generating farming intelligence…" /></div>}

          {result && !loading && (
            <>
              {/* Current weather card */}
              <div className="weather-main" style={{ borderRadius: 'var(--radius-lg)' }} aria-label="Current weather">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--primary-200)', fontSize: 13, marginBottom: 4 }}>
                      <MapPin size={13} />
                      {form.locationName}
                    </div>
                    <div className="weather-temperature">
                      {ws.current_temp?.toFixed(1)}°C
                    </div>
                    <div className="weather-location" style={{ marginTop: 4 }}>
                      {weatherIcon(ws.current_temp)} Forecast: {ws.forecast_min_temp?.toFixed(0)}° – {ws.forecast_max_temp?.toFixed(0)}°C
                    </div>
                  </div>

                  {/* Stats */}
                  <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
                    <WeatherStat icon={<Droplets size={15} />} label="Humidity" value={`${ws.current_humidity?.toFixed(0)}%`} />
                    <WeatherStat icon={<Wind size={15} />} label="Wind" value={`${ws.current_wind_speed?.toFixed(0)} km/h`} />
                    <WeatherStat icon={<CloudRain size={15} />} label="Rain chance" value={`${ws.forecast_rain_probability?.toFixed(0)}%`} />
                    <WeatherStat icon={<CloudRain size={15} />} label="Expected rain" value={`${ws.forecast_rain_amount?.toFixed(1)} mm`} />
                  </div>
                </div>

                {/* Irrigation summary */}
                <div style={{ marginTop: 20, background: 'rgba(255,255,255,0.1)', borderRadius: 12, padding: '12px 16px', fontSize: 13 }}>
                  <span style={{ fontWeight: 700, color: 'var(--lime-300)' }}>💡 Irrigation: </span>
                  <span style={{ color: 'white' }}>{result.irrigation_recommendation}</span>
                </div>
              </div>

              {/* Disease risk + work hours */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
                <div className="card" style={{ padding: '16px 18px' }}>
                  <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 5 }}>
                    <Shield size={13} /> Disease Risk
                  </div>
                  <div style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-primary)' }}>
                    {result.disease_risk_level}
                  </div>
                </div>
                <div className="card" style={{ padding: '16px 18px' }}>
                  <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 5 }}>
                    <Clock size={13} /> Optimal Work Hours
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>
                    {result.optimal_work_hours?.join(' · ') || '—'}
                  </div>
                </div>
              </div>

              {/* Recommended actions */}
              {result.recommended_actions?.length > 0 && (
                <div className="card" style={{ padding: '20px 22px' }}>
                  <h3 style={{ fontSize: 15, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                    <CheckCircle size={15} color="var(--primary-600)" /> Recommended Actions
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {result.recommended_actions.map((action, i) => (
                      <div key={i} style={{
                        background: 'var(--surface-soft)',
                        borderRadius: 'var(--radius-md)',
                        padding: '14px 16px',
                        borderLeft: `3px solid var(--${priorityVariant(action.priority) === 'danger' ? 'danger' : priorityVariant(action.priority) === 'warning' ? 'warning' : 'info'})`,
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                          <Badge variant={priorityVariant(action.priority)} style={{ fontSize: 10, padding: '2px 8px' }}>
                            {action.priority}
                          </Badge>
                          <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>{action.title}</span>
                        </div>
                        <p style={{ fontSize: 12, color: 'var(--text-secondary)', margin: '0 0 4px' }}>{action.description}</p>
                        <p style={{ fontSize: 11, color: 'var(--text-muted)', margin: 0 }}>⏱ {action.timing}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Risk alerts */}
              {result.risk_alerts?.length > 0 && (
                <div className="card" style={{ padding: '20px 22px' }}>
                  <h3 style={{ fontSize: 15, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                    <AlertTriangle size={15} color="var(--warning)" /> Risk Alerts
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {result.risk_alerts.map((alert, i) => (
                      <div key={i} style={{ background: 'var(--warning-bg)', borderRadius: 'var(--radius-md)', padding: '14px 16px', border: '1px solid rgba(200,144,22,0.2)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                          <AlertTriangle size={14} color="var(--warning)" />
                          <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>{alert.risk_type}</span>
                          <Badge variant={priorityVariant(alert.severity)} style={{ fontSize: 10 }}>{alert.severity}</Badge>
                        </div>
                        <p style={{ fontSize: 12, color: 'var(--text-secondary)', margin: '0 0 8px' }}>{alert.description}</p>
                        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                          {alert.prevention_tips?.map((tip, j) => (
                            <li key={j} style={{ fontSize: 12, color: 'var(--text-secondary)', display: 'flex', gap: 6, marginBottom: 3 }}>
                              <CheckCircle size={12} color="var(--success)" style={{ flexShrink: 0, marginTop: 2 }} />{tip}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div style={{ fontSize: 11, color: 'var(--text-light)', textAlign: 'right' }}>
                Data source: {result.data_source}
              </div>
            </>
          )}

          {!result && !loading && (
            <div className="card" style={{ padding: '48px 24px', textAlign: 'center' }}>
              <div style={{ width: 72, height: 72, borderRadius: '50%', background: 'var(--warning-bg)', display: 'grid', placeItems: 'center', color: 'var(--warning)', margin: '0 auto 16px' }}>
                <CloudSun size={32} />
              </div>
              <h3 style={{ fontSize: 15, marginBottom: 6 }}>Select a location to get started</h3>
              <p style={{ fontSize: 13, color: 'var(--text-muted)', margin: 0 }}>
                Live weather intelligence and farming advice will appear here.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function WeatherStat({ icon, label, value }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'rgba(197,220,200,0.8)', fontSize: 11, fontWeight: 600 }}>
        {icon} {label}
      </div>
      <div style={{ fontSize: 16, fontWeight: 700, color: 'white' }}>{value}</div>
    </div>
  )
}
