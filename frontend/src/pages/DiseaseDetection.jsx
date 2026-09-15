import React, { useState, useRef, useCallback } from 'react'
import {
  Upload, ImageIcon, Microscope, AlertTriangle,
  CheckCircle, XCircle, RotateCcw, Info,
  ChevronDown, ChevronUp, Leaf, ArrowRight,
} from 'lucide-react'
import { diseaseAPI } from '../services/api.js'
import Badge from '../components/UI/Badge.jsx'
import LoadingState from '../components/UI/LoadingState.jsx'
import ErrorState from '../components/UI/ErrorState.jsx'
import SectionHeader from '../components/UI/SectionHeader.jsx'

/* ─── Disease info lookup (common treatments from backend class names) ─────── */
const DISEASE_TIPS = {
  healthy: {
    advice: [
      'Continue regular monitoring',
      'Maintain current watering schedule',
      'Apply balanced fertilizer as needed',
      'Keep good air circulation around plants',
    ],
  },
  default: {
    advice: [
      'Remove and destroy infected plant material',
      'Avoid overhead watering to reduce humidity',
      'Apply appropriate fungicide / bactericide',
      'Improve air circulation around plants',
      'Rotate crops next season',
      'Monitor surrounding plants closely',
    ],
  },
}

function getTips(predictedClass = '') {
  const lower = predictedClass.toLowerCase()
  if (lower.includes('healthy')) return DISEASE_TIPS.healthy.advice
  return DISEASE_TIPS.default.advice
}

function formatClassName(raw = '') {
  return raw
    .replace(/___/g, ' — ')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

function isHealthy(predictedClass = '') {
  return predictedClass.toLowerCase().includes('healthy')
}

function confidenceVariant(conf) {
  if (conf >= 0.85) return 'success'
  if (conf >= 0.60) return 'warning'
  return 'danger'
}

/* ─── Component ────────────────────────────────────────────────────────────── */
export default function DiseaseDetection() {
  const [preview, setPreview]       = useState(null)   // data-url string
  const [file, setFile]             = useState(null)   // File object
  const [dragOver, setDragOver]     = useState(false)
  const [loading, setLoading]       = useState(false)
  const [result, setResult]         = useState(null)   // API response
  const [error, setError]           = useState(null)
  const [showTop5, setShowTop5]     = useState(false)
  const inputRef = useRef(null)

  /* ── file handling ─────────────────────────────────────────────── */
  const handleFile = useCallback((f) => {
    if (!f) return
    if (!['image/jpeg', 'image/jpg', 'image/png'].includes(f.type)) {
      setError('Please upload a JPG or PNG image.')
      return
    }
    if (f.size > 10 * 1024 * 1024) {
      setError('Image must be under 10 MB.')
      return
    }
    setError(null)
    setResult(null)
    setFile(f)
    const reader = new FileReader()
    reader.onload = (e) => setPreview(e.target.result)
    reader.readAsDataURL(f)
  }, [])

  const onInputChange = (e) => handleFile(e.target.files?.[0])

  const onDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    handleFile(e.dataTransfer.files?.[0])
  }

  const onDragOver = (e) => { e.preventDefault(); setDragOver(true) }
  const onDragLeave = () => setDragOver(false)

  /* ── prediction ────────────────────────────────────────────────── */
  const analyze = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const { data } = await diseaseAPI.predict(file)
      setResult(data)
    } catch (err) {
      setError(err.message || 'Could not analyze the image. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setPreview(null)
    setFile(null)
    setResult(null)
    setError(null)
    setShowTop5(false)
    if (inputRef.current) inputRef.current.value = ''
  }

  /* ── derived values ────────────────────────────────────────────── */
  const prediction = result?.prediction
  const healthy    = prediction ? isHealthy(prediction.predicted_class) : null
  const tips       = prediction ? getTips(prediction.predicted_class) : []
  const confPct    = prediction ? (prediction.confidence * 100).toFixed(1) : null

  return (
    <div className="page-enter">

      {/* ── Page intro ─────────────────────────────────────────────── */}
      <div style={{ marginBottom: 24 }}>
        <p style={{ fontSize: 14, color: 'var(--text-secondary)', maxWidth: 580 }}>
          Upload a clear leaf or crop image. Our AI model will identify the disease,
          estimate confidence and suggest treatment steps.
        </p>
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: result ? '1fr 1fr' : '1fr',
          gap: 24,
          alignItems: 'start',
        }}
      >
        {/* ── Left: Upload panel ─────────────────────────────────── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>

          {/* Drop zone */}
          {!preview ? (
            <div
              className={`dropzone${dragOver ? ' dragover' : ''}`}
              onClick={() => inputRef.current?.click()}
              onDrop={onDrop}
              onDragOver={onDragOver}
              onDragLeave={onDragLeave}
              role="button"
              tabIndex={0}
              aria-label="Upload leaf image"
              onKeyDown={(e) => e.key === 'Enter' && inputRef.current?.click()}
            >
              <div
                style={{
                  width: 72,
                  height: 72,
                  borderRadius: '50%',
                  background: 'var(--primary-100)',
                  display: 'grid',
                  placeItems: 'center',
                  color: 'var(--primary-600)',
                }}
                aria-hidden="true"
              >
                <Upload size={30} />
              </div>
              <div>
                <p style={{ fontWeight: 600, color: 'var(--primary-800)', margin: 0, fontSize: 15 }}>
                  Drag & drop an image here
                </p>
                <p style={{ fontSize: 13, color: 'var(--text-muted)', margin: '4px 0 0' }}>
                  or click to browse files
                </p>
              </div>
              <p style={{ fontSize: 12, color: 'var(--text-light)', margin: 0 }}>
                Supports JPG, PNG — max 10 MB
              </p>
            </div>
          ) : (
            /* Preview card */
            <div className="card" style={{ overflow: 'hidden' }}>
              <div style={{ position: 'relative' }}>
                <img
                  src={preview}
                  alt="Uploaded leaf for analysis"
                  style={{
                    width: '100%',
                    maxHeight: 340,
                    objectFit: 'cover',
                    display: 'block',
                    borderRadius: 'var(--radius-lg) var(--radius-lg) 0 0',
                  }}
                />
                {/* Replace button */}
                <button
                  onClick={() => inputRef.current?.click()}
                  style={{
                    position: 'absolute',
                    top: 12,
                    right: 12,
                    background: 'rgba(7,28,18,0.75)',
                    border: 'none',
                    borderRadius: 8,
                    padding: '6px 12px',
                    color: 'white',
                    fontSize: 12,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 5,
                  }}
                  aria-label="Replace image"
                >
                  <ImageIcon size={13} /> Replace
                </button>
              </div>
              <div style={{ padding: '14px 18px', borderTop: '1px solid var(--border-light)' }}>
                <p style={{ fontSize: 13, color: 'var(--text-muted)', margin: 0 }}>
                  {file?.name} &nbsp;·&nbsp; {(file?.size / 1024).toFixed(0)} KB
                </p>
              </div>
            </div>
          )}

          <input
            ref={inputRef}
            type="file"
            accept="image/jpeg,image/jpg,image/png"
            style={{ display: 'none' }}
            onChange={onInputChange}
            aria-label="File input"
          />

          {/* Error */}
          {error && <ErrorState message={error} onRetry={preview ? analyze : undefined} />}

          {/* Action buttons */}
          <div style={{ display: 'flex', gap: 10 }}>
            {preview && !loading && (
              <>
                <button
                  className="btn btn-primary"
                  onClick={analyze}
                  disabled={loading}
                  style={{ flex: 1 }}
                  aria-label="Analyze image for disease"
                >
                  <Microscope size={16} />
                  Analyze Image
                </button>
                <button
                  className="btn btn-outline"
                  onClick={reset}
                  aria-label="Reset and upload new image"
                >
                  <RotateCcw size={15} />
                  Reset
                </button>
              </>
            )}
            {!preview && (
              <button
                className="btn btn-primary"
                onClick={() => inputRef.current?.click()}
                style={{ flex: 1 }}
                aria-label="Select image file"
              >
                <Upload size={16} />
                Select Image
              </button>
            )}
          </div>

          {/* Loading state */}
          {loading && (
            <div className="card" style={{ padding: 0 }}>
              <LoadingState message="Analyzing leaf image… this may take a few seconds." />
            </div>
          )}

          {/* Supported crops info */}
          <div
            className="card"
            style={{ padding: '16px 20px' }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                marginBottom: 10,
                fontSize: 13,
                fontWeight: 600,
                color: 'var(--text-secondary)',
              }}
            >
              <Info size={14} aria-hidden="true" />
              About this model
            </div>
            <p style={{ fontSize: 13, color: 'var(--text-muted)', margin: '0 0 8px' }}>
              Trained on 38 disease classes across tomato, potato, corn, apple, grape and more.
              Works best with clear, well-lit leaf images.
            </p>
            <div className="chip-list">
              {['Tomato', 'Potato', 'Corn', 'Apple', 'Grape', 'Pepper', 'Strawberry'].map((c) => (
                <span key={c} className="chip" style={{ cursor: 'default' }}>
                  <Leaf size={11} /> {c}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* ── Right: Result panel (visible after prediction) ───────── */}
        {prediction && (
          <div
            style={{ display: 'flex', flexDirection: 'column', gap: 16 }}
            aria-live="polite"
            aria-label="Disease detection results"
          >

            {/* Status banner */}
            <div className={healthy ? 'result-card-success' : 'result-card-danger'}>
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 12 }}>
                <div>
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 8,
                      marginBottom: 8,
                    }}
                  >
                    {healthy
                      ? <CheckCircle size={20} color="var(--success)" aria-hidden="true" />
                      : <AlertTriangle size={20} color="var(--danger)" aria-hidden="true" />
                    }
                    <Badge variant={healthy ? 'success' : 'danger'}>
                      {healthy ? 'Healthy Plant' : 'Disease Detected'}
                    </Badge>
                  </div>

                  <h2
                    style={{
                      fontSize: 22,
                      fontWeight: 700,
                      color: healthy ? 'var(--success)' : 'var(--danger)',
                      marginBottom: 4,
                    }}
                  >
                    {formatClassName(prediction.predicted_class)}
                  </h2>

                  <p style={{ fontSize: 13, color: 'var(--text-secondary)', margin: 0 }}>
                    AI confidence score
                  </p>
                </div>

                {/* Confidence circle */}
                <div style={{ textAlign: 'center', flexShrink: 0 }}>
                  <div
                    style={{
                      width: 80,
                      height: 80,
                      borderRadius: '50%',
                      background: `conic-gradient(
                        ${healthy ? 'var(--success)' : 'var(--danger)'}
                        ${prediction.confidence * 100}%,
                        var(--primary-100) 0%
                      )`,
                      display: 'grid',
                      placeItems: 'center',
                      position: 'relative',
                    }}
                    aria-hidden="true"
                  >
                    <div
                      style={{
                        position: 'absolute',
                        width: 62,
                        height: 62,
                        borderRadius: '50%',
                        background: healthy ? 'var(--success-bg)' : 'var(--danger-bg)',
                      }}
                    />
                    <span
                      style={{
                        position: 'relative',
                        zIndex: 1,
                        fontSize: 15,
                        fontWeight: 700,
                        color: healthy ? 'var(--success)' : 'var(--danger)',
                      }}
                    >
                      {confPct}%
                    </span>
                  </div>
                  <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
                    Confidence
                  </p>
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div className="card" style={{ padding: '20px 22px' }}>
              <h3 style={{ fontSize: 15, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
                <CheckCircle size={16} color="var(--primary-600)" aria-hidden="true" />
                {healthy ? 'Maintenance Tips' : 'Recommended Actions'}
              </h3>
              <ul
                style={{
                  listStyle: 'none',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 10,
                  padding: 0,
                  margin: 0,
                }}
              >
                {tips.map((tip, i) => (
                  <li
                    key={i}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: 10,
                      fontSize: 13,
                      color: 'var(--text-secondary)',
                    }}
                  >
                    <CheckCircle
                      size={14}
                      color="var(--success)"
                      style={{ flexShrink: 0, marginTop: 2 }}
                      aria-hidden="true"
                    />
                    {tip}
                  </li>
                ))}
              </ul>
            </div>

            {/* Top 5 predictions toggle */}
            {prediction.top5_predictions?.length > 0 && (
              <div className="card" style={{ padding: '16px 20px' }}>
                <button
                  onClick={() => setShowTop5((s) => !s)}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    padding: 0,
                    fontSize: 14,
                    fontWeight: 600,
                    color: 'var(--text-primary)',
                  }}
                  aria-expanded={showTop5}
                  aria-controls="top5-list"
                >
                  Top 5 Predictions
                  {showTop5 ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                </button>

                {showTop5 && (
                  <div
                    id="top5-list"
                    style={{
                      marginTop: 14,
                      display: 'flex',
                      flexDirection: 'column',
                      gap: 10,
                    }}
                  >
                    {prediction.top5_predictions.map((p, i) => (
                      <div key={i}>
                        <div
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            marginBottom: 4,
                            fontSize: 13,
                          }}
                        >
                          <span style={{ color: 'var(--text-secondary)' }}>
                            {i + 1}. {formatClassName(p.class)}
                          </span>
                          <Badge variant={confidenceVariant(p.confidence)}>
                            {(p.confidence * 100).toFixed(1)}%
                          </Badge>
                        </div>
                        <div className="progress" style={{ height: 5 }}>
                          <div
                            className="progress-bar"
                            style={{
                              width: `${p.confidence * 100}%`,
                              background: i === 0 ? 'var(--primary-600)' : 'var(--primary-300)',
                            }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Try again */}
            <button
              className="btn btn-outline"
              onClick={reset}
              style={{ alignSelf: 'flex-start' }}
              aria-label="Analyze a different image"
            >
              <RotateCcw size={14} />
              Analyze Another Image
            </button>
          </div>
        )}
      </div>

      {/* Responsive: stack on mobile */}
      <style>{`
        @media (max-width: 768px) {
          .disease-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  )
}
