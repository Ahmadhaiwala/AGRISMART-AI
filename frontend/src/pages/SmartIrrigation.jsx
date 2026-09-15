import React, { useState } from 'react'
import { Droplets, CheckCircle, AlertTriangle, RotateCcw, Thermometer, Wind, Info } from 'lucide-react'
import { irrigationAPI } from '../services/api.js'
import Badge from '../components/UI/Badge.jsx'
import LoadingState from '../components/UI/LoadingState.jsx'
import ErrorState from '../components/UI/ErrorState.jsx'

/* ─── Backend enum values ──────────────────────────────────────────────────── */
const CROPS  = ['Wheat', 'Chilli', 'Potato', 'Carrot', 'Tomato']
const SOILS  = ['Clay Soil', 'Sandy Soil', 'Red Soil', 'Loam Soil', 'Black Soil', 'Alluvial Soil', 'Chalky Soil']
const STAGES = [
  'Germination',
  'Seedling Stage',
  'Vegetative Growth / Root or Tuber Development',
  'Flowering',
  'Pollination',
  'Fruit/Grain/Bulb Formation',
  'Maturation',
  'Harvest',
]

const DEFAULTS = {
  crop_id: 'Tomato',
  soil_type: 'Loam Soil',
  seedling_stage: 'Vegetative Growth / Root or Tuber Development',
  moi: 35,
  temp: 28,
  humidity: 65,
}

function levelStyle(levelCode) {
  if (levelCode === 0) return { variant: 'success', bg: 'var(--success-bg)', color: 'var(--success)', icon: <CheckCircle size={22} />, label: 'No Irrigation Needed' }
  if (levelCode === 1) return { variant: 'warning', bg: 'var(--warning-bg)', color: 'var(--warning)', icon: <Droplets size={22} />,     label: 'Medium Irrigation Required' }
  return                      { variant: 'danger',  bg: 'var(--danger-bg)',  color: 'var(--danger)',  icon: <AlertTriangle size={22} />, label: 'High Irrigation Required' }
}

export default function SmartIrrigation() {
  const [form, setForm]       = useState(DEFAULTS)
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [error, setError]     = useState(null)

  const set = (k, v) => setForm(p => ({ ...p, [k]: v }))

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true); setError(null); setResult(null)
    try {
      const payload = { ...form, moi: Number(form.moi), temp: Number(form.temp), humidity: Number(form.humidity) }
      const { data } = await irrigationAPI.predict(payload)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const reset = () => { setForm(DEFAULTS); setResult(null); setError(null) }

  const Field = ({ label, children }) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
      <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>{label}</label>
      {children}
    </div>
  )

  const Sel = ({ field, options }) => (
    <select className="select" value={form[field]} onChange={e => set(field, e.target.value)}
      style={{ padding: '9px 12px', fontSize: 13 }}>
      {options.map(o => <option key={o} value={o}>{o}</option>)}
    </select>
  )

  const recommendation = result?.recommendation
  const ls = recommendation ? levelStyle(recommendation.level_code) : null

  return (
    <div className="page-enter">
      <p style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 24, maxWidth: 580 }}>
        Enter your crop conditions to receive an AI-driven irrigation decision based on
        soil moisture, temperature and growth stage.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: result ? '1fr 1fr' : '560px 1fr', gap: 24, alignItems: 'start' }}>

        {/* ── Form ──────────────────────────────────────────────── */}
        <form onSubmit={submit} noValidate>
          <div className="card" style={{ padding: '24px 26px' }}>
            <h3 style={{ marginBottom: 20, fontSize: 15, display: 'flex', alignItems: 'center', gap: 8 }}>
              <Droplets size={16} color="var(--info)" /> Crop & Soil Conditions
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, marginBottom: 14 }}>
              <Field label="Crop Type"><Sel field="crop_id" options={CROPS} /></Field>
              <Field label="Soil Type"><Sel field="soil_type" options={SOILS} /></Field>
            </div>

            <Field label="Growth Stage" >
              <select className="select" value={form.seedling_stage} onChange={e => set('seedling_stage', e.target.value)}
                style={{ padding: '9px 12px', fontSize: 13, marginBottom: 14 }}>
                {STAGES.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </Field>

            <div style={{ borderTop: '1px solid var(--border-light)', margin: '16px 0' }} />

            {/* Sliders */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
              <SliderField
                label="Soil Moisture (MOI)"
                value={form.moi}
                min={0} max={100}
                unit="%"
                color={form.moi < 30 ? 'var(--danger)' : form.moi > 70 ? 'var(--info)' : 'var(--success)'}
                onChange={v => set('moi', v)}
              />
              <SliderField
                label="Temperature"
                value={form.temp}
                min={-10} max={60}
                unit="°C"
                color="var(--warning)"
                onChange={v => set('temp', v)}
              />
              <SliderField
                label="Humidity"
                value={form.humidity}
                min={0} max={100}
                unit="%"
                color="var(--info)"
                onChange={v => set('humidity', v)}
              />
            </div>

            {error && <div style={{ marginTop: 16 }}><ErrorState message={error} /></div>}

            <div style={{ display: 'flex', gap: 10, marginTop: 20 }}>
              <button type="submit" className="btn btn-primary" disabled={loading} style={{ flex: 1 }}>
                {loading ? 'Checking…' : 'Check Irrigation Need'}
              </button>
              <button type="button" className="btn btn-outline" onClick={reset}>
                <RotateCcw size={14} />
              </button>
            </div>
          </div>
        </form>

        {/* ── Result ────────────────────────────────────────────── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {loading && <div className="card" style={{ padding: 0 }}><LoadingState message="Calculating irrigation need…" /></div>}

          {result && !loading && (
            <>
              {/* Main decision */}
              <div style={{
                background: ls.bg,
                border: `1px solid ${ls.color}30`,
                borderRadius: 'var(--radius-lg)',
                padding: '28px 26px',
              }} aria-live="polite">
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14 }}>
                  <div style={{ color: ls.color }}>{ls.icon}</div>
                  <Badge variant={ls.variant} style={{ fontSize: 13, padding: '6px 14px' }}>
                    {ls.label}
                  </Badge>
                </div>

                <div style={{ fontSize: 26, fontWeight: 700, color: ls.color, marginBottom: 6 }}>
                  {recommendation.water_amount_liters
                    ? `${recommendation.water_amount_liters} L/m²`
                    : 'No water needed'}
                </div>
                <div style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
                  Confidence: <strong>{(recommendation.confidence * 100).toFixed(1)}%</strong>
                </div>
              </div>

              {/* Status cards */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <StatusTile icon={<Droplets size={16} />} label="Moisture Status" value={result.moisture_status} bg="var(--info-bg)" color="var(--info)" />
                <StatusTile icon={<Thermometer size={16} />} label="Temperature" value={result.temperature_status} bg="var(--warning-bg)" color="var(--warning)" />
              </div>

              {/* Suggestions */}
              {result.suggestions?.length > 0 && (
                <div className="card" style={{ padding: '20px 22px' }}>
                  <h3 style={{ fontSize: 15, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                    <CheckCircle size={15} color="var(--success)" /> Suggestions
                  </h3>
                  <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 10 }}>
                    {result.suggestions.map((s, i) => (
                      <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 10, fontSize: 13, color: 'var(--text-secondary)' }}>
                        <CheckCircle size={14} color="var(--success)" style={{ flexShrink: 0, marginTop: 2 }} />
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Conditions summary */}
              <div className="card" style={{ padding: '16px 20px' }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 10, display: 'flex', alignItems: 'center', gap: 6 }}>
                  <Info size={13} /> Conditions Used
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
                  {Object.entries(result.conditions || {}).map(([k, v]) => (
                    <div key={k} style={{ fontSize: 12 }}>
                      <span style={{ color: 'var(--text-muted)', textTransform: 'capitalize' }}>{k}: </span>
                      <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{String(v)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {!result && !loading && (
            <div className="card" style={{ padding: '48px 24px', textAlign: 'center' }}>
              <div style={{ width: 72, height: 72, borderRadius: '50%', background: 'var(--info-bg)', display: 'grid', placeItems: 'center', color: 'var(--info)', margin: '0 auto 16px' }}>
                <Droplets size={32} />
              </div>
              <h3 style={{ fontSize: 15, marginBottom: 6 }}>Enter field conditions</h3>
              <p style={{ fontSize: 13, color: 'var(--text-muted)', margin: 0 }}>
                Your irrigation recommendation will appear here.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function SliderField({ label, value, min, max, unit, color, onChange }) {
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>{label}</label>
        <span style={{ fontSize: 13, fontWeight: 700, color }}>{value}{unit}</span>
      </div>
      <input
        type="range" min={min} max={max} value={value}
        onChange={e => onChange(Number(e.target.value))}
        style={{ width: '100%', accentColor: color }}
        aria-label={label}
        aria-valuenow={value} aria-valuemin={min} aria-valuemax={max}
      />
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10, color: 'var(--text-light)', marginTop: 2 }}>
        <span>{min}{unit}</span><span>{max}{unit}</span>
      </div>
    </div>
  )
}

function StatusTile({ icon, label, value, bg, color }) {
  return (
    <div style={{ background: bg, borderRadius: 'var(--radius-md)', padding: '14px 16px', border: `1px solid ${color}25` }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, color, marginBottom: 6 }}>
        {icon}
        <span style={{ fontSize: 11, fontWeight: 600 }}>{label}</span>
      </div>
      <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>{value}</div>
    </div>
  )
}
