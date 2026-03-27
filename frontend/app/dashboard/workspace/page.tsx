'use client'

import { useState } from 'react'
import Link from 'next/link'
import { MessageSquare, Star, Zap } from 'lucide-react'
import { GlassCard } from '@/components/shared/GlassCard'
import { NoteInput } from '@/components/workspace/NoteInput'
import { PredictionPanel } from '@/components/workspace/PredictionPanel'
import { ConceptPanel } from '@/components/workspace/ConceptPanel'
import { ConceptDiagnosisMap } from '@/components/workspace/ConceptDiagnosisMap'
import { FeedbackWidget } from '@/components/workspace/FeedbackWidget'
import { usePrediction } from '@/hooks/usePrediction'
import { cn } from '@/lib/utils'
import type { PredictResponse } from '@/types'

type ResultTab = 'diagnoses' | 'concepts' | 'attribution'

function ResultSkeleton() {
  return (
    <div className="space-y-3 animate-pulse">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="skeleton h-16 rounded-xl" />
      ))}
    </div>
  )
}

export default function WorkspacePage() {
  const { runPrediction, loading, error, result, isDemo } = usePrediction()
  const [activeTab, setActiveTab] = useState<ResultTab>('diagnoses')
  const [showFeedback, setShowFeedback] = useState(false)
  const [selectedCode, setSelectedCode] = useState<string | null>(null)
  const [selectedConcept, setSelectedConcept] = useState<string | null>(null)

  async function handleSubmit(text: string) {
    setSelectedCode(null)
    setSelectedConcept(null)
    setActiveTab('diagnoses')
    await runPrediction(text)
  }

  const TABS: { id: ResultTab; label: string }[] = [
    { id: 'diagnoses', label: 'Diagnoses' },
    { id: 'concepts', label: 'Concepts' },
    { id: 'attribution', label: 'Attribution' },
  ]

  return (
    <div className="max-w-7xl mx-auto animate-fade-in">
      {/* Responsive split pane: stacked on mobile, side-by-side on lg+ */}
      <div
        className="flex flex-col lg:flex-row gap-6"
        style={{ minHeight: 'calc(100vh - 140px)' }}
      >
        {/* ── Left pane: Note input ── */}
        <div className="w-full lg:w-[420px] lg:shrink-0">
          <GlassCard className="p-6 h-full">
            <h2 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-secondary)' }}>
              Clinical Note
            </h2>
            <NoteInput onSubmit={handleSubmit} loading={loading} />
          </GlassCard>
        </div>

        {/* ── Right pane: Results ── */}
        <div className="flex-1 min-w-0">
          {!result && !loading && !error && (
            <GlassCard className="h-full flex flex-col items-center justify-center p-12 text-center">
              <div
                className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4 animate-pulse"
                style={{ background: 'var(--accent-dim)', boxShadow: '0 0 24px rgba(78,205,196,0.2)' }}
              >
                <Zap className="w-7 h-7" style={{ color: 'var(--accent)' }} />
              </div>
              <h3 className="font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
                Ready to analyze
              </h3>
              <p className="text-sm max-w-xs leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
                Choose a sample note or paste a clinical note on the left, then click
                &ldquo;Analyze with ShifaMind&rdquo; to see Phase 1 predictions.
              </p>
            </GlassCard>
          )}

          {loading && (
            <GlassCard className="p-6 h-full">
              <div className="mb-4">
                <div className="skeleton h-5 w-32 rounded mb-3" />
                <div className="flex gap-3 mb-4">
                  {[0, 1, 2].map(i => <div key={i} className="skeleton h-8 w-24 rounded-xl" />)}
                </div>
              </div>
              <ResultSkeleton />
            </GlassCard>
          )}

          {error && !loading && (
            <GlassCard className="p-6 flex flex-col items-center justify-center text-center h-full">
              <p className="text-sm mb-2 font-medium" style={{ color: 'var(--accent-warm)' }}>
                Prediction failed
              </p>
              <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>{error}</p>
            </GlassCard>
          )}

          {result && !loading && (
            <GlassCard className="p-6 flex flex-col h-full animate-fade-in">
              {/* Header */}
              <div className="flex items-center justify-between mb-4 shrink-0 flex-wrap gap-2">
                <div className="flex items-center gap-3">
                  <h2 className="text-sm font-semibold" style={{ color: 'var(--text-secondary)' }}>
                    Prediction Results
                  </h2>
                  <span
                    className="text-xs px-2 py-0.5 rounded-full font-mono"
                    style={{ background: 'var(--glass-bg)', color: 'var(--text-muted)' }}
                  >
                    {result.metadata.inference_time_ms}ms
                  </span>
                  <span className="text-xs hidden sm:inline" style={{ color: 'var(--text-muted)' }}>
                    {result.predictions.filter(p => p.above_threshold).length} active
                    {' · '}
                    {result.activated_concepts.filter(c => c.active).length} concepts
                  </span>
                  {isDemo && (
                    <span
                      className="text-xs px-2 py-0.5 rounded-full"
                      style={{ background: 'rgba(255,217,61,0.1)', color: 'var(--accent-gold)' }}
                    >
                      Demo
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  {result.prediction_id && !isDemo && (
                    <button
                      onClick={() => setShowFeedback(true)}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs transition-colors"
                      style={{
                        background: 'rgba(255,217,61,0.1)',
                        color: 'var(--accent-gold)',
                        border: '1px solid rgba(255,217,61,0.2)',
                      }}
                    >
                      <Star className="w-3.5 h-3.5" />
                      Rate
                    </button>
                  )}
                  {(result.prediction_id || isDemo) && (
                    <Link
                      href={isDemo ? '/dashboard/chat?demo=true' : `/dashboard/chat?prediction_id=${result.prediction_id}`}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs transition-all"
                      style={{
                        background: 'var(--accent-dim)',
                        color: 'var(--accent)',
                        border: '1px solid rgba(78,205,196,0.2)',
                      }}
                    >
                      <MessageSquare className="w-3.5 h-3.5" />
                      Discuss →
                    </Link>
                  )}
                </div>
              </div>

              {/* Tabs */}
              <div
                className="flex gap-1 p-1 rounded-xl mb-4 shrink-0 overflow-x-auto"
                style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--glass-border)' }}
              >
                {TABS.map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={cn(
                      'flex-1 py-2 px-3 rounded-xl text-xs font-medium transition-all duration-200 whitespace-nowrap',
                      activeTab === tab.id
                        ? 'bg-white/[0.1] text-white shadow-sm'
                        : 'text-white/40 hover:text-white/60 hover:bg-white/[0.04]'
                    )}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* Tab content */}
              <div className="flex-1 overflow-y-auto">
                {activeTab === 'diagnoses' && (
                  <PredictionPanel
                    predictions={result.predictions}
                    activatedConcepts={result.activated_concepts}
                    selectedCode={selectedCode}
                    onSelectCode={setSelectedCode}
                  />
                )}
                {activeTab === 'concepts' && (
                  <ConceptPanel
                    concepts={result.activated_concepts}
                    selectedConcept={selectedConcept}
                    onSelectConcept={setSelectedConcept}
                  />
                )}
                {activeTab === 'attribution' && (
                  <ConceptDiagnosisMap
                    predictions={result.predictions}
                    concepts={result.activated_concepts}
                  />
                )}
              </div>
            </GlassCard>
          )}
        </div>
      </div>

      {/* Feedback modal */}
      {showFeedback && result?.prediction_id && (
        <FeedbackWidget
          predictionId={result.prediction_id}
          onClose={() => setShowFeedback(false)}
        />
      )}
    </div>
  )
}
