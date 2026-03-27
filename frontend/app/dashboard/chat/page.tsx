'use client'

import { Suspense, useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { RotateCcw } from 'lucide-react'
import { ChatPanel } from '@/components/chat/ChatPanel'
import { ChatInput } from '@/components/chat/ChatInput'
import { ContextSidebar } from '@/components/chat/ContextSidebar'
import { useChat } from '@/hooks/useChat'
import { createClient } from '@/lib/supabase/client'
import type { PredictResponse } from '@/types'

export default function ChatPage() {
  return (
    <Suspense>
      <ChatContent />
    </Suspense>
  )
}

function ChatContent() {
  const searchParams = useSearchParams()
  const isDemo = searchParams.get('demo') === 'true'
  const predictionId = isDemo ? null : searchParams.get('prediction_id')

  const [predictionContext, setPredictionContext] = useState<PredictResponse | null>(null)
  const [loadingContext, setLoadingContext] = useState(false)

  const { messages, streaming, error, isDemo: chatIsDemo, sendMessage, reset } = useChat({
    predictionId,
    predictionContext,
  })

  // Load prediction context — from sessionStorage (demo) or Supabase (real)
  useEffect(() => {
    if (isDemo) {
      try {
        const stored = sessionStorage.getItem('shifamind_demo_prediction')
        if (stored) setPredictionContext(JSON.parse(stored) as PredictResponse)
      } catch {
        // sessionStorage unavailable — proceed without context
      }
      return
    }

    if (!predictionId) return
    setLoadingContext(true)
    const supabase = createClient()
    supabase
      .from('predictions')
      .select('*')
      .eq('id', predictionId)
      .single()
      .then(({ data }) => {
        if (data) {
          setPredictionContext({
            prediction_id: data.id,
            predictions: data.predicted_codes ?? [],
            activated_concepts: data.activated_concepts ?? [],
            metadata: {
              inference_time_ms: data.inference_time_ms ?? 0,
              model_version: 'phase1_v1',
              threshold_source: 'tuned',
            },
          })
        }
        setLoadingContext(false)
      })
  }, [isDemo, predictionId])

  const showDemoTag = isDemo || chatIsDemo

  return (
    // -m-6 removes the layout's p-6, giving us edge-to-edge chat
    <div className="-m-6 flex flex-col" style={{ height: 'calc(100vh - 64px)' }}>
      <div className="flex flex-1 overflow-hidden">
        {/* Main chat area */}
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
              <div className="flex items-center gap-2">
                {isDemo ? (
                  <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                    Demo prediction context
                  </p>
                ) : predictionId ? (
                  <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                    Grounded in prediction{' '}
                    <span className="font-mono">{predictionId.slice(0, 8)}…</span>
                  </p>
                ) : (
                  <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                    General session — no prediction context
                  </p>
                )}
                {showDemoTag && (
                  <span
                    className="text-xs px-2 py-0.5 rounded-full"
                    style={{ background: 'rgba(255,217,61,0.1)', color: 'var(--accent-gold)' }}
                  >
                    Demo
                  </span>
                )}
              </div>
            </div>

            {messages.length > 0 && (
              <button
                onClick={reset}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs transition-colors"
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
          <ChatPanel
            messages={messages}
            streaming={streaming}
            onSuggestionClick={sendMessage}
          />

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
                isDemo || predictionId
                  ? 'Ask about the predictions, differentials, workup…'
                  : 'Ask ShifaMind anything about clinical AI…'
              }
            />
            <p className="text-center text-xs mt-2" style={{ color: 'var(--text-muted)' }}>
              AI-generated content — not a substitute for clinical judgment
            </p>
          </div>
        </div>

        {/* Context sidebar — hidden on mobile */}
        <div className="hidden lg:block">
          <ContextSidebar
            predictionId={predictionId}
            prediction={predictionContext}
            loadingPrediction={loadingContext}
          />
        </div>
      </div>
    </div>
  )
}
