'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { History, MessageSquare, ChevronDown, ChevronUp, FlaskConical } from 'lucide-react'
import { createClient } from '@/lib/supabase/client'
import { GlassCard } from '@/components/shared/GlassCard'
import { ConfidenceBar } from '@/components/shared/ConfidenceBar'
import { ConceptBadge } from '@/components/shared/ConceptBadge'

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

function PredictionCard({ prediction }: { prediction: PredictionRow }) {
  const [expanded, setExpanded] = useState(false)
  const top = prediction.predicted_codes.filter(p => p.above_threshold).slice(0, 3)
  const topConcepts = prediction.activated_concepts.filter(c => c.active).slice(0, 6)
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
                className="font-mono text-xs px-2 py-0.5 rounded-lg"
                style={{ background: 'var(--accent-dim)', color: 'var(--accent)' }}
              >
                {p.code}
              </span>
            ))}
            {prediction.predicted_codes.filter(p => p.above_threshold).length > 3 && (
              <span className="text-xs px-2 py-0.5 rounded-lg" style={{ background: 'var(--glass-bg)', color: 'var(--text-muted)' }}>
                +{prediction.predicted_codes.filter(p => p.above_threshold).length - 3} more
              </span>
            )}
          </div>
          {/* Note snippet */}
          <p className="text-xs leading-relaxed line-clamp-2 mb-2" style={{ color: 'var(--text-secondary)' }}>
            {prediction.input_text.slice(0, 180)}…
          </p>
          {/* Meta */}
          <div className="flex items-center gap-3">
            <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
              {date.toLocaleDateString()} {date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
            <span className="text-xs font-mono" style={{ color: 'var(--text-muted)' }}>
              {prediction.inference_time_ms}ms
            </span>
            <span
              className="text-xs px-1.5 py-0.5 rounded"
              style={{ background: 'var(--glass-bg)', color: 'var(--text-muted)' }}
            >
              {prediction.note_source}
            </span>
          </div>
        </div>

        {/* Actions + expand */}
        <div className="flex items-center gap-2 shrink-0">
          <Link
            href={`/dashboard/chat?prediction_id=${prediction.id}`}
            onClick={e => e.stopPropagation()}
            className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs transition-colors"
            style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)', color: 'var(--text-secondary)' }}
            onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent)')}
            onMouseLeave={e => (e.currentTarget.style.color = 'var(--text-secondary)')}
          >
            <MessageSquare className="w-3 h-3" />
            Chat
          </Link>
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
              {prediction.predicted_codes.filter(p => p.above_threshold).slice(0, 6).map(p => (
                <div key={p.code} className="flex items-center gap-3">
                  <span className="font-mono text-xs w-16 shrink-0" style={{ color: 'var(--accent)' }}>{p.code}</span>
                  <span className="text-xs flex-1 truncate" style={{ color: 'var(--text-primary)' }}>{p.description}</span>
                  <div className="w-24 shrink-0"><ConfidenceBar value={p.confidence} /></div>
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

function EmptyHistory() {
  return (
    <GlassCard className="p-12 flex flex-col items-center justify-center text-center">
      <div className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
        style={{ background: 'rgba(255,217,61,0.1)' }}>
        <History className="w-7 h-7" style={{ color: 'var(--accent-gold)' }} />
      </div>
      <h3 className="font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>No predictions yet</h3>
      <p className="text-sm mb-5" style={{ color: 'var(--text-secondary)' }}>
        Run your first analysis to see it here.
      </p>
      <Link
        href="/dashboard/workspace"
        className="px-5 py-2.5 rounded-xl text-sm font-medium transition-all"
        style={{ background: '#4ecdc4', color: '#060a13' }}
      >
        Go to Workspace →
      </Link>
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
  const PAGE = 20

  useEffect(() => {
    const supabase = createClient()
    supabase
      .from('predictions')
      .select('id,note_source,input_text,predicted_codes,activated_concepts,inference_time_ms,created_at')
      .order('created_at', { ascending: false })
      .limit(PAGE + 1)
      .then(({ data }) => {
        const rows = data ?? []
        setHasMore(rows.length > PAGE)
        setPredictions(rows.slice(0, PAGE) as PredictionRow[])
        setLoading(false)
      })
  }, [])

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold" style={{ color: 'var(--text-primary)' }}>History</h1>
          <p className="text-sm mt-0.5" style={{ color: 'var(--text-secondary)' }}>
            Your past predictions and analyses
          </p>
        </div>
        {predictions.length > 0 && (
          <span className="text-sm" style={{ color: 'var(--text-muted)' }}>
            {predictions.length}{hasMore ? '+' : ''} predictions
          </span>
        )}
      </div>

      {loading && <HistorySkeleton />}
      {!loading && predictions.length === 0 && <EmptyHistory />}
      {!loading && predictions.length > 0 && (
        <div className="space-y-3">
          {predictions.map(p => <PredictionCard key={p.id} prediction={p} />)}
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
