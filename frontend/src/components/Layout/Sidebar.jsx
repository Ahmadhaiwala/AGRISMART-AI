import React, { useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  Bug,
  Sprout,
  Droplets,
  CloudSun,
  Leaf,
  MessageSquare,
  Menu,
  X,
} from 'lucide-react'

const NAV_ITEMS = [
  { to: '/',                    label: 'Dashboard',            icon: LayoutDashboard },
  { to: '/disease-detection',   label: 'Disease Detection',    icon: Bug            },
  { to: '/crop-recommendation', label: 'Crop Recommendation',  icon: Sprout         },
  { to: '/smart-irrigation',    label: 'Smart Irrigation',     icon: Droplets       },
  { to: '/weather',             label: 'Weather Intelligence', icon: CloudSun       },
  { to: '/sustainability',      label: 'Sustainability Score',  icon: Leaf           },
  { to: '/assistant',           label: 'AI Assistant',         icon: MessageSquare  },
]

export default function Sidebar() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const location = useLocation()

  // Decide active for exact "/" vs sub-routes
  const isActive = (to) => {
    if (to === '/') return location.pathname === '/'
    return location.pathname.startsWith(to)
  }

  const navLinks = (
    <nav className="sidebar-nav" aria-label="Main navigation">
      {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          end={to === '/'}
          className={`sidebar-link${isActive(to) ? ' active' : ''}`}
          onClick={() => setMobileOpen(false)}
          aria-current={isActive(to) ? 'page' : undefined}
        >
          <Icon size={18} aria-hidden="true" />
          <span>{label}</span>
        </NavLink>
      ))}
    </nav>
  )

  return (
    <>
      {/* ── Desktop sidebar ─────────────────────────────── */}
      <aside className="sidebar" aria-label="Sidebar">
        {/* Logo */}
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon" aria-hidden="true">
            <Sprout size={18} />
          </div>
          <span>AgriSmart AI</span>
        </div>

        {navLinks}

        {/* Bottom tagline */}
        <div
          style={{
            marginTop: 'auto',
            padding: '16px 12px',
            fontSize: 11,
            color: 'rgba(184,200,188,0.55)',
            lineHeight: 1.5,
          }}
        >
          <div style={{ fontWeight: 600, marginBottom: 2, color: 'rgba(184,200,188,0.75)' }}>
            Healthy Crops
          </div>
          Brighter Tomorrows
        </div>
      </aside>

      {/* ── Mobile hamburger button ──────────────────────── */}
      <button
        className="btn"
        onClick={() => setMobileOpen(true)}
        aria-label="Open navigation menu"
        style={{
          display: 'none',
          position: 'fixed',
          top: 12,
          left: 12,
          zIndex: 200,
          width: 40,
          height: 40,
          minHeight: 40,
          padding: 0,
          background: 'var(--primary-950)',
          borderRadius: 10,
          '@media (maxWidth: 800px)': { display: 'grid' },
        }}
        id="mobile-menu-btn"
      >
        <Menu size={18} color="white" />
      </button>

      {/* ── Mobile overlay drawer ────────────────────────── */}
      {mobileOpen && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 300,
            display: 'flex',
          }}
        >
          {/* Backdrop */}
          <div
            style={{ flex: 1, background: 'rgba(0,0,0,0.45)' }}
            onClick={() => setMobileOpen(false)}
            aria-hidden="true"
          />

          {/* Drawer */}
          <aside
            style={{
              width: 260,
              background: 'var(--primary-950)',
              padding: '24px 16px',
              display: 'flex',
              flexDirection: 'column',
              gap: 0,
              order: -1,
            }}
            aria-label="Mobile navigation"
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                paddingBottom: 24,
                paddingLeft: 12,
                paddingRight: 4,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <div className="sidebar-logo-icon">
                  <Sprout size={18} />
                </div>
                <span style={{ fontWeight: 700, fontSize: 18, color: 'white' }}>
                  AgriSmart AI
                </span>
              </div>
              <button
                onClick={() => setMobileOpen(false)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  color: '#b8c8bc',
                  display: 'grid',
                  placeItems: 'center',
                }}
                aria-label="Close navigation menu"
              >
                <X size={20} />
              </button>
            </div>

            {navLinks}
          </aside>
        </div>
      )}

      {/* Inject mobile-button visibility via a style tag */}
      <style>{`
        @media (max-width: 800px) {
          #mobile-menu-btn { display: grid !important; }
        }
      `}</style>
    </>
  )
}
