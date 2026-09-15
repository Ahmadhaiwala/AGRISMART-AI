import React from 'react'

/**
 * ProgressBar
 * Props:
 *   value   0-100
 *   color   CSS color (default: var(--primary-600))
 *   height  px (default: 8)
 *   label   string  — shown left of bar
 *   showValue bool  — show numeric value right of bar
 */
export default function ProgressBar({
  value = 0,
  color,
  height = 8,
  label,
  showValue = true,
}) {
  const clamped = Math.max(0, Math.min(100, value))

  return (
    <div style={{ width: '100%' }}>
      {(label || showValue) && (
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: 6,
          }}
        >
          {label && (
            <span style={{ fontSize: 13, color: 'var(--text-secondary)', fontWeight: 500 }}>
              {label}
            </span>
          )}
          {showValue && (
            <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)' }}>
              {clamped}
            </span>
          )}
        </div>
      )}
      <div
        className="progress"
        style={{ height }}
        role="progressbar"
        aria-valuenow={clamped}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label}
      >
        <div
          className="progress-bar"
          style={{
            width: `${clamped}%`,
            background: color || 'var(--primary-600)',
          }}
        />
      </div>
    </div>
  )
}
