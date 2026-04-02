"use client"

import { X, Stethoscope, Code2, BarChart3 } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { ConceptBadge } from "@/components/ui/concept-badge"

interface ContextSidebarProps {
  onClose?: () => void
  isOpen?: boolean
}

const contextData = {
  topDiagnosis: {
    code: "E11.9",
    description: "Type 2 diabetes mellitus without complications",
    confidence: 0.96,
  },
  topConcepts: [
    { concept: "elevated_fasting_glucose", score: 0.92 },
    { concept: "increased_thirst", score: 0.88 },
    { concept: "frequent_urination", score: 0.85 },
  ],
  analysisMetrics: {
    inferenceTime: "324ms",
    totalConcepts: 7,
    activeDiagnoses: 4,
  },
}

export function ContextSidebar({ onClose, isOpen = true }: ContextSidebarProps) {
  if (!isOpen) return null

  return (
    <div className="w-full sm:w-80 bg-white/[0.02] border-r border-white/[0.08] rounded-lg overflow-hidden flex flex-col">
      {/* Header */}
      <div className="px-4 py-4 border-b border-white/[0.08] flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Stethoscope className="w-5 h-5 text-primary" />
          <h3 className="font-semibold text-foreground">Analysis Context</h3>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="p-1 hover:bg-white/[0.08] rounded transition-colors"
          >
            <X className="w-4 h-4 text-foreground-muted" />
          </button>
        )}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto space-y-4 px-4 py-4">
        {/* Top Diagnosis */}
        <div>
          <p className="text-xs font-semibold text-foreground-muted uppercase mb-3">
            Top Diagnosis
          </p>
          <div className="p-3 rounded-lg bg-white/[0.04] border border-white/[0.08] space-y-2">
            <div className="flex items-baseline gap-2">
              <span className="text-sm font-mono text-primary">{contextData.topDiagnosis.code}</span>
              <span className="text-xs bg-primary/20 text-primary px-2 py-1 rounded">
                {Math.round(contextData.topDiagnosis.confidence * 100)}%
              </span>
            </div>
            <p className="text-xs text-foreground-muted leading-tight">
              {contextData.topDiagnosis.description}
            </p>
          </div>
        </div>

        {/* Top Concepts */}
        <div>
          <p className="text-xs font-semibold text-foreground-muted uppercase mb-3">
            Contributing Concepts
          </p>
          <div className="space-y-2">
            {contextData.topConcepts.map((item) => (
              <ConceptBadge
                key={item.concept}
                label={item.concept.replace(/_/g, " ")}
                score={item.score}
              />
            ))}
          </div>
        </div>

        {/* Analysis Metrics */}
        <div>
          <p className="text-xs font-semibold text-foreground-muted uppercase mb-3">
            Metrics
          </p>
          <div className="space-y-2">
            <div className="flex items-center justify-between p-2 rounded bg-white/[0.04]">
              <span className="text-xs text-foreground-muted">Inference Time</span>
              <span className="text-xs font-mono text-gold">{contextData.analysisMetrics.inferenceTime}</span>
            </div>
            <div className="flex items-center justify-between p-2 rounded bg-white/[0.04]">
              <span className="text-xs text-foreground-muted">Total Concepts</span>
              <span className="text-xs font-mono text-primary">{contextData.analysisMetrics.totalConcepts}</span>
            </div>
            <div className="flex items-center justify-between p-2 rounded bg-white/[0.04]">
              <span className="text-xs text-foreground-muted">Active Diagnoses</span>
              <span className="text-xs font-mono text-primary">{contextData.analysisMetrics.activeDiagnoses}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
