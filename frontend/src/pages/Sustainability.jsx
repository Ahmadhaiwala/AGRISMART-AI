import React, { useState } from 'react'
import { Leaf, Droplets, Package, Heart, CheckCircle, RotateCcw, Info, TrendingUp } from 'lucide-react'
import { sustainabilityAPI } from '../services/api.js'
import Badge from '../components/UI/Badge.jsx'
import ProgressBar from '../components/UI/ProgressBar.jsx'
import LoadingState from '../components/UI/LoadingState.jsx'
import ErrorState from '../components/UI/ErrorState.jsx'

const GRADE_STYLES = {
  A: { color: 'var(--success)',  bg: 'var(--success-bg)',  label: 'Excellent' },
  B: { color: 'var(--primary-600)', bg: 'var(--primary-50)', label: 'Good' },
  C: { color: 'var(--warning)',  bg: 'var(--warning-bg)', label: 'Moderate' },
  D: { color: 'var(--danger)',   bg: 'var(--danger-bg)',  label: 'Needs Work' },
}

const DEFAULTS = {
  water_used_liters: 1200,
  water_required_liters: 1000,
  fertilizer_used_kg: 5,
  fertilizer_recommended_kg: 4,
  pesticide_used_kg: 0.3,
  pesticide_recommended_kg: 0.3,
  is_healthy: true,
  disease_confidence: 0,
}

export default function Sustainability() {
  const [form, setForm]       = useState(DEFAULTS)
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [error, setError]     = useState(null)

  const set = (k, v) => setForm(p => ({ ...p, [k]: v }))

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true); setError(null); setResult(null)
    try {
      const payload = {
        ...form,
        water_used_liters: Number(form.water_used_liters),
        water_required_liters: Number(form.water_required_liters),
        fertilizer_used_kg: Number(form.fertilizer_used_kg),
        fertilizer_recommended_kg: Number(form.fertilizer_recommended_kg),
        pesticide_used_kg: Number(form.pesticide_used_kg),
        pesticide_recommended_kg: Number(form.pesticide_recommended_kg),
        disease_confidence: Number(form.disease_confidence),
      }
      const { data } = await sustainabilityAPI.score(payload)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const reset = () => { setForm(DEFAULTS); setResult(null); setError(null) }

  const gradeStyle = result ? (GRADE_STYLES[result.grade] || GRADE_STYLES.C) : null

  const NumField = ({ label, field, min = 0, step = 0.1, hint }) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
      <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>{label}</label>
      <input type="number" className="input" value={form[field]} min={min} step={step}
        onChange={e => set(field, e.target.value)}
        style={{ padding: '9px 12px', fontSize: 13 }} />
      {hint && <span style={{ fontSize: 11, color: 'var(--text-light)' }}>{hint}</span>}
    </div>
  )

  return (
    <div className="page-enter">
      <p style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 24, maxWidth: 620 }}>
        Enter your actual resource usage to measure your farm's sustainability score
        across water efficiency, resource use and crop health.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: result ? '1fr 1fr' : '540px 1fr', gap: 24, alignItems: 'start' }}>

        {/* ── Form ──────────────────────────────────────────────── */}
        <form onSubmit={submit} noValidate>
          <div className="card" style={{ padding: '24px 26px' }}>
            <h3 style={{ fontSize: 15, marginBottom: 20, display: 'flex', alignItems: 'center', gap: 8 }}>
              <Leaf size={16} color="var(--primary-600)" /> Resource Usage
            </h3>

            {/* Water */}
            <SectionLabel icon={<Droplets size={14} />} label="Water Usage" color="var(--info)" />
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 18 }}>
              <NumField label="Water Used (L)" field="water_used_liters" step={10} />
              <NumField label="Water Required (L)" field="water_required_liters" step={10} />
            </div>

            {/* Fertilizer */}
            <SectionLabel icon={<Package size={14} />} label="Fertilizer" color="var(--warning)" />
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 18 }}>
              <NumField label="Fertilizer Used (kg)" field="fertilizer_used_kg" step={0.5} />
              <NumField label="Recommended (kg)" field="fertilizer_recommended_kg" step={0.5} />
            </div>

            {/* Pesticide */}
            <SectionLabel icon={<Package size={14} />} label="Pesticide (optional)" color="var(--danger)" />
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 18 }}>
              <NumField label="Pesticide Used (kg)" field="pesticide_used_kg" step={0.05} />
              <NumField label="Recommended (kg)" field="pesticide_recommended_kg" step={0.05} />
            </div>

            {/* Crop health */}
            <SectionLabel icon={<Heart size={14} />} label="Crop Health" color="var(--success)" />
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 20 }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, cursor: 'pointer' }}>
                <input type="checkbox" checked={form.is_healthy} onChange={e => set('is_healthy', e.target.checked)}
                  style={{ accentColor: 'var(--success)', width: 15, height: 15 }} />
                Crop is currently healthy
              </label>
              {!form.is_healthy && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
                  <label style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-secondary)' }}>
                    Disease Confidence (0 – 1)
                  </label>
                  <input type="number" className="input" value={form.disease_confidence}
                    min={0} max={1} step={0.01}
                    onChange={e => set('disease_confidence', e.target.value)}
                    style={{ padding: '9px 12px', fontSize: 13 }} />
                </div>
              )}
            </div>

            {error && <div style={{ marginBottom: 16 }}><ErrorState message={error} /></div>}

            <div style={{ display: 'flex', gap: 10 }}>
              <button type="submit" className="btn btn-primary" disabled={loading} style={{ flex: 1 }}>
                {loading ? 'Calculating…' : 'Calculate Score'}
              </button>
              <button type="button" className="btn btn-outline" onClick={reset}>
                <RotateCcw size={14} />
              </button>
            </div>
          </div>
        </form>

        {/* ── Result ────────────────────────────────────────────── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {loading && <div className="card" style={{ padding: 0 }}><LoadingState message="Computing sustainability score…" /></div>}

          {result && !loading && (
            <>
              {/* Score circle + grade */}
              <div className="card score-card" aria-label="Sustainability score">
                {/* Dynamic circle */}
                <div
                  className="score-circle-dynamic"
                  style={{
                    background: `conic-gradient(
                      ${gradeStyle.color} ${result.overall_score}%,
                      var(--primary-100) 0%
                    )`,
                  }}
                  aria-hidden="true"
                >
                  <div className="score-value-inner">
                    <div style={{ fontSize: 28, fontWeight: 700, color: gradeStyle.color, lineHeight: 1 }}>
                      {Math.round(result.overall_score)}
                    </div>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>/100</div>
                  </div>
                </div>

                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
                    <span style={{ fontSize: 28, fontWeight: 700, color: 'var(--text-primary)' }}>
                      Grade {result.grade}
                    </span>
                    <Badge variant={result.grade === 'A' ? 'success' : result.grade === 'B' ? 'info' : result.grade === 'C' ? 'warning' : 'danger'}>
                      {gradeStyle.label}
                    </Badge>
                  </div>

                  {/* Sub-scores */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12, width: '100%', minWidth: 180 }}>
                    <ProgressBar label="Water Efficiency" value={Math.round(result.sub_scores.water_efficiency)} color="var(--info)" />
                    <ProgressBar label="Resource Use" value={Math.round(result.sub_scores.resource_use)} color="var(--warning)" />
                    <ProgressBar label="Crop Health" value={Math.round(result.sub_scores.crop_health)} color="var(--success)" />
                  </div>
                </div>
              </div>

              {/* Suggestions */}
              {result.suggestions?.length > 0 && (
                <div className="card" style={{ padding: '20px 22px' }}>
                  <h3 style={{ fontSize: 15, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                    <TrendingUp size={15} color="var(--primary-600)" /> Improvement Suggestions
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

              {/* Formula note */}
              <div className="card" style={{ padding: '14px 18px', background: 'var(--primary-50)' }}>
                <div style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', alignItems: 'flex-start', gap: 6 }}>
                  <Info size={13} style={{ flexShrink: 0, marginTop: 1 }} />
                  Score formula v{result.formula_version}: Water Efficiency 40% · Resource Use 30% · Crop Health 30%
                </div>
              </div>
            </>
          )}

          {!result && !loading && (
            <div className="card" style={{ padding: '48px 24px', textAlign: 'center' }}>
              <div style={{ width: 72, height: 72, borderRadius: '50%', background: 'var(--primary-50)', display: 'grid', placeItems: 'center', color: 'var(--primary-300)', margin: '0 auto 16px' }}>
                <Leaf size={32} />
              </div>
              <h3 style={{ fontSize: 15, marginBottom: 6 }}>Enter your resource data</h3>
              <p style={{ fontSize: 13, color: 'var(--text-muted)', margin: 0 }}>
                Your sustainability score will be calculated and displayed here.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function SectionLabel({ icon, label, color }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, fontWeight: 700, color, marginBottom: 10, textTransform: 'uppercase', letterSpacing: 0.5 }}>
      <span style={{ color }}>{icon}</span>
      {label}
    </div>
  )
}
