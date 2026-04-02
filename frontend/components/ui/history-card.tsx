"use client"

import * as React from "react"
import { ChevronDown, CheckCircle2, AlertCircle } from "lucide-react"
import { GlassCard } from "./glass-card"
import { ConceptBadge } from "./concept-badge"
import { cn } from "@/lib/utils"

interface PredictionCode {
  code: string
  label: string
  confidence: number
}

interface HistoryCardProps {
  id: string
  date: string
  diagnosis: string
  content: string
  codes: PredictionCode[]
  userFeedback?: "helpful" | "incorrect" | "partial"
  onExpand?: (id: string) => void
  isExpanded?: boolean
}

export function HistoryCard({
  id,
  date,
  diagnosis,
  content,
  codes,
  userFeedback,
  onExpand,
  isExpanded = false,
}: HistoryCardProps) {
  return (
    <GlassCard className="overflow-hidden hover">
      <button
        onClick={() => onExpand?.(id)}
        className="w-full text-left"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-foreground font-medium truncate">
                {diagnosis}
              </h3>
              {userFeedback === "helpful" && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-green-500/20 text-green-400 border border-green-500/30">
                  <CheckCircle2 className="w-3 h-3" />
                  Helpful
                </span>
              )}
              {userFeedback === "incorrect" && (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-destructive/20 text-destructive border border-destructive/30">
                  <AlertCircle className="w-3 h-3" />
                  Incorrect
                </span>
              )}
            </div>
            <p className="text-sm text-foreground-muted mt-1">{date}</p>
          </div>
          <ChevronDown
            className={cn(
              "w-5 h-5 text-foreground-subtle flex-shrink-0 transition-transform duration-300",
              isExpanded && "rotate-180"
            )}
          />
        </div>
      </button>

      {isExpanded && (
        <div className="mt-6 pt-6 border-t border-white/[0.06] space-y-4 animate-fade-in">
          {/* Original content */}
          <div>
            <h4 className="text-sm font-medium text-foreground-muted mb-2">Clinical Note</h4>
            <div className="p-3 rounded-lg bg-white/[0.04] text-sm text-foreground leading-relaxed max-h-32 overflow-y-auto">
              {content}
            </div>
          </div>

          {/* Predicted codes */}
          <div>
            <h4 className="text-sm font-medium text-foreground-muted mb-3">ICD-10 Predictions</h4>
            <div className="space-y-2">
              {codes.map((code) => (
                <div key={code.code} className="flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2 min-w-0 flex-1">
                    <span className="text-sm font-mono font-semibold text-primary">
                      {code.code}
                    </span>
                    <span className="text-sm text-foreground-muted truncate">
                      {code.label}
                    </span>
                  </div>
                  <span className="text-sm font-semibold text-foreground flex-shrink-0">
                    {Math.round(code.confidence * 100)}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Feedback section */}
          {!userFeedback && (
            <div className="pt-4 border-t border-white/[0.06]">
              <p className="text-xs text-foreground-muted mb-3">Was this prediction helpful?</p>
              <div className="flex gap-2">
                <button className="px-3 py-1.5 text-xs rounded-lg bg-primary/20 text-primary border border-primary/30 hover:bg-primary/30 transition-colors">
                  Helpful
                </button>
                <button className="px-3 py-1.5 text-xs rounded-lg bg-white/[0.06] border border-white/[0.08] text-foreground hover:bg-white/[0.1] transition-colors">
                  Incorrect
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </GlassCard>
  )
}
