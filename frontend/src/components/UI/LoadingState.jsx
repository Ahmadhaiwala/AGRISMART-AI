import React from 'react'

/**
 * LoadingState — centred spinner with optional message
 * Props:
 *   message  string
 *   size     'sm' | 'md' | 'lg'  (default 'md')
 *   fullPage bool
 */
export default function LoadingState({
  message = 'Loading…',
  size = 'md',
  fullPage = false,
}) {
  const dim = size === 'sm' ? 28 : size === 'lg' ? 64 : 44

  const inner = (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 16,
        padding: 32,
      }}
      role="status"
      aria-live="polite"
      aria-label={message}
    >
      {/* Spinner */}
      <div
        style={{
          width: dim,
          height: dim,
          borderRadius: '50%',
          border: `3px solid var(--primary-100)`,
          borderTopColor: 'var(--primary-600)',
          animation: 'agri-spin 0.8s linear infinite',
        }}
        aria-hidden="true"
      />
      {message && (
        <p style={{ fontSize: 14, color: 'var(--text-muted)', margin: 0 }}>{message}</p>
      )}

      {/* Keyframe injected once */}
      <style>{`
        @keyframes agri-spin { to { transform: rotate(360deg); } }
      `}</style>
    </div>
  )

  if (fullPage) {
    return (
      <div
        style={{
          position: 'fixed',
          inset: 0,
          display: 'grid',
          placeItems: 'center',
          background: 'rgba(245,247,240,0.7)',
          zIndex: 999,
        }}
      >
        {inner}
      </div>
    )
  }

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: 160,
      }}
    >
      {inner}
    </div>
  )
}
