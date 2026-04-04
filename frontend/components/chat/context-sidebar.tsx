"use client"

import { X, Stethoscope, Code2, BarChart3 } from "lucide-react"
import { ConceptBadge } from "@/components/ui/concept-badge"
import type { ChatAnalysisContext } from "@/lib/chat-context"

interface ContextSidebarProps {
  context: ChatAnalysisContext
  onClose?: () => void
  onClear?: () => void
}

export function ContextSidebar({ context, onClose, onClear }: ContextSidebarProps) {
  return (
    <div className="w-full sm:w-80 bg-white/[0.02] border-r border-white/[0.08] rounded-lg overflow-hidden flex flex-col">
      <div className="px-4 py-4 border-b border-white/[0.08] flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Stethoscope className="w-5 h-5 text-primary" />
          <h3 className="font-semibold text-foreground">Analysis Context</h3>
        </div>
        {onClose && (
          <button
            type="button"
            onClick={onClose}
            className="p-1 hover:bg-white/[0.08] rounded transition-colors"
          >
            <X className="w-4 h-4 text-foreground-muted" />
          </button>
        )}
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 px-4 py-4">
        <div>
          <p className="text-xs font-semibold text-foreground-muted uppercase mb-3">Top Diagnosis</p>
          <div className="p-3 rounded-lg bg-white/[0.04] border border-white/[0.08] space-y-2">
            {context.topDiagnosis ? (
              <>
                <div className="flex items-baseline gap-2">
                  <span className="text-sm font-mono text-primary">{context.topDiagnosis.code}</span>
                  <span className="text-xs bg-primary/20 text-primary px-2 py-1 rounded">
                    {Math.round(context.topDiagnosis.confidence * 100)}%
                  </span>
                </div>
                <p className="text-xs text-foreground-muted leading-tight">
                  {context.topDiagnosis.description}
                </p>
              </>
            ) : (
              <p className="text-xs text-foreground-muted">No prediction above threshold.</p>
            )}
          </div>
        </div>

        <div>
          <p className="text-xs font-semibold text-foreground-muted uppercase mb-3 flex items-center gap-1.5">
            <Code2 className="w-3.5 h-3.5" />
            Contributing Concepts
          </p>
          <div className="space-y-2">
            {context.topConcepts.length > 0 ? (
              context.topConcepts.map((item) => (
                <ConceptBadge key={item.concept} name={item.concept} score={item.score} />
              ))
            ) : (
              <p className="text-xs text-foreground-muted">No active concepts.</p>
            )}
          </div>
        </div>

        <div>
          <p className="text-xs font-semibold text-foreground-muted uppercase mb-3 flex items-center gap-1.5">
            <BarChart3 className="w-3.5 h-3.5" />
            Metrics
          </p>
          <div className="space-y-2">
            <div className="flex items-center justify-between p-2 rounded bg-white/[0.04]">
              <span className="text-xs text-foreground-muted">Inference Time</span>
              <span className="text-xs font-mono text-gold">{context.inferenceTimeMs}ms</span>
            </div>
            <div className="flex items-center justify-between p-2 rounded bg-white/[0.04]">
              <span className="text-xs text-foreground-muted">Total Concepts</span>
              <span className="text-xs font-mono text-primary">{context.totalConcepts}</span>
            </div>
            <div className="flex items-center justify-between p-2 rounded bg-white/[0.04]">
              <span className="text-xs text-foreground-muted">Active Diagnoses</span>
              <span className="text-xs font-mono text-primary">{context.activeDiagnoses}</span>
            </div>
          </div>
        </div>
      </div>

      {onClear && (
        <div className="p-3 border-t border-white/[0.08]">
          <button
            type="button"
            onClick={onClear}
            className="w-full text-xs text-foreground-muted hover:text-foreground py-2 rounded-lg hover:bg-white/[0.06] transition-colors"
          >
            Dismiss context
          </button>
        </div>
      )}
    </div>
  )
}
