import React, { useState } from 'react'
import { Sprout, Leaf, CheckCircle, RotateCcw, Info, TrendingUp } from 'lucide-react'
import { cropAPI } from '../services/api.js'
import Badge from '../components/UI/Badge.jsx'
import LoadingState from '../components/UI/LoadingState.jsx'
import ErrorState from '../components/UI/ErrorState.jsx'
import ProgressBar from '../components/UI/ProgressBar.jsx'
import SectionHeader from '../components/UI/SectionHeader.jsx'

/* ─── Static option lists matching backend enum values ─────────────────────── */
const CROP_TYPES = ['FOOD GRAIN', 'OILSEEDS', 'PULSES', 'COMMERCIAL', 'HORTICULTURE', 'SPICES', 'FODDER']
const SOILS      = ['CLAYEY', 'SANDY', 'LOAMY', 'RED', 'BLACK', 'ALLUVIAL', 'LATERITE']
const SEASONS    = ['KHARIF', 'RABI', 'ZAID', 'WHOLE YEAR']
const SOURCES    = ['RAIN FED', 'IRRIGATION', 'DRIP', 'BOTH']

const CROP_ICONS = {
  rice: '🌾', wheat: '🌿', maize: '🌽', cotton: '🪴', sugarcane: '🎋',
  groundnut: '🥜', soybean: '🫘', jowar: '🌾', bajra: '🌾', barley: '🌾',
  default: '🌱',
}

function cropIcon(name = '') {
  const lower = name.toLowerCase()
  return CROP_ICONS[lower] || CROP_ICONS.default
}

function suitabilityLabel(conf) {
  if (conf >= 0.70) return { label: 'High suitability',     variant: 'success' }
  if (conf >= 0.40) return { label: 'Moderate suitability', variant: 'warning' }
  return               { label: 'Low suitability',          variant: 'danger'  }
}

/* ─── Default form values (sensible starting point) ───────────────────────── */
const DEFAULTS = {
  type_of_crop: 'FOOD GRAIN',
  soil: 'LOAMY',
  season: 'KHARIF',
  water_source: 'RAIN FED',
  soil_ph: 6.5,
  soil_ph_high: 7.5,
  temp: 25,
  max_temp: 35,
  waterrequired: 100,
  waterrequired_max: 150,
  relative_humidity: 60,
  relative_humidity_max: 80,
  n: 40,  n_max: 60,
  p: 30,  p_max: 50,
  k: 20,  k_max: 40,
}

export default function CropRecommendation() {
  const [form, setForm]     = useState(DEFAULTS)
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [error, setError]     = useState(null)

  const set = (k, v) => setForm(prev => ({ ...prev, [k]: v }))
  const num = (k, v) => set(k, parseFloat(v) || 0)

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const { data } = await cropAPI.recommend(form)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const reset = () => { setForm(DEFAULTS); setResult(null); setError(null) }

  /* ── Field helper ──────────────────────────────────────────────── */
  const Field = ({ label, children }) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
      <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>
        {label}
      </label>
      {children}
    </div>
  )

  const NumInput = ({ field, min, max, step = 0.1 }) => (
    <input
      type="number"
      className="input"
      value={form[field]}
      min={min}
      max={max}
      step={step}
      onChange={e => num(field, e.target.value)}
      style={{ padding: '9px 12px', fontSize: 13 }}
    />
  )

  const Sel = ({ field, options }) => (
    <select
      className="select"
      value={form[field]}
      onChange={e => set(field, e.target.value)}
      style={{ padding: '9px 12px', fontSize: 13 }}
    >
      {options.map(o => <option key={o} value={o}>{o}</option>)}
    </select>
  )

  return (
    <div className="page-enter">
      <p style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 24, maxWidth: 580 }}>
        Enter your soil, climate and water conditions to get the best crop suggestions
        powered by our CatBoost recommendation model.
      </p>

      <div style={{
        display: 'grid',
        gridTemplateColumns: result ? '1fr 1fr' : '640px 1fr',
        gap: 24,
        alignItems: 'start',
      }}>

        {/* ── Form ──────────────────────────────────────────────── */}
        <form onSubmit={submit} noValidate>
          <div className="card" style={{ padding: '24px 26px' }}>
            <h3 style={{ marginBottom: 20, fontSize: 15, display: 'flex', alignItems: 'center', gap: 8 }}>
              <Sprout size={16} color="var(--primary-600)" />
              Farm Information
            </h3>

            {/* Row 1 — categorical */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, marginBottom: 14 }}>
              <Field label="Crop Category">
                <Sel field="type_of_crop" options={CROP_TYPES} />
              </Field>
              <Field label="Season">
                <Sel field="season" options={SEASONS} />
              </Field>
              <Field label="Soil Type">
                <Sel field="soil" options={SOILS} />
              </Field>
              <Field label="Water Source">
                <Sel field="water_source" options={SOURCES} />
              </Field>
            </div>

            {/* Divider */}
            <div style={{ borderTop: '1px solid var(--border-light)', margin: '16px 0' }} />

            {/* Row 2 — numeric pairs */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, marginBottom: 14 }}>
              <Field label="Soil pH (min)">
                <NumInput field="soil_ph" min={0} max={14} />
              </Field>
              <Field label="Soil pH (max)">
                <NumInput field="soil_ph_high" min={0} max={14} />
              </Field>
              <Field label="Temperature °C (min)">
                <NumInput field="temp" min={-10} max={60} step={1} />
              </Field>
              <Field label="Temperature °C (max)">
                <NumInput field="max_temp" min={-10} max={60} step={1} />
              </Field>
              <Field label="Water Required mm (min)">
                <NumInput field="waterrequired" min={0} step={10} />
              </Field>
              <Field label="Water Required mm (max)">
                <NumInput field="waterrequired_max" min={0} step={10} />
              </Field>
              <Field label="Humidity % (min)">
                <NumInput field="relative_humidity" min={0} max={100} step={1} />
              </Field>
              <Field label="Humidity % (max)">
                <NumInput field="relative_humidity_max" min={0} max={100} step={1} />
              </Field>
            </div>

            {/* Divider */}
            <div style={{ borderTop: '1px solid var(--border-light)', margin: '16px 0' }} />

            {/* NPK */}
            <h4 style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 12, fontWeight: 600 }}>
              NPK Values (Nitrogen · Phosphorus · Potassium)
            </h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 14, marginBottom: 14 }}>
              <Field label="N min"><NumInput field="n" min={0} step={1} /></Field>
              <Field label="N max"><NumInput field="n_max" min={0} step={1} /></Field>
              <div /> {/* spacer */}
              <Field label="P min"><NumInput field="p" min={0} step={1} /></Field>
              <Field label="P max"><NumInput field="p_max" min={0} step={1} /></Field>
              <div />
              <Field label="K min"><NumInput field="k" min={0} step={1} /></Field>
              <Field label="K max"><NumInput field="k_max" min={0} step={1} /></Field>
            </div>

            {error && <div style={{ marginBottom: 16 }}><ErrorState message={error} /></div>}

            <div style={{ display: 'flex', gap: 10 }}>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
                style={{ flex: 1 }}
              >
                {loading ? 'Getting recommendations…' : 'Get Recommendations'}
              </button>
              <button type="button" className="btn btn-outline" onClick={reset}>
                <RotateCcw size={14} /> Reset
              </button>
            </div>
          </div>
        </form>

        {/* ── Results ────────────────────────────────────────────── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {loading && (
            <div className="card" style={{ padding: 0 }}>
              <LoadingState message="Finding the best crops for your conditions…" />
            </div>
          )}

          {result && !loading && (
            <>
              {/* Top pick */}
              <div
                style={{
                  background: 'linear-gradient(135deg, var(--primary-800), var(--primary-600))',
                  borderRadius: 'var(--radius-lg)',
                  padding: '28px 26px',
                  color: 'white',
                }}
              >
                <div style={{ fontSize: 12, color: 'var(--lime-300)', fontWeight: 600, marginBottom: 8, textTransform: 'uppercase', letterSpacing: 0.5 }}>
                  Top Recommendation
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                  <div style={{
                    width: 56, height: 56, borderRadius: 16,
                    background: 'rgba(255,255,255,0.12)',
                    display: 'grid', placeItems: 'center', fontSize: 26,
                  }}>
                    {cropIcon(result.top_crop)}
                  </div>
                  <div>
                    <div style={{ fontSize: 26, fontWeight: 700, textTransform: 'capitalize', lineHeight: 1.1 }}>
                      {result.top_crop}
                    </div>
                    <div style={{ fontSize: 13, color: 'var(--lime-300)', marginTop: 4 }}>
                      {(result.confidence * 100).toFixed(1)}% confidence match
                    </div>
                  </div>
                </div>
              </div>

              {/* Top 5 list */}
              <div className="card" style={{ padding: '20px 22px' }}>
                <h3 style={{ fontSize: 15, marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
                  <TrendingUp size={15} color="var(--primary-600)" />
                  All Recommendations
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                  {result.top_5_predictions.map((p, i) => {
                    const { label, variant } = suitabilityLabel(p.confidence)
                    return (
                      <div key={i}>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                            <span style={{ fontSize: 20 }}>{cropIcon(p.crop_name)}</span>
                            <div>
                              <div style={{ fontSize: 14, fontWeight: 600, textTransform: 'capitalize', color: 'var(--text-primary)' }}>
                                {p.crop_name}
                              </div>
                              <Badge variant={variant} style={{ marginTop: 2 }}>{label}</Badge>
                            </div>
                          </div>
                          <span style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-primary)' }}>
                            {(p.confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                        <ProgressBar
                          value={Math.round(p.confidence * 100)}
                          showValue={false}
                          color={i === 0 ? 'var(--primary-600)' : 'var(--primary-300)'}
                          height={6}
                        />
                      </div>
                    )
                  })}
                </div>
              </div>

              {/* Input summary */}
              <div className="card" style={{ padding: '16px 20px' }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 10, display: 'flex', alignItems: 'center', gap: 6 }}>
                  <Info size={13} /> Input Summary
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
                  {[
                    ['Soil', form.soil],
                    ['Season', form.season],
                    ['pH range', `${form.soil_ph} – ${form.soil_ph_high}`],
                    ['Temp range', `${form.temp}–${form.max_temp} °C`],
                    ['Water', `${form.waterrequired}–${form.waterrequired_max} mm`],
                    ['Humidity', `${form.relative_humidity}–${form.relative_humidity_max} %`],
                  ].map(([k, v]) => (
                    <div key={k} style={{ fontSize: 12 }}>
                      <span style={{ color: 'var(--text-muted)' }}>{k}: </span>
                      <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{v}</span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {!result && !loading && (
            <div className="card" style={{ padding: 0 }}>
              <div style={{ padding: '48px 24px', textAlign: 'center' }}>
                <div style={{
                  width: 72, height: 72, borderRadius: '50%',
                  background: 'var(--primary-50)',
                  display: 'grid', placeItems: 'center',
                  color: 'var(--primary-300)', margin: '0 auto 16px',
                }}>
                  <Sprout size={32} />
                </div>
                <h3 style={{ fontSize: 15, marginBottom: 6 }}>Fill in your farm conditions</h3>
                <p style={{ fontSize: 13, color: 'var(--text-muted)', margin: 0 }}>
                  Your top crop recommendations will appear here.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
