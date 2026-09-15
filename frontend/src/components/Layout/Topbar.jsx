import React, { useState } from 'react'
import { useLocation } from 'react-router-dom'
import { Bell, Search, User, ChevronDown } from 'lucide-react'

const PAGE_TITLES = {
  '/':                    { title: 'Dashboard',             subtitle: 'Farm overview & AI insights' },
  '/disease-detection':   { title: 'Disease Detection',     subtitle: 'AI-powered crop disease analysis' },
  '/crop-recommendation': { title: 'Crop Recommendation',   subtitle: 'Get best crop suggestions for your field' },
  '/smart-irrigation':    { title: 'Smart Irrigation',      subtitle: 'Intelligent water management' },
  '/weather':             { title: 'Weather Intelligence',  subtitle: 'Real-time forecasts & farming advice' },
  '/sustainability':      { title: 'Sustainability Score',  subtitle: 'Measure and improve your farm\'s impact' },
  '/assistant':           { title: 'AI Farmer Assistant',   subtitle: 'Ask anything about your crops' },
}

export default function Topbar() {
  const location = useLocation()
  const [searchOpen, setSearchOpen] = useState(false)

  const info = PAGE_TITLES[location.pathname] || PAGE_TITLES['/']

  return (
    <header className="topbar" role="banner">
      {/* Page title */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <h1
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: 'var(--text-primary)',
            lineHeight: 1.2,
          }}
        >
          {info.title}
        </h1>
        <p
          style={{ fontSize: 12, color: 'var(--text-muted)', margin: 0 }}
          aria-label="Page description"
        >
          {info.subtitle}
        </p>
      </div>

      {/* Right controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        {/* Search */}
        <div style={{ position: 'relative' }}>
          {searchOpen ? (
            <input
              autoFocus
              className="input"
              placeholder="Search..."
              onBlur={() => setSearchOpen(false)}
              style={{
                width: 200,
                padding: '8px 12px 8px 36px',
                fontSize: 13,
                height: 36,
                borderRadius: 'var(--radius-full)',
              }}
              aria-label="Search"
            />
          ) : null}
          <button
            onClick={() => setSearchOpen((o) => !o)}
            aria-label="Toggle search"
            style={{
              position: searchOpen ? 'absolute' : 'relative',
              left: searchOpen ? 8 : 0,
              top: searchOpen ? '50%' : 0,
              transform: searchOpen ? 'translateY(-50%)' : 'none',
              background: searchOpen ? 'transparent' : 'var(--surface)',
              border: searchOpen ? 'none' : '1px solid var(--border-light)',
              borderRadius: 'var(--radius-full)',
              width: 36,
              height: 36,
              display: 'grid',
              placeItems: 'center',
              cursor: 'pointer',
              color: 'var(--text-muted)',
              transition: '0.2s ease',
              zIndex: 1,
            }}
          >
            <Search size={16} aria-hidden="true" />
          </button>
        </div>

        {/* Notification bell */}
        <button
          aria-label="Notifications"
          style={{
            position: 'relative',
            background: 'var(--surface)',
            border: '1px solid var(--border-light)',
            borderRadius: 'var(--radius-full)',
            width: 36,
            height: 36,
            display: 'grid',
            placeItems: 'center',
            cursor: 'pointer',
            color: 'var(--text-muted)',
          }}
        >
          <Bell size={16} aria-hidden="true" />
          {/* Unread indicator */}
          <span
            aria-label="1 new notification"
            style={{
              position: 'absolute',
              top: 7,
              right: 7,
              width: 7,
              height: 7,
              borderRadius: '50%',
              background: 'var(--danger)',
              border: '1.5px solid white',
            }}
          />
        </button>

        {/* User avatar */}
        <button
          aria-label="User menu"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            background: 'var(--surface)',
            border: '1px solid var(--border-light)',
            borderRadius: 'var(--radius-full)',
            padding: '4px 12px 4px 4px',
            cursor: 'pointer',
          }}
        >
          <div
            style={{
              width: 28,
              height: 28,
              borderRadius: '50%',
              background: 'var(--primary-700)',
              display: 'grid',
              placeItems: 'center',
            }}
          >
            <User size={14} color="white" aria-hidden="true" />
          </div>
          <span
            style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}
          >
            Farmer
          </span>
          <ChevronDown size={13} color="var(--text-muted)" aria-hidden="true" />
        </button>
      </div>
    </header>
  )
}
