'use client'

import { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'
import type { PredictedCode, ActivatedConcept } from '@/types'
import { ConfidenceBar } from '@/components/shared/ConfidenceBar'
import { ConceptBadge } from '@/components/shared/ConceptBadge'
import { cn } from '@/lib/utils'

interface PredictionPanelProps {
  predictions: PredictedCode[]
  activatedConcepts: ActivatedConcept[]
  onSelectCode?: (code: string | null) => void
  selectedCode?: string | null
}

const TOP_N_EXPANDED = 15  // Show top 15 codes by default

export function PredictionPanel({
  predictions,
  activatedConcepts,
  onSelectCode,
  selectedCode,
}: PredictionPanelProps) {
  const [expandedCode, setExpandedCode] = useState<string | null>(null)
  const [showAll, setShowAll] = useState(false)

  const aboveThreshold = predictions.filter(p => p.above_threshold)
  const displayed = showAll ? predictions : predictions.slice(0, TOP_N_EXPANDED)

  function toggleExpand(code: string) {
    const next = expandedCode === code ? null : code
    setExpandedCode(next)
    onSelectCode?.(next)
  }

  // For a given ICD-10 code, find most relevant concepts (top 5 by score among active ones)
  function getTopConceptsForCode(code: string): ActivatedConcept[] {
    return activatedConcepts
      .filter(c => c.active)
      .slice(0, 5)
  }

  return (
    <div className="space-y-2">
      {/* Summary header */}
      <div className="flex items-center justify-between mb-3">
        <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>
          <span className="font-semibold" style={{ color: 'var(--accent)' }}>
            {aboveThreshold.length}
          </span>{' '}
          of {predictions.length} codes above threshold
        </p>
      </div>

      {displayed.map((pred, i) => (
        <div
          key={pred.code}
          className={cn(
            'animate-fade-in',
            'rounded-xl border transition-all duration-150 overflow-hidden',
            pred.above_threshold
              ? pred.rank === 1
                ? 'border-[rgba(78,205,196,0.3)] bg-white/[0.04]'
                : 'border-[var(--glass-border)] bg-white/[0.03]'
              : 'border-white/[0.04] bg-transparent opacity-50'
          )}
          style={{
            animationDelay: `${i * 50}ms`,
            animationFillMode: 'backwards',
            ...(pred.rank === 1 && pred.above_threshold ? {
              borderLeft: '2px solid #4ecdc4',
              boxShadow: '0 0 20px rgba(78,205,196,0.06), inset 3px 0 12px rgba(78,205,196,0.08)',
            } : {}),
          }}
        >
          {/* Row */}
          <button
            type="button"
            onClick={() => pred.above_threshold && toggleExpand(pred.code)}
            className={cn(
              'w-full flex items-center gap-3 px-4 py-3 text-left',
              pred.above_threshold && 'hover:bg-white/[0.03] cursor-pointer'
            )}
          >
            {/* Rank */}
            <span
              className={cn(
                'text-2xl font-bold w-8 shrink-0 tabular-nums',
                pred.rank === 1 && pred.above_threshold ? 'gradient-text' : ''
              )}
              style={pred.rank === 1 && pred.above_threshold ? {} : { color: 'var(--text-muted)' }}
            >
              {pred.rank}
            </span>

            {/* Code + description */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="font-mono text-sm font-semibold" style={{ color: 'var(--accent)' }}>
                  {pred.code}
                </span>
                {pred.above_threshold && (
                  <span
                    className="text-xs px-1.5 py-0.5 rounded-md"
                    style={{
                      background: 'var(--accent-dim)',
                      color: 'var(--accent)',
                    }}
                  >
                    active
                  </span>
                )}
              </div>
              <p className="text-sm truncate" style={{ color: 'var(--text-primary)' }}>
                {pred.description}
              </p>
            </div>

            {/* Confidence */}
            <div className="shrink-0 text-right">
              {pred.rank === 1 && pred.above_threshold ? (
                <>
                  <p className="text-xl font-bold tabular-nums gradient-text leading-none">
                    {(pred.confidence * 100).toFixed(0)}%
                  </p>
                  <p className="text-xs mt-1 font-mono" style={{ color: 'var(--text-muted)' }}>
                    confidence
                  </p>
                </>
              ) : (
                <div className="w-20 sm:w-28">
                  <ConfidenceBar value={pred.confidence} />
                  <p className="text-xs mt-1 text-right font-mono" style={{ color: 'var(--text-muted)' }}>
                    thr: {(pred.threshold * 100).toFixed(0)}%
                  </p>
                </div>
              )}
            </div>

            {pred.above_threshold && (
              expandedCode === pred.code
                ? <ChevronUp className="w-4 h-4 shrink-0" style={{ color: 'var(--text-muted)' }} />
                : <ChevronDown className="w-4 h-4 shrink-0" style={{ color: 'var(--text-muted)' }} />
            )}
          </button>

          {/* Expanded: concept attribution */}
          {expandedCode === pred.code && (
            <div
              className="px-4 pb-4 border-t"
              style={{ borderColor: 'var(--glass-border)' }}
            >
              <p className="text-xs mb-2 mt-3" style={{ color: 'var(--text-secondary)' }}>
                Contributing concepts
              </p>
              <div className="flex flex-wrap gap-1.5">
                {getTopConceptsForCode(pred.code).map(c => (
                  <ConceptBadge key={c.concept} concept={c.concept} score={c.score} />
                ))}
              </div>
            </div>
          )}
        </div>
      ))}

      {/* Show more / less */}
      {predictions.length > TOP_N_EXPANDED && (
        <button
          type="button"
          onClick={() => setShowAll(!showAll)}
          className="w-full py-2 text-xs rounded-xl transition-colors"
          style={{
            color: 'var(--text-muted)',
            border: '1px solid var(--glass-border)',
            background: 'transparent',
          }}
          onMouseEnter={e => (e.currentTarget.style.color = 'var(--text-secondary)')}
          onMouseLeave={e => (e.currentTarget.style.color = 'var(--text-muted)')}
        >
          {showAll ? 'Show fewer codes' : `Show all ${predictions.length} codes`}
        </button>
      )}
    </div>
  )
}
