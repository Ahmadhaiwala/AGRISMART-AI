import React from 'react'

/**
 * Card — thin wrapper that applies .card + optional hover
 */
export default function Card({ children, hover = false, style, className = '' }) {
  return (
    <div
      className={`card${hover ? ' card-hover' : ''} ${className}`.trim()}
      style={style}
    >
      {children}
    </div>
  )
}
