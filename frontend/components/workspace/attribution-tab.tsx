"use client"

import { useState } from "react"
import { AlertCircle } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"

interface Attribution {
  diagnosisCode: string
  diagnosisName: string
  concepts: string[]
}

interface AttributionTabProps {
  attributions: Attribution[]
}

export function AttributionTab({ attributions }: AttributionTabProps) {
  const [selectedDiagnosis, setSelectedDiagnosis] = useState<string | null>(null)
  const [selectedConcept, setSelectedConcept] = useState<string | null>(null)

  const getDiagnosisColor = (code: string, selected: boolean) => {
    if (!selected) return "bg-white/[0.04] border-white/[0.08]"
    return "bg-primary/10 border-primary/30"
  }

  const getConceptColor = (concept: string, selected: boolean) => {
    if (!selected) return "bg-white/[0.04] border-white/[0.08]"
    return "bg-primary/10 border-primary/30"
  }

  return (
    <div className="space-y-4">
      {/* Info banner */}
      <div className="flex gap-3 p-3 rounded-lg bg-white/[0.04] border border-white/[0.08]">
        <AlertCircle className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
        <p className="text-sm text-foreground-muted">
          Click on a diagnosis or concept to see how they relate
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Diagnoses column */}
        <div className="space-y-2">
          <h3 className="text-xs text-foreground-muted uppercase tracking-wider font-semibold">Diagnoses</h3>
          <div className="space-y-2">
            {attributions.map(attr => (
              <button
                key={attr.diagnosisCode}
                onClick={() => setSelectedDiagnosis(
                  selectedDiagnosis === attr.diagnosisCode ? null : attr.diagnosisCode
                )}
                className={`w-full text-left p-3 rounded-lg border transition-colors ${getDiagnosisColor(attr.diagnosisCode, selectedDiagnosis === attr.diagnosisCode)}`}
              >
                <div className="font-mono text-sm font-semibold text-foreground">
                  {attr.diagnosisCode}
                </div>
                <div className="text-xs text-foreground-muted mt-1">
                  {attr.diagnosisName}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Concepts column */}
        <div className="space-y-2">
          <h3 className="text-xs text-foreground-muted uppercase tracking-wider font-semibold">Concepts</h3>
          {selectedDiagnosis ? (
            <div className="space-y-2">
              {attributions
                .find(a => a.diagnosisCode === selectedDiagnosis)
                ?.concepts.map(concept => (
                  <button
                    key={concept}
                    onClick={() => setSelectedConcept(
                      selectedConcept === concept ? null : concept
                    )}
                    className={`w-full text-left p-3 rounded-lg border transition-colors ${getConceptColor(concept, selectedConcept === concept)}`}
                  >
                    <div className="text-sm text-foreground capitalize">
                      {concept.replace(/_/g, " ")}
                    </div>
                  </button>
                ))}
            </div>
          ) : (
            <GlassCard className="flex items-center justify-center py-8">
              <p className="text-sm text-foreground-muted text-center">
                Select a diagnosis to view related concepts
              </p>
            </GlassCard>
          )}
        </div>
      </div>
    </div>
  )
}
