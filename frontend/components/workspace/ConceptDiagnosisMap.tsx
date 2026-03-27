'use client'

import { useState } from 'react'
import type { PredictedCode, ActivatedConcept } from '@/types'
import { ConfidenceBar } from '@/components/shared/ConfidenceBar'
import { cn } from '@/lib/utils'

interface ConceptDiagnosisMapProps {
  predictions: PredictedCode[]
  concepts: ActivatedConcept[]
}

export function ConceptDiagnosisMap({ predictions, concepts }: ConceptDiagnosisMapProps) {
  const [selectedCode, setSelectedCode] = useState<string | null>(null)
  const [selectedConcept, setSelectedConcept] = useState<string | null>(null)

  const aboveThreshold = predictions.filter(p => p.above_threshold).slice(0, 10)
  const activeConcepts = concepts.filter(c => c.active).slice(0, 20)

  function handleSelectCode(code: string) {
    setSelectedCode(selectedCode === code ? null : code)
    setSelectedConcept(null)
  }

  function handleSelectConcept(concept: string) {
    setSelectedConcept(selectedConcept === concept ? null : concept)
    setSelectedCode(null)
  }

  return (
    <div className="grid grid-cols-2 gap-6">
      {/* Left: diagnoses */}
      <div>
        <p className="text-xs font-medium mb-3" style={{ color: 'var(--text-secondary)' }}>
          Predicted diagnoses
        </p>
        <div className="space-y-1.5">
          {aboveThreshold.map(pred => (
            <button
              key={pred.code}
              type="button"
              onClick={() => handleSelectCode(pred.code)}
              className={cn(
                'w-full text-left px-3 py-2.5 rounded-xl transition-all border',
                selectedCode === pred.code
                  ? 'bg-[var(--accent-dim)] border-[var(--accent)]/40'
                  : 'bg-white/[0.03] border-white/[0.05] hover:bg-white/[0.05]'
              )}
            >
              <span className="font-mono text-xs block mb-0.5" style={{ color: 'var(--accent)' }}>
                {pred.code}
              </span>
              <span className="text-xs block mb-1.5 leading-tight" style={{ color: 'var(--text-primary)' }}>
                {pred.description}
              </span>
              <ConfidenceBar value={pred.confidence} showLabel={false} />
            </button>
          ))}
        </div>
      </div>

      {/* Right: concepts */}
      <div>
        <p className="text-xs font-medium mb-3" style={{ color: 'var(--text-secondary)' }}>
          Activated concepts
        </p>
        <div className="space-y-1.5">
          {activeConcepts.map(c => (
            <button
              key={c.concept}
              type="button"
              onClick={() => handleSelectConcept(c.concept)}
              className={cn(
                'w-full text-left px-3 py-2.5 rounded-xl transition-all border',
                selectedConcept === c.concept
                  ? 'bg-[var(--accent-dim)] border-[var(--accent)]/40'
                  : 'bg-white/[0.03] border-white/[0.05] hover:bg-white/[0.05]'
              )}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-medium" style={{ color: 'var(--text-primary)' }}>
                  {c.concept}
                </span>
                <span className="font-mono text-xs" style={{
                  color: c.score >= 0.7 ? 'var(--confidence-high)'
                    : c.score >= 0.4 ? 'var(--confidence-medium)'
                    : 'var(--text-muted)',
                }}>
                  {(c.score * 100).toFixed(0)}%
                </span>
              </div>
              <ConfidenceBar value={c.score} showLabel={false} />
            </button>
          ))}
        </div>
      </div>

      {/* Selection hint */}
      {!selectedCode && !selectedConcept && (
        <div className="col-span-2 text-center py-4">
          <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
            Click a diagnosis or concept to highlight the relationship
          </p>
        </div>
      )}

      {(selectedCode || selectedConcept) && (
        <div className="col-span-2 px-4 py-3 rounded-xl" style={{ background: 'var(--accent-dim)', border: '1px solid rgba(78,205,196,0.2)' }}>
          <p className="text-xs" style={{ color: 'var(--accent)' }}>
            {selectedCode
              ? `Showing concepts contributing to ${selectedCode}`
              : `Showing diagnoses influenced by "${selectedConcept}"`}
          </p>
        </div>
      )}
    </div>
  )
}
