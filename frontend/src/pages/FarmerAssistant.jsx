import React, { useState, useRef, useEffect } from 'react'
import { Send, MessageSquare, User, Sprout, Leaf, Droplets, CloudSun, RotateCcw } from 'lucide-react'
import { assistantAPI } from '../services/api.js'

/* ─── Suggested quick prompts ──────────────────────────────────────────────── */
const QUICK_PROMPTS = [
  { icon: <Sprout size={13} />,   text: 'Suggest best crops for my farm' },
  { icon: <Droplets size={13} />, text: 'When should I irrigate?' },
  { icon: <Leaf size={13} />,     text: 'How can I prevent tomato early blight?' },
  { icon: <CloudSun size={13} />, text: 'Will rain affect my harvest?' },
  { icon: <Leaf size={13} />,     text: 'How to improve soil health?' },
  { icon: <Sprout size={13} />,   text: 'Sustainability tips for my farm' },
]

/* ─── Context form defaults ────────────────────────────────────────────────── */
const CROP_OPTIONS  = ['Tomato', 'Wheat', 'Potato', 'Rice', 'Cotton', 'Maize', 'Groundnut']
const STAGE_OPTIONS = ['Germination', 'Seedling', 'Vegetative', 'Flowering', 'Maturation', 'Harvest']
const LANG_OPTIONS  = [{ value: 'en', label: 'English' }, { value: 'hi', label: 'हिंदी' }, { value: 'gu', label: 'ગુજરાતી' }]

const WELCOME_MSG = {
  id: 'welcome',
  role: 'assistant',
  text: `Hello, Farmer! 👋\n\nI'm your AgriSmart AI assistant. Ask me anything about your crops, irrigation, diseases, weather or sustainability — in English, Hindi or Gujarati.\n\nTry one of the suggestions below or type your own question.`,
}

export default function FarmerAssistant() {
  const [messages, setMessages]     = useState([WELCOME_MSG])
  const [input, setInput]           = useState('')
  const [loading, setLoading]       = useState(false)
  const [context, setContext]       = useState({
    farm_id: 'farm_001',
    crop_name: 'Tomato',
    growth_stage: 'Vegetative',
    soil_moisture: 45,
    language: 'en',
  })
  const [showContext, setShowContext] = useState(false)
  const bottomRef = useRef(null)
  const inputRef  = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const sendMessage = async (text) => {
    const trimmed = (text || input).trim()
    if (!trimmed || loading) return

    const userMsg = { id: Date.now(), role: 'user', text: trimmed }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const payload = {
        farm_id: context.farm_id,
        message: trimmed,
        language: context.language,
        crop_name: context.crop_name || undefined,
        growth_stage: context.growth_stage || undefined,
        soil_moisture: context.soil_moisture ? Number(context.soil_moisture) : undefined,
      }
      const { data } = await assistantAPI.chat(payload)
      const aiMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        text: data.answer,
        grounded: data.grounded,
        warning: data.warning,
        contextUsed: data.context_used,
      }
      setMessages(prev => [...prev, aiMsg])
    } catch (err) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        text: `I'm having trouble connecting to the AI service right now. Please make sure the backend is running and try again.\n\nError: ${err.message}`,
        isError: true,
      }])
    } finally {
      setLoading(false)
      setTimeout(() => inputRef.current?.focus(), 100)
    }
  }

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const clearChat = () => setMessages([WELCOME_MSG])

  return (
    <div className="page-enter" style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 120px)', gap: 16 }}>

      {/* ── Header row ─────────────────────────────────────────── */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 10 }}>
        <p style={{ fontSize: 14, color: 'var(--text-secondary)', margin: 0, maxWidth: 500 }}>
          Ask questions in plain language. Responses are grounded in your farm context.
        </p>
        <div style={{ display: 'flex', gap: 8 }}>
          <button
            className="btn btn-outline"
            style={{ fontSize: 12, padding: '0 14px', minHeight: 36 }}
            onClick={() => setShowContext(s => !s)}
            aria-expanded={showContext}
            aria-controls="context-panel"
          >
            {showContext ? 'Hide Context' : 'Farm Context'}
          </button>
          <button className="btn btn-outline" style={{ fontSize: 12, padding: '0 14px', minHeight: 36 }} onClick={clearChat} aria-label="Clear chat history">
            <RotateCcw size={13} /> Clear
          </button>
        </div>
      </div>

      {/* ── Context panel (collapsible) ───────────────────────── */}
      {showContext && (
        <div id="context-panel" className="card" style={{ padding: '16px 20px' }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 12 }}>
            Farm Context — used to ground AI responses
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 12 }}>
            <CtxField label="Farm ID">
              <input className="input" value={context.farm_id} onChange={e => setContext(p => ({ ...p, farm_id: e.target.value }))}
                style={{ padding: '8px 10px', fontSize: 13 }} />
            </CtxField>
            <CtxField label="Crop">
              <select className="select" value={context.crop_name} onChange={e => setContext(p => ({ ...p, crop_name: e.target.value }))}
                style={{ padding: '8px 10px', fontSize: 13 }}>
                {CROP_OPTIONS.map(c => <option key={c}>{c}</option>)}
              </select>
            </CtxField>
            <CtxField label="Growth Stage">
              <select className="select" value={context.growth_stage} onChange={e => setContext(p => ({ ...p, growth_stage: e.target.value }))}
                style={{ padding: '8px 10px', fontSize: 13 }}>
                {STAGE_OPTIONS.map(s => <option key={s}>{s}</option>)}
              </select>
            </CtxField>
            <CtxField label="Soil Moisture %">
              <input type="number" className="input" value={context.soil_moisture} min={0} max={100}
                onChange={e => setContext(p => ({ ...p, soil_moisture: e.target.value }))}
                style={{ padding: '8px 10px', fontSize: 13 }} />
            </CtxField>
            <CtxField label="Language">
              <select className="select" value={context.language} onChange={e => setContext(p => ({ ...p, language: e.target.value }))}
                style={{ padding: '8px 10px', fontSize: 13 }}>
                {LANG_OPTIONS.map(l => <option key={l.value} value={l.value}>{l.label}</option>)}
              </select>
            </CtxField>
          </div>
        </div>
      )}

      {/* ── Chat area ─────────────────────────────────────────── */}
      <div
        className="card"
        style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', minHeight: 0 }}
      >
        {/* Messages scroll area */}
        <div
          className="chat-messages"
          style={{ flex: 1, minHeight: 0, maxHeight: 'none' }}
          aria-live="polite"
          aria-label="Chat messages"
          role="log"
        >
          {messages.map(msg => (
            <ChatBubble key={msg.id} msg={msg} />
          ))}

          {/* Typing indicator */}
          {loading && (
            <div style={{ alignSelf: 'flex-start' }}>
              <div style={{ fontSize: 11, color: 'var(--text-light)', marginBottom: 4, marginLeft: 4 }}>
                AgriSmart AI is typing…
              </div>
              <div className="typing-indicator" aria-label="AI is typing">
                <div className="typing-dot" /><div className="typing-dot" /><div className="typing-dot" />
              </div>
            </div>
          )}
          <div ref={bottomRef} aria-hidden="true" />
        </div>

        {/* Quick prompts */}
        <div style={{ padding: '12px 16px', borderTop: '1px solid var(--border-light)' }}>
          <div className="chip-list" style={{ marginBottom: 12 }}>
            {QUICK_PROMPTS.map(({ icon, text }) => (
              <button
                key={text}
                className="chip"
                onClick={() => sendMessage(text)}
                disabled={loading}
                type="button"
              >
                {icon} {text}
              </button>
            ))}
          </div>

          {/* Input row */}
          <div className="chat-input">
            <input
              ref={inputRef}
              className="input"
              placeholder="Type your question…"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={onKeyDown}
              disabled={loading}
              aria-label="Chat input"
              style={{ flex: 1, borderRadius: 'var(--radius-full)', padding: '10px 18px', fontSize: 14 }}
            />
            <button
              className="btn btn-primary"
              onClick={() => sendMessage()}
              disabled={loading || !input.trim()}
              aria-label="Send message"
              style={{ borderRadius: 'var(--radius-full)', width: 44, minHeight: 44, padding: 0 }}
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

/* ─── Chat bubble ──────────────────────────────────────────────────────────── */
function ChatBubble({ msg }) {
  const isUser = msg.role === 'user'

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: isUser ? 'flex-end' : 'flex-start', gap: 4 }}>
      {/* Avatar row */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexDirection: isUser ? 'row-reverse' : 'row' }}>
        <div style={{
          width: 24, height: 24, borderRadius: '50%',
          background: isUser ? 'var(--primary-700)' : 'var(--lime-500)',
          display: 'grid', placeItems: 'center',
          color: isUser ? 'white' : 'var(--primary-950)',
          flexShrink: 0,
        }} aria-hidden="true">
          {isUser ? <User size={13} /> : <MessageSquare size={13} />}
        </div>
        <span style={{ fontSize: 11, color: 'var(--text-light)', fontWeight: 600 }}>
          {isUser ? 'You' : 'AgriSmart AI'}
        </span>
      </div>

      {/* Bubble */}
      <div
        className={`chat-message ${isUser ? 'user' : 'assistant'}`}
        style={msg.isError ? { background: 'var(--danger-bg)', color: 'var(--danger)' } : {}}
        role={isUser ? undefined : 'article'}
        aria-label={isUser ? 'Your message' : 'AI response'}
      >
        {/* Render line breaks */}
        {msg.text.split('\n').map((line, i) => (
          <React.Fragment key={i}>
            {line}
            {i < msg.text.split('\n').length - 1 && <br />}
          </React.Fragment>
        ))}
      </div>

      {/* Grounding badge */}
      {!isUser && msg.grounded !== undefined && (
        <span style={{ fontSize: 10, color: msg.grounded ? 'var(--success)' : 'var(--text-light)', marginLeft: 30 }}>
          {msg.grounded ? '✓ Grounded in farm data' : 'General advice'}
        </span>
      )}
      {!isUser && msg.warning && (
        <span style={{ fontSize: 10, color: 'var(--warning)', marginLeft: 30 }}>
          ⚠ {msg.warning}
        </span>
      )}
    </div>
  )
}

function CtxField({ label, children }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      <label style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-muted)' }}>{label}</label>
      {children}
    </div>
  )
}
