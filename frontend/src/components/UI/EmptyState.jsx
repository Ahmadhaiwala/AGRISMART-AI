import React from 'react'

/**
 * EmptyState — shown when no data is available yet
 * Props:
 *   icon      ReactNode  (large icon, ~40px)
 *   title     string
 *   message   string
 *   action    ReactNode  (optional CTA button)
 */
export default function EmptyState({ icon, title, message, action }) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: '48px 24px',
        gap: 12,
      }}
      role="status"
    >
      {icon && (
        <div
          style={{
            width: 72,
            height: 72,
            borderRadius: '50%',
            background: 'var(--primary-50)',
            display: 'grid',
            placeItems: 'center',
            color: 'var(--primary-300)',
            marginBottom: 4,
          }}
          aria-hidden="true"
        >
          {icon}
        </div>
      )}
      {title && (
        <h3 style={{ fontSize: 16, fontWeight: 600, color: 'var(--text-primary)' }}>
          {title}
        </h3>
      )}
      {message && (
        <p style={{ fontSize: 14, color: 'var(--text-muted)', maxWidth: 320, margin: 0 }}>
          {message}
        </p>
      )}
      {action && <div style={{ marginTop: 8 }}>{action}</div>}
    </div>
  )
}
