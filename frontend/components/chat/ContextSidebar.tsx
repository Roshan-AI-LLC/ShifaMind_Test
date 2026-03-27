'use client'

import { useState } from 'react'
import Link from 'next/link'
import { ChevronRight, FlaskConical, X } from 'lucide-react'
import { ConfidenceBar } from '@/components/shared/ConfidenceBar'
import { ConceptBadge } from '@/components/shared/ConceptBadge'
import type { PredictResponse } from '@/types'
import { cn } from '@/lib/utils'

interface ContextSidebarProps {
  predictionId: string | null
  prediction: PredictResponse | null
  loadingPrediction?: boolean
}

export function ContextSidebar({ predictionId, prediction, loadingPrediction }: ContextSidebarProps) {
  const [collapsed, setCollapsed] = useState(false)

  const aboveThreshold = prediction?.predictions.filter(p => p.above_threshold).slice(0, 5) ?? []
  const topConcepts = prediction?.activated_concepts
    .filter(c => c.active)
    .slice(0, 8) ?? []

  return (
    <div
      className={cn(
        'shrink-0 transition-all duration-300 flex flex-col',
        'border-l border-white/[0.06]',
        collapsed ? 'w-10' : 'w-72'
      )}
    >
      {/* Toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="h-16 flex items-center justify-center hover:bg-white/[0.04] transition-colors shrink-0 border-b border-white/[0.06]"
      >
        <ChevronRight
          className={cn('w-4 h-4 transition-transform', !collapsed && 'rotate-180')}
          style={{ color: 'var(--text-muted)' }}
        />
      </button>

      {!collapsed && (
        <div className="flex-1 overflow-y-auto p-4 space-y-5">
          {/* Header */}
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-muted)' }}>
              Context
            </p>
            {predictionId && (
              <Link
                href={`/dashboard/workspace`}
                className="flex items-center gap-1 text-xs transition-colors"
                style={{ color: 'var(--text-muted)' }}
                onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent)')}
                onMouseLeave={e => (e.currentTarget.style.color = 'var(--text-muted)')}
              >
                <FlaskConical className="w-3 h-3" />
                Workspace
              </Link>
            )}
          </div>

          {!predictionId && (
            <div className="text-center py-6">
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                No prediction loaded.
              </p>
              <Link
                href="/dashboard/workspace"
                className="text-xs mt-2 block transition-colors"
                style={{ color: 'var(--accent)' }}
              >
                Go to Workspace →
              </Link>
            </div>
          )}

          {loadingPrediction && (
            <div className="space-y-2">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="skeleton h-10 rounded-xl" />
              ))}
            </div>
          )}

          {prediction && !loadingPrediction && (
            <>
              {/* Active diagnoses */}
              {aboveThreshold.length > 0 && (
                <div>
                  <p className="text-xs mb-2" style={{ color: 'var(--text-secondary)' }}>
                    Active diagnoses ({aboveThreshold.length})
                  </p>
                  <div className="space-y-1.5">
                    {aboveThreshold.map(p => (
                      <div
                        key={p.code}
                        className="px-3 py-2 rounded-xl"
                        style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)' }}
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-mono text-xs" style={{ color: 'var(--accent)' }}>
                            {p.code}
                          </span>
                        </div>
                        <p className="text-xs leading-tight mb-1.5" style={{ color: 'var(--text-primary)' }}>
                          {p.description}
                        </p>
                        <ConfidenceBar value={p.confidence} showLabel={false} />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Top concepts */}
              {topConcepts.length > 0 && (
                <div>
                  <p className="text-xs mb-2" style={{ color: 'var(--text-secondary)' }}>
                    Top concepts
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {topConcepts.map(c => (
                      <ConceptBadge key={c.concept} concept={c.concept} score={c.score} />
                    ))}
                  </div>
                </div>
              )}

              {/* Inference meta */}
              <div
                className="px-3 py-2 rounded-xl text-xs space-y-1"
                style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)' }}
              >
                <div className="flex justify-between">
                  <span style={{ color: 'var(--text-muted)' }}>Inference</span>
                  <span className="font-mono" style={{ color: 'var(--text-secondary)' }}>
                    {prediction.metadata.inference_time_ms}ms
                  </span>
                </div>
                <div className="flex justify-between">
                  <span style={{ color: 'var(--text-muted)' }}>Model</span>
                  <span className="font-mono" style={{ color: 'var(--text-secondary)' }}>
                    {prediction.metadata.model_version}
                  </span>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}
