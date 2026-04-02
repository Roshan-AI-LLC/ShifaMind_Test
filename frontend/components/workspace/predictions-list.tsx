"use client"

import { useState } from "react"
import { ChevronDown } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { ConfidenceBar } from "@/components/ui/confidence-bar"
import { ConceptBadge } from "@/components/ui/concept-badge"

interface Prediction {
  rank: number
  code: string
  description: string
  confidence: number
  isActive: boolean
  concepts: Array<{ name: string; score: number }>
}

interface PredictionsListProps {
  predictions: Prediction[]
}

export function PredictionsList({ predictions }: PredictionsListProps) {
  const [expandedRank, setExpandedRank] = useState<number | null>(0)

  const topPrediction = predictions[0]

  return (
    <div className="space-y-3">
      {predictions.map((pred, idx) => (
        <div key={pred.code} className={`animate-fade-in stagger-${idx + 1}`}>
          {pred.rank === 1 ? (
            // Top prediction with special styling
            <GlassCard
              className="cursor-pointer group relative overflow-hidden"
              onClick={() => setExpandedRank(expandedRank === pred.rank ? null : pred.rank)}
            >
              {/* Gradient background */}
              <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
              
              <div className="relative space-y-4">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-baseline gap-2 mb-2">
                      <span className="text-xs font-semibold text-primary uppercase tracking-wider">Rank #{pred.rank}</span>
                      {pred.isActive && (
                        <span className="px-2 py-0.5 rounded text-xs font-medium bg-primary/20 text-primary">
                          Active
                        </span>
                      )}
                    </div>
                    <h3 className="text-lg font-semibold text-foreground">
                      {pred.code}
                    </h3>
                    <p className="text-sm text-foreground-muted mt-1">
                      {pred.description}
                    </p>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <div className="text-4xl font-bold bg-gradient-to-r from-primary to-primary/50 bg-clip-text text-transparent">
                      {Math.round(pred.confidence * 100)}%
                    </div>
                    <p className="text-xs text-foreground-muted mt-1">Confidence</p>
                  </div>
                </div>

                {/* Expanded concepts */}
                {expandedRank === pred.rank && pred.concepts.length > 0 && (
                  <div className="pt-4 border-t border-white/[0.06] space-y-2">
                    <p className="text-xs text-foreground-muted uppercase tracking-wider">Contributing Concepts</p>
                    <div className="flex flex-wrap gap-2">
                      {pred.concepts.map(concept => (
                        <ConceptBadge
                          key={concept.name}
                          concept={concept.name}
                          score={concept.score}
                        />
                      ))}
                    </div>
                  </div>
                )}

                <ChevronDown
                  className={`w-5 h-5 text-foreground-muted transition-transform ${
                    expandedRank === pred.rank ? "rotate-180" : ""
                  } absolute right-4 top-4`}
                />
              </div>
            </GlassCard>
          ) : (
            // Other predictions
            <GlassCard
              className="cursor-pointer group"
              onClick={() => setExpandedRank(expandedRank === pred.rank ? null : pred.rank)}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-baseline gap-2 mb-2">
                    <span className="text-xs font-semibold text-foreground-muted uppercase tracking-wider">
                      Rank #{pred.rank}
                    </span>
                    {pred.isActive && (
                      <span className="px-2 py-0.5 rounded text-xs font-medium bg-primary/20 text-primary">
                        Active
                      </span>
                    )}
                  </div>
                  <h3 className="font-semibold text-foreground">
                    {pred.code}
                  </h3>
                  <p className="text-sm text-foreground-muted mt-1">
                    {pred.description}
                  </p>
                  
                  <div className="mt-3">
                    <ConfidenceBar
                      value={pred.confidence}
                      label={`${Math.round(pred.confidence * 100)}%`}
                    />
                  </div>
                </div>
                <ChevronDown
                  className={`w-5 h-5 text-foreground-muted transition-transform flex-shrink-0 mt-1 ${
                    expandedRank === pred.rank ? "rotate-180" : ""
                  }`}
                />
              </div>

              {/* Expanded concepts */}
              {expandedRank === pred.rank && pred.concepts.length > 0 && (
                <div className="mt-4 pt-4 border-t border-white/[0.06] space-y-2">
                  <p className="text-xs text-foreground-muted uppercase tracking-wider">Contributing Concepts</p>
                  <div className="flex flex-wrap gap-2">
                    {pred.concepts.map(concept => (
                      <ConceptBadge
                        key={concept.name}
                        concept={concept.name}
                        score={concept.score}
                      />
                    ))}
                  </div>
                </div>
              )}
            </GlassCard>
          )}
        </div>
      ))}
    </div>
  )
}
