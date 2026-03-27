'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { History, MessageSquare, ChevronDown, ChevronUp, FlaskConical } from 'lucide-react'
import { createClient } from '@/lib/supabase/client'
import { GlassCard } from '@/components/shared/GlassCard'
import { ConfidenceBar } from '@/components/shared/ConfidenceBar'
import { ConceptBadge } from '@/components/shared/ConceptBadge'
import { MOCK_SCENARIOS, MOCK_NOTES } from '@/lib/mock-data'

interface PredictionRow {
  id: string
  note_source: 'sample' | 'custom'
  input_text: string
  predicted_codes: Array<{
    rank: number; code: string; description: string
    confidence: number; above_threshold: boolean
  }>
  activated_concepts: Array<{ concept: string; score: number; active: boolean }>
  inference_time_ms: number
  created_at: string
}

// Demo fallback — one entry per sample note, spread over the past week
const SCENARIO_KEYS = ['heart_failure', 'pneumonia', 'aki', 'sepsis', 'stroke'] as const
const MOCK_HISTORY: PredictionRow[] = MOCK_NOTES.map((note, i) => {
  const scenario = MOCK_SCENARIOS[SCENARIO_KEYS[i]]
  const daysAgo = i * 1.5
  return {
    id: `demo-${note.id}`,
    note_source: 'sample',
    input_text: note.text,
    predicted_codes: scenario.predictions,
    activated_concepts: scenario.activated_concepts,
    inference_time_ms: scenario.metadata.inference_time_ms,
    created_at: new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000).toISOString(),
  }
})

function PredictionCard({ prediction, isDemo }: { prediction: PredictionRow; isDemo: boolean }) {
  const [expanded, setExpanded] = useState(false)
  const codes = Array.isArray(prediction.predicted_codes) ? prediction.predicted_codes : []
  const concepts = Array.isArray(prediction.activated_concepts) ? prediction.activated_concepts : []
  const top = codes.filter(p => p.above_threshold).slice(0, 3)
  const topConcepts = concepts.filter(c => c.active).slice(0, 6)
  const date = new Date(prediction.created_at)

  return (
    <GlassCard className="overflow-hidden">
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-start gap-4 p-4 hover:bg-white/[0.02] transition-colors text-left"
      >
        {/* Icon */}
        <div
          className="w-9 h-9 rounded-xl flex items-center justify-center shrink-0 mt-0.5"
          style={{ background: 'var(--accent-dim)' }}
        >
          <FlaskConical className="w-4 h-4" style={{ color: 'var(--accent)' }} />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Top codes pills */}
          <div className="flex flex-wrap gap-1.5 mb-2">
            {top.map(p => (
              <span
                key={p.code}
                className="font-mono text-xs px-2 py-0.5 rounded-full"
                style={{ background: 'var(--accent-dim)', color: 'var(--accent)' }}
              >
                {p.code}
              </span>
            ))}
            {codes.filter(p => p.above_threshold).length > 3 && (
              <span className="text-xs px-2 py-0.5 rounded-full" style={{ background: 'var(--glass-bg)', color: 'var(--text-muted)' }}>
                +{codes.filter(p => p.above_threshold).length - 3} more
              </span>
            )}
          </div>
          {/* Note snippet */}
          <p className="text-xs leading-relaxed line-clamp-2 mb-2" style={{ color: 'var(--text-secondary)' }}>
            {prediction.input_text.slice(0, 180)}…
          </p>
          {/* Meta */}
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
              {date.toLocaleDateString()} {date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
            <span className="text-xs font-mono" style={{ color: 'var(--text-muted)' }}>
              {prediction.inference_time_ms}ms
            </span>
            <span
              className="text-xs px-1.5 py-0.5 rounded-md"
              style={{ background: 'var(--glass-bg)', color: 'var(--text-muted)' }}
            >
              {prediction.note_source}
            </span>
          </div>
        </div>

        {/* Actions + expand */}
        <div className="flex flex-wrap items-center gap-2 shrink-0">
          {!isDemo && (
            <Link
              href={`/dashboard/chat?prediction_id=${prediction.id}`}
              onClick={e => e.stopPropagation()}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl text-xs transition-colors"
              style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)', color: 'var(--text-secondary)' }}
              onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent)')}
              onMouseLeave={e => (e.currentTarget.style.color = 'var(--text-secondary)')}
            >
              <MessageSquare className="w-3 h-3" />
              Chat
            </Link>
          )}
          {expanded
            ? <ChevronUp className="w-4 h-4" style={{ color: 'var(--text-muted)' }} />
            : <ChevronDown className="w-4 h-4" style={{ color: 'var(--text-muted)' }} />
          }
        </div>
      </button>

      {/* Expanded detail */}
      {expanded && (
        <div className="px-4 pb-4 border-t space-y-4" style={{ borderColor: 'var(--glass-border)' }}>
          {/* Top diagnoses */}
          <div className="pt-4">
            <p className="text-xs font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
              Top diagnoses
            </p>
            <div className="space-y-2">
              {codes.filter(p => p.above_threshold).slice(0, 6).map(p => (
                <div key={p.code} className="flex items-center gap-3">
                  <span className="font-mono text-xs w-16 shrink-0" style={{ color: 'var(--accent)' }}>{p.code}</span>
                  <span className="text-xs flex-1 truncate" style={{ color: 'var(--text-primary)' }}>{p.description}</span>
                  <div className="w-16 sm:w-24 shrink-0"><ConfidenceBar value={p.confidence} /></div>
                </div>
              ))}
            </div>
          </div>

          {/* Active concepts */}
          {topConcepts.length > 0 && (
            <div>
              <p className="text-xs font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                Activated concepts
              </p>
              <div className="flex flex-wrap gap-1.5">
                {topConcepts.map(c => (
                  <ConceptBadge key={c.concept} concept={c.concept} score={c.score} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </GlassCard>
  )
}

function HistorySkeleton() {
  return (
    <div className="space-y-3">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="skeleton h-24 rounded-2xl" />
      ))}
    </div>
  )
}

export default function HistoryPage() {
  const [predictions, setPredictions] = useState<PredictionRow[]>([])
  const [loading, setLoading] = useState(true)
  const [hasMore, setHasMore] = useState(false)
  const [isDemo, setIsDemo] = useState(false)
  const PAGE = 20

  useEffect(() => {
    async function load() {
      try {
        const supabase = createClient()
        const { data, error } = await supabase
          .from('predictions')
          .select('id,note_source,input_text,predicted_codes,activated_concepts,inference_time_ms,created_at')
          .order('created_at', { ascending: false })
          .limit(PAGE + 1)

        if (error) throw error
        const rows = data ?? []
        setHasMore(rows.length > PAGE)
        setPredictions(rows.slice(0, PAGE) as PredictionRow[])
      } catch {
        // Supabase not configured — fall back to demo history
        setPredictions(MOCK_HISTORY)
        setIsDemo(true)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div className="max-w-3xl mx-auto px-2 sm:px-0 animate-fade-in">
      <div className="flex items-center justify-between mb-6 gap-2 flex-wrap">
        <div>
          <h1 className="text-xl font-semibold" style={{ color: 'var(--text-primary)' }}>History</h1>
          <p className="text-sm mt-0.5" style={{ color: 'var(--text-secondary)' }}>
            Your past predictions and analyses
          </p>
        </div>
        <div className="flex items-center gap-2">
          {isDemo && (
            <span className="text-xs px-2 py-0.5 rounded-full" style={{ background: 'rgba(255,217,61,0.1)', color: 'var(--accent-gold)' }}>
              Demo
            </span>
          )}
          {predictions.length > 0 && (
            <span className="text-sm" style={{ color: 'var(--text-muted)' }}>
              {predictions.length}{hasMore ? '+' : ''} predictions
            </span>
          )}
        </div>
      </div>

      {loading && <HistorySkeleton />}
      {!loading && predictions.length > 0 && (
        <div className="space-y-3">
          {predictions.map((p, i) => (
            <div
              key={p.id}
              className="animate-fade-in"
              style={{ animationDelay: `${i * 40}ms`, animationFillMode: 'backwards' }}
            >
              <PredictionCard prediction={p} isDemo={isDemo} />
            </div>
          ))}
          {hasMore && (
            <p className="text-center text-xs py-2" style={{ color: 'var(--text-muted)' }}>
              Showing latest {PAGE} predictions
            </p>
          )}
        </div>
      )}
    </div>
  )
}
