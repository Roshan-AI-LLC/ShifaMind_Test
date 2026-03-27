'use client'

import { useState } from 'react'
import type { ActivatedConcept } from '@/types'
import { ConceptBadge } from '@/components/shared/ConceptBadge'
import { ConfidenceBar } from '@/components/shared/ConfidenceBar'
import { cn } from '@/lib/utils'

interface ConceptPanelProps {
  concepts: ActivatedConcept[]
  onSelectConcept?: (concept: string | null) => void
  selectedConcept?: string | null
}

type ViewMode = 'pills' | 'bars'

export function ConceptPanel({ concepts, onSelectConcept, selectedConcept }: ConceptPanelProps) {
  const [mode, setMode] = useState<ViewMode>('pills')
  const [showInactive, setShowInactive] = useState(false)

  const active = concepts.filter(c => c.active)
  const displayed = showInactive ? concepts : active

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex items-center justify-between">
        <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>
          <span className="font-semibold" style={{ color: 'var(--accent)' }}>
            {active.length}
          </span>{' '}
          of {concepts.length} concepts activated
        </p>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setShowInactive(!showInactive)}
            className="text-xs px-2.5 py-1 rounded-lg transition-colors"
            style={{
              background: showInactive ? 'var(--accent-dim)' : 'var(--glass-bg)',
              color: showInactive ? 'var(--accent)' : 'var(--text-muted)',
              border: '1px solid var(--glass-border)',
            }}
          >
            {showInactive ? 'Hide inactive' : 'Show all'}
          </button>
          {/* View toggle */}
          <div
            className="flex rounded-lg overflow-hidden"
            style={{ border: '1px solid var(--glass-border)' }}
          >
            {(['pills', 'bars'] as ViewMode[]).map(m => (
              <button
                key={m}
                type="button"
                onClick={() => setMode(m)}
                className={cn(
                  'px-3 py-1 text-xs transition-colors capitalize',
                  mode === m
                    ? 'bg-[var(--accent-dim)] text-[var(--accent)]'
                    : 'text-[var(--text-muted)] hover:text-[var(--text-secondary)]'
                )}
              >
                {m}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Pills view */}
      {mode === 'pills' && (
        <div className="flex flex-wrap gap-2">
          {displayed.map(c => (
            <button
              key={c.concept}
              type="button"
              onClick={() => onSelectConcept?.(selectedConcept === c.concept ? null : c.concept)}
            >
              <ConceptBadge
                concept={c.concept}
                score={c.score}
                active={c.active}
                className={cn(
                  'transition-all cursor-pointer',
                  selectedConcept === c.concept && 'ring-1 ring-[var(--accent)]'
                )}
              />
            </button>
          ))}
        </div>
      )}

      {/* Bars view */}
      {mode === 'bars' && (
        <div className="space-y-2">
          {displayed.map(c => (
            <div
              key={c.concept}
              className={cn(
                'flex items-center gap-3 px-3 py-2 rounded-lg transition-colors cursor-pointer',
                selectedConcept === c.concept
                  ? 'bg-[var(--accent-dim)]'
                  : 'hover:bg-white/[0.03]'
              )}
              onClick={() => onSelectConcept?.(selectedConcept === c.concept ? null : c.concept)}
            >
              <span
                className="text-xs font-medium w-28 shrink-0 truncate"
                style={{ color: c.active ? 'var(--text-primary)' : 'var(--text-muted)' }}
              >
                {c.concept}
              </span>
              <div className="flex-1">
                <ConfidenceBar value={c.score} showLabel={false} />
              </div>
              <span
                className="text-xs font-mono w-10 text-right shrink-0"
                style={{
                  color: c.score >= 0.7 ? 'var(--confidence-high)'
                    : c.score >= 0.4 ? 'var(--confidence-medium)'
                    : 'var(--text-muted)',
                }}
              >
                {(c.score * 100).toFixed(0)}%
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
