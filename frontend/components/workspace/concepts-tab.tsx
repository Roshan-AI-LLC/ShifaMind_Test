"use client"

import { useState } from "react"
import { ToggleLeft, ToggleRight } from "lucide-react"
import { ConceptBadge } from "@/components/ui/concept-badge"
import { ConfidenceBar } from "@/components/ui/confidence-bar"

interface Concept {
  name: string
  score: number
  active: boolean
}

interface ConceptsTabProps {
  concepts: Concept[]
}

export function ConceptsTab({ concepts }: ConceptsTabProps) {
  const [viewMode, setViewMode] = useState<"pills" | "bars">("pills")
  const [showInactive, setShowInactive] = useState(false)

  const filteredConcepts = showInactive ? concepts : concepts.filter(c => c.active)

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center gap-3 pb-4 border-b border-white/[0.06]">
        <div className="flex items-center gap-2">
          <span className="text-sm text-foreground-muted">View Mode:</span>
          <div className="flex gap-1 bg-white/[0.06] p-1 rounded-lg">
            <button
              onClick={() => setViewMode("pills")}
              className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                viewMode === "pills"
                  ? "bg-primary/20 text-primary"
                  : "text-foreground-muted hover:text-foreground"
              }`}
            >
              Pills
            </button>
            <button
              onClick={() => setViewMode("bars")}
              className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                viewMode === "bars"
                  ? "bg-primary/20 text-primary"
                  : "text-foreground-muted hover:text-foreground"
              }`}
            >
              Bars
            </button>
          </div>
        </div>

        <button
          onClick={() => setShowInactive(!showInactive)}
          className="ml-auto flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/[0.06] border border-white/[0.08] text-sm text-foreground hover:bg-white/[0.1] transition-colors"
        >
          {showInactive ? (
            <ToggleRight className="w-4 h-4" />
          ) : (
            <ToggleLeft className="w-4 h-4" />
          )}
          {showInactive ? "Show All" : "Active Only"}
        </button>
      </div>

      {/* Content */}
      {viewMode === "pills" ? (
        <div className="space-y-3">
          {filteredConcepts.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {filteredConcepts.map(concept => (
                <div key={concept.name} className={concept.active ? "" : "opacity-50"}>
                  <ConceptBadge
                    concept={concept.name}
                    score={concept.score}
                  />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-foreground-muted">No concepts found</p>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-3">
          {filteredConcepts.length > 0 ? (
            filteredConcepts.map(concept => (
              <div
                key={concept.name}
                className={`p-3 rounded-lg bg-white/[0.04] border border-white/[0.06] ${
                  !concept.active ? "opacity-50" : ""
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-foreground capitalize">
                    {concept.name.replace(/_/g, " ")}
                  </span>
                  <span className="text-sm font-mono text-primary">
                    {Math.round(concept.score * 100)}%
                  </span>
                </div>
                <ConfidenceBar value={concept.score} />
              </div>
            ))
          ) : (
            <div className="text-center py-8">
              <p className="text-foreground-muted">No concepts found</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
