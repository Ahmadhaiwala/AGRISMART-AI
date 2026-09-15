import React from 'react'

/**
 * MetricCard — uses .metric-card from index.css
 * Props:
 *   icon      ReactNode
 *   label     string
 *   value     string | number
 *   sub       string   (small secondary line)
 *   iconBg    CSS color string  (default: var(--primary-100))
 *   iconColor CSS color string  (default: var(--primary-700))
 *   trend     'up' | 'down' | null
 *   loading   bool
 */
export default function MetricCard({
  icon,
  label,
  value,
  sub,
  iconBg,
  iconColor,
  loading = false,
}) {
  return (
    <div className="metric-card card-hover">
      <div
        className="metric-icon"
        style={{
          background: iconBg || 'var(--primary-100)',
          color: iconColor || 'var(--primary-700)',
        }}
        aria-hidden="true"
      >
        {icon}
      </div>

      {loading ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          <div className="skeleton" style={{ height: 28, width: '60%', borderRadius: 6 }} />
          <div className="skeleton" style={{ height: 14, width: '80%', borderRadius: 6 }} />
        </div>
      ) : (
        <>
          <div className="metric-value">{value ?? '—'}</div>
          <div className="metric-label">{label}</div>
          {sub && (
            <div
              style={{
                fontSize: 11,
                color: 'var(--text-light)',
                marginTop: 4,
              }}
            >
              {sub}
            </div>
          )}
        </>
      )}
    </div>
  )
}
