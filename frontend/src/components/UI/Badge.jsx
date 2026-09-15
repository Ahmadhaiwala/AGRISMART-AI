import React from 'react'

/**
 * Badge — thin status chip
 * variant: 'success' | 'warning' | 'danger' | 'info' | 'neutral'
 */
export default function Badge({ children, variant = 'info', style }) {
  return (
    <span className={`badge badge-${variant}`} style={style}>
      {children}
    </span>
  )
}
