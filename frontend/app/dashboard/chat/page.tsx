'use client'

import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { RotateCcw } from 'lucide-react'
import { GlassCard } from '@/components/shared/GlassCard'
import { ChatPanel } from '@/components/chat/ChatPanel'
import { ChatInput } from '@/components/chat/ChatInput'
import { ContextSidebar } from '@/components/chat/ContextSidebar'
import { useChat } from '@/hooks/useChat'
import { predict } from '@/lib/api'
import type { PredictResponse } from '@/types'

export default function ChatPage() {
  const searchParams = useSearchParams()
  const predictionId = searchParams.get('prediction_id')

  const [predictionContext, setPredictionContext] = useState<PredictResponse | null>(null)
  const [loadingContext, setLoadingContext] = useState(false)

  const { messages, streaming, error, sendMessage, reset } = useChat({ predictionId })

  // Load prediction context from Supabase for the sidebar
  useEffect(() => {
    if (!predictionId) return
    setLoadingContext(true)

    // We fetch the prediction via the predict endpoint indirectly —
    // the backend fetches it when building the system prompt.
    // For the sidebar, we load it directly from the notes API as a best-effort.
    // In a full implementation this would be a GET /api/predictions/{id} endpoint (Part 4).
    // For now we surface the prediction_id as context cue.
    setLoadingContext(false)
  }, [predictionId])

  return (
    <div
      className="fixed inset-0 flex flex-col"
      style={{
        top: '64px',     // header height
        left: '64px',    // sidebar width
        background: 'var(--bg-deep)',
      }}
    >
      <div className="flex flex-1 overflow-hidden">
        {/* ── Main chat area ── */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Top bar */}
          <div
            className="flex items-center justify-between px-5 py-3 shrink-0 border-b border-white/[0.06]"
            style={{ background: 'var(--glass-bg)', backdropFilter: 'blur(20px)' }}
          >
            <div>
              <h2 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                Clinical Assistant
              </h2>
              {predictionId ? (
                <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                  Grounded in prediction{' '}
                  <span className="font-mono">{predictionId.slice(0, 8)}…</span>
                </p>
              ) : (
                <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                  General session — no prediction context
                </p>
              )}
            </div>

            {messages.length > 0 && (
              <button
                onClick={reset}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-colors"
                style={{
                  background: 'var(--glass-bg)',
                  border: '1px solid var(--glass-border)',
                  color: 'var(--text-muted)',
                }}
                onMouseEnter={e => (e.currentTarget.style.color = 'var(--text-secondary)')}
                onMouseLeave={e => (e.currentTarget.style.color = 'var(--text-muted)')}
              >
                <RotateCcw className="w-3.5 h-3.5" />
                New chat
              </button>
            )}
          </div>

          {/* Messages */}
          <ChatPanel messages={messages} streaming={streaming} />

          {/* Error banner */}
          {error && (
            <div
              className="mx-4 mb-2 px-4 py-2 rounded-xl text-xs"
              style={{
                background: 'rgba(255,107,107,0.1)',
                border: '1px solid rgba(255,107,107,0.3)',
                color: 'var(--accent-warm)',
              }}
            >
              {error}
            </div>
          )}

          {/* Input */}
          <div className="px-4 py-4 shrink-0">
            <ChatInput
              onSend={sendMessage}
              disabled={streaming}
              placeholder={
                predictionId
                  ? 'Ask about the predictions, differentials, workup…'
                  : 'Ask ShifaMind anything about clinical AI…'
              }
            />
            <p className="text-center text-xs mt-2" style={{ color: 'var(--text-muted)' }}>
              AI-generated content — not a substitute for clinical judgment
            </p>
          </div>
        </div>

        {/* ── Context sidebar ── */}
        <ContextSidebar
          predictionId={predictionId}
          prediction={predictionContext}
          loadingPrediction={loadingContext}
        />
      </div>
    </div>
  )
}
