import React from 'react'
import { AlertTriangle } from 'lucide-react'

/**
 * ErrorState — friendly error display
 * Props:
 *   message  string
 *   onRetry  fn  (optional)
 */
export default function ErrorState({ message, onRetry }) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: '40px 24px',
        gap: 12,
        background: 'var(--danger-bg)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid rgba(217,75,69,0.15)',
      }}
      role="alert"
    >
      <div
        style={{
          width: 52,
          height: 52,
          borderRadius: '50%',
          background: 'rgba(217,75,69,0.1)',
          display: 'grid',
          placeItems: 'center',
          color: 'var(--danger)',
        }}
        aria-hidden="true"
      >
        <AlertTriangle size={24} />
      </div>
      <p style={{ fontSize: 14, color: 'var(--danger)', fontWeight: 600, margin: 0 }}>
        {message || 'Something went wrong. Please try again.'}
      </p>
      {onRetry && (
        <button className="btn btn-outline" onClick={onRetry} style={{ fontSize: 13 }}>
          Try Again
        </button>
      )}
    </div>
  )
}
