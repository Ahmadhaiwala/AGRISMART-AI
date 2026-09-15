import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Thermometer, Droplets, Leaf, CloudRain,
  Bug, Sprout, CloudSun, MessageSquare,
  ArrowRight,
} from 'lucide-react'
import MetricCard from '../components/UI/MetricCard.jsx'
import SectionHeader from '../components/UI/SectionHeader.jsx'
import Badge from '../components/UI/Badge.jsx'
import ProgressBar from '../components/UI/ProgressBar.jsx'
import { healthCheck } from '../services/api.js'

/* ─── helpers ─────────────────────────────────────────────────────────────── */
function getGreeting() {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
}

/* ─── Module cards data ────────────────────────────────────────────────────── */
const MODULES = [
  {
    to: '/disease-detection',
    icon: Bug,
    iconBg: 'var(--danger-bg)',
    iconColor: 'var(--danger)',
    title: 'Disease Detection',
    desc: 'Identify crop diseases from leaf images using AI vision.',
  },
  {
    to: '/crop-recommendation',
    icon: Sprout,
    iconBg: 'var(--success-bg)',
    iconColor: 'var(--success)',
    title: 'Crop Recommendation',
    desc: 'Get best-fit crops based on soil, climate and season.',
  },
  {
    to: '/smart-irrigation',
    icon: Droplets,
    iconBg: 'var(--info-bg)',
    iconColor: 'var(--info)',
    title: 'Smart Irrigation',
    desc: 'Save water with AI-driven irrigation decisions.',
  },
  {
    to: '/weather',
    icon: CloudSun,
    iconBg: 'var(--warning-bg)',
    iconColor: 'var(--warning)',
    title: 'Weather Intelligence',
    desc: 'Timely farming actions backed by live forecasts.',
  },
  {
    to: '/sustainability',
    icon: Leaf,
    iconBg: 'var(--primary-100)',
    iconColor: 'var(--primary-700)',
    title: 'Sustainability Score',
    desc: 'Measure water, resource and crop health impact.',
  },
  {
    to: '/assistant',
    icon: MessageSquare,
    iconBg: '#eef0ff',
    iconColor: '#5c6bc0',
    title: 'AI Assistant',
    desc: 'Ask farming questions in plain language, 24/7.',
  },
]

/* ─── Dashboard ────────────────────────────────────────────────────────────── */
export default function Dashboard() {
  const [backendOnline, setBackendOnline] = useState(null)

  useEffect(() => {
    healthCheck()
      .then(() => setBackendOnline(true))
      .catch(() => setBackendOnline(false))
  }, [])

  return (
    <div className="page-enter">

      {/* ── Hero ─────────────────────────────────────────────────────── */}
      <section
        className="hero"
        style={{
          background: `
            linear-gradient(90deg,
              rgba(7,28,18,0.96) 0%,
              rgba(7,28,18,0.72) 45%,
              rgba(7,28,18,0.18) 100%
            ),
            linear-gradient(135deg, #103c24 0%, #1d7540 60%, #2f914d 100%)
          `,
        }}
        aria-labelledby="hero-heading"
      >
        <div className="hero-content">
          {/* Backend status pill */}
          {backendOnline !== null && (
            <div style={{ marginBottom: 16 }}>
              <span
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 6,
                  background: backendOnline
                    ? 'rgba(35,132,71,0.25)'
                    : 'rgba(217,75,69,0.25)',
                  border: `1px solid ${backendOnline ? 'rgba(35,132,71,0.5)' : 'rgba(217,75,69,0.5)'}`,
                  borderRadius: 'var(--radius-full)',
                  padding: '4px 12px',
                  fontSize: 12,
                  fontWeight: 600,
                  color: backendOnline ? '#83c987' : '#e88',
                }}
              >
                <span
                  style={{
                    width: 6, height: 6, borderRadius: '50%',
                    background: backendOnline ? '#83c987' : '#e88',
                  }}
                />
                {backendOnline ? 'AI Backend Online' : 'Backend Offline — check server'}
              </span>
            </div>
          )}

          <h1
            id="hero-heading"
            className="display-font"
            style={{ color: 'white', fontSize: 'clamp(1.8rem,3.5vw,3rem)', marginBottom: 14 }}
          >
            Smarter Farming for a<br />
            <span style={{ color: 'var(--lime-400)' }}>Sustainable Tomorrow</span>
          </h1>

          <p style={{ color: '#d5e2d8', maxWidth: 480, marginBottom: 28, fontSize: 15 }}>
            AI-powered insights for healthier crops, higher yields and a greener future.
            Monitor diseases, weather, soil and sustainability — all in one place.
          </p>

          <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
            <Link to="/disease-detection" className="btn btn-accent">
              Get Started <ArrowRight size={15} />
            </Link>
            <Link to="/crop-recommendation" className="btn btn-outline"
              style={{ color: 'white', borderColor: 'rgba(255,255,255,0.3)' }}>
              Explore Modules
            </Link>
          </div>

          {/* Highlight pill */}
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              marginTop: 28,
              background: 'rgba(255,255,255,0.08)',
              border: '1px solid rgba(255,255,255,0.15)',
              borderRadius: 'var(--radius-full)',
              padding: '8px 16px',
              fontSize: 12,
              color: 'var(--lime-300)',
            }}
          >
            <Leaf size={13} />
            Healthy Fields · Sustainable Future
          </div>
        </div>
      </section>

      {/* ── Quick Metrics ────────────────────────────────────────────── */}
      <section className="section" aria-label="Quick metrics">
        <div className="metric-grid">
          <MetricCard
            icon={<Thermometer size={20} />}
            label="Temperature"
            value="—"
            sub="Visit Weather page for live data"
            iconBg="var(--warning-bg)"
            iconColor="var(--warning)"
          />
          <MetricCard
            icon={<Droplets size={20} />}
            label="Soil Moisture"
            value="—"
            sub="Enter conditions in Irrigation"
            iconBg="var(--info-bg)"
            iconColor="var(--info)"
          />
          <MetricCard
            icon={<Leaf size={20} />}
            label="Sustainability"
            value="—"
            sub="Run the Sustainability module"
            iconBg="var(--primary-100)"
            iconColor="var(--primary-700)"
          />
          <MetricCard
            icon={<CloudRain size={20} />}
            label="Rain Chance"
            value="—"
            sub="Check Weather Intelligence"
            iconBg="var(--primary-50)"
            iconColor="var(--primary-500)"
          />
        </div>
      </section>

      {/* ── Modules Grid ─────────────────────────────────────────────── */}
      <section className="section" aria-label="AI modules">
        <SectionHeader
          title="AI-Powered Modules"
          subtitle="Everything your farm needs, powered by machine learning"
        />
        <div className="module-grid">
          {MODULES.map(({ to, icon: Icon, iconBg, iconColor, title, desc }) => (
            <Link
              key={to}
              to={to}
              className="module-card"
              aria-label={`Go to ${title}`}
              style={{ textDecoration: 'none' }}
            >
              <div
                className="module-icon"
                style={{ background: iconBg, color: iconColor }}
                aria-hidden="true"
              >
                <Icon size={22} />
              </div>
              <h3 style={{ marginBottom: 6 }}>{title}</h3>
              <p style={{ fontSize: 13 }}>{desc}</p>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 4,
                  marginTop: 14,
                  fontSize: 12,
                  fontWeight: 600,
                  color: 'var(--primary-600)',
                }}
              >
                Open Module <ArrowRight size={13} />
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* ── Farm Intelligence row ─────────────────────────────────────── */}
      <section className="section" aria-label="Farm intelligence">
        <SectionHeader title="Farm Intelligence" subtitle="AI recommendations for today" />

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: 16,
          }}
        >
          {/* Weather hint */}
          <IntelCard
            icon={<CloudSun size={18} />}
            iconBg="var(--warning-bg)"
            iconColor="var(--warning)"
            title="Weather Intelligence"
            body="Get real-time weather forecasts and farming advice tailored to your location and crop conditions."
            linkTo="/weather"
            linkLabel="Check Weather"
          />

          {/* Disease hint */}
          <IntelCard
            icon={<Bug size={18} />}
            iconBg="var(--danger-bg)"
            iconColor="var(--danger)"
            title="Disease Detection"
            body="Upload a leaf image to detect diseases early and get treatment recommendations powered by AI."
            linkTo="/disease-detection"
            linkLabel="Analyze Crop"
          />

          {/* Irrigation hint */}
          <IntelCard
            icon={<Droplets size={18} />}
            iconBg="var(--info-bg)"
            iconColor="var(--info)"
            title="Smart Irrigation"
            body="Find out exactly when and how much to irrigate based on soil moisture, temperature and crop stage."
            linkTo="/smart-irrigation"
            linkLabel="Check Irrigation"
          />
        </div>
      </section>

      {/* ── Quick Sustainability Overview ────────────────────────────── */}
      <section className="section" aria-label="Sustainability overview">
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: 16,
          }}
        >
          {/* Score teaser */}
          <div
            className="card"
            style={{ padding: 28, display: 'flex', alignItems: 'center', gap: 28 }}
          >
            <div
              style={{
                width: 100,
                height: 100,
                flexShrink: 0,
                borderRadius: '50%',
                background:
                  'conic-gradient(var(--primary-600) 0%, var(--primary-100) 0%)',
                display: 'grid',
                placeItems: 'center',
                position: 'relative',
              }}
              aria-hidden="true"
            >
              <div
                style={{
                  position: 'absolute',
                  width: 78,
                  height: 78,
                  borderRadius: '50%',
                  background: 'var(--surface)',
                }}
              />
              <Leaf
                size={28}
                color="var(--primary-400)"
                style={{ position: 'relative', zIndex: 1 }}
              />
            </div>
            <div>
              <div style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 6 }}>
                Sustainability Score
              </div>
              <div
                style={{ fontSize: 26, fontWeight: 700, color: 'var(--primary-800)', marginBottom: 4 }}
              >
                Not computed yet
              </div>
              <p style={{ fontSize: 13, margin: 0 }}>
                Enter your farm data to calculate your sustainability score.
              </p>
              <Link to="/sustainability" className="btn btn-secondary" style={{ marginTop: 14, fontSize: 13 }}>
                Calculate Score
              </Link>
            </div>
          </div>

          {/* AI Assistant teaser */}
          <div
            className="card"
            style={{
              padding: 28,
              background: 'linear-gradient(135deg, var(--primary-950) 0%, var(--primary-800) 100%)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: 12,
                  background: 'var(--lime-500)',
                  display: 'grid',
                  placeItems: 'center',
                  color: 'var(--primary-950)',
                  marginBottom: 14,
                }}
                aria-hidden="true"
              >
                <MessageSquare size={18} />
              </div>
              <h3 style={{ color: 'white', marginBottom: 8 }}>Farming Questions?<br />We're Here 24/7</h3>
              <p style={{ fontSize: 13, color: '#b8c8bc', margin: 0 }}>
                Ask about diseases, irrigation, crop selection, weather impacts and more.
              </p>
            </div>
            <Link
              to="/assistant"
              className="btn btn-accent"
              style={{ marginTop: 20, alignSelf: 'flex-start' }}
            >
              Chat with AI <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </section>

      {/* ── Demo workflow story ──────────────────────────────────────── */}
      <section className="section" aria-label="How AgriSmart works">
        <SectionHeader
          title="How AgriSmart Works"
          subtitle="A complete intelligent farming workflow"
        />
        <div
          className="card"
          style={{ padding: '28px 32px' }}
        >
          <div
            style={{
              display: 'flex',
              gap: 0,
              overflowX: 'auto',
              paddingBottom: 4,
            }}
          >
            {WORKFLOW_STEPS.map((step, i) => (
              <WorkflowStep key={i} step={step} isLast={i === WORKFLOW_STEPS.length - 1} />
            ))}
          </div>
        </div>
      </section>

    </div>
  )
}

/* ── Sub-components ──────────────────────────────────────────────────────── */

function IntelCard({ icon, iconBg, iconColor, title, body, linkTo, linkLabel }) {
  return (
    <div className="recommendation-card card-hover" style={{ padding: 22 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12 }}>
        <div
          style={{
            width: 34,
            height: 34,
            borderRadius: 10,
            background: iconBg,
            color: iconColor,
            display: 'grid',
            placeItems: 'center',
          }}
          aria-hidden="true"
        >
          {icon}
        </div>
        <span className="recommendation-title" style={{ fontSize: 15 }}>{title}</span>
      </div>
      <p className="recommendation-text" style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
        {body}
      </p>
      <Link
        to={linkTo}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: 4,
          marginTop: 14,
          fontSize: 12,
          fontWeight: 600,
          color: 'var(--primary-600)',
        }}
      >
        {linkLabel} <ArrowRight size={12} />
      </Link>
    </div>
  )
}

const WORKFLOW_STEPS = [
  { icon: <Bug size={16} />,         label: 'Upload Leaf',      desc: 'Disease detected' },
  { icon: <CloudSun size={16} />,    label: 'Check Weather',    desc: 'Forecast fetched' },
  { icon: <Droplets size={16} />,    label: 'Irrigation',       desc: 'Decision made' },
  { icon: <Sprout size={16} />,      label: 'Crop Selection',   desc: 'Best crop found' },
  { icon: <Leaf size={16} />,        label: 'Sustainability',   desc: 'Score calculated' },
  { icon: <MessageSquare size={16}/>,label: 'AI Explains',      desc: 'All in one chat' },
]

function WorkflowStep({ step, isLast }) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 0,
        flex: '0 0 auto',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 8,
          minWidth: 90,
          padding: '0 8px',
        }}
      >
        <div
          style={{
            width: 44,
            height: 44,
            borderRadius: '50%',
            background: 'var(--primary-100)',
            color: 'var(--primary-700)',
            display: 'grid',
            placeItems: 'center',
            border: '2px solid var(--primary-200)',
          }}
          aria-hidden="true"
        >
          {step.icon}
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-primary)' }}>
            {step.label}
          </div>
          <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{step.desc}</div>
        </div>
      </div>

      {!isLast && (
        <div
          style={{
            width: 28,
            height: 2,
            background: 'var(--border-green)',
            flexShrink: 0,
            marginBottom: 22,
          }}
          aria-hidden="true"
        />
      )}
    </div>
  )
}
