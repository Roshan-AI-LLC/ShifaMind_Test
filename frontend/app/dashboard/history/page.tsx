"use client"

import { useState } from "react"
import { Filter, Download } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { HistoryCard } from "@/components/ui/history-card"

// Mock prediction history data
const predictions = [
  {
    id: "pred-001",
    date: "2024-01-15 10:32 AM",
    diagnosis: "Type 2 Diabetes Mellitus",
    content: "58-year-old male with persistent elevated fasting glucose levels (142 mg/dL), BMI 28, family history of diabetes. Patient reports increased thirst and frequent urination over past 3 weeks.",
    codes: [
      { code: "E11.9", label: "Type 2 diabetes mellitus without complications", confidence: 0.96 },
      { code: "R06.02", label: "Tachypnea", confidence: 0.72 },
      { code: "E78.5", label: "Lipidemia, unspecified", confidence: 0.68 },
    ],
    userFeedback: "helpful",
  },
  {
    id: "pred-002",
    date: "2024-01-14 2:15 PM",
    diagnosis: "Hypertensive Crisis",
    content: "45-year-old female presenting with severe headache, dizziness, and BP 180/120. No prior history of hypertension. Symptomatic and requires immediate intervention.",
    codes: [
      { code: "I10", label: "Essential (primary) hypertension", confidence: 0.88 },
      { code: "R51.9", label: "Headache, unspecified", confidence: 0.91 },
      { code: "R25.1", label: "Tremor, unspecified", confidence: 0.54 },
    ],
    userFeedback: "helpful",
  },
  {
    id: "pred-003",
    date: "2024-01-13 9:45 AM",
    diagnosis: "Acute Bronchitis with Productive Cough",
    content: "32-year-old male with 5-day history of productive cough with greenish sputum, fever, and chest discomfort. Recent upper respiratory infection. No shortness of breath.",
    codes: [
      { code: "J20.9", label: "Acute bronchitis, unspecified", confidence: 0.93 },
      { code: "R05.9", label: "Fever, unspecified", confidence: 0.79 },
      { code: "R06.02", label: "Tachypnea", confidence: 0.65 },
    ],
  },
  {
    id: "pred-004",
    date: "2024-01-12 11:20 AM",
    diagnosis: "Gastroesophageal Reflux Disease",
    content: "52-year-old female with chronic heartburn, regurgitation after meals, and mild dysphagia. Symptoms worse at night. Tried over-the-counter antacids with minimal relief.",
    codes: [
      { code: "K21.9", label: "Unspecified esophagitis", confidence: 0.85 },
      { code: "R12", label: "Heartburn", confidence: 0.94 },
      { code: "K22.70", label: "Barrett's esophagus without dysplasia", confidence: 0.41 },
    ],
    userFeedback: "partial",
  },
  {
    id: "pred-005",
    date: "2024-01-11 3:00 PM",
    diagnosis: "Acute Sinusitis",
    content: "28-year-old male with nasal congestion, facial pain, and purulent nasal discharge. Recent viral URI. No fever or systemic symptoms.",
    codes: [
      { code: "J01.90", label: "Unspecified acute sinusitis", confidence: 0.87 },
      { code: "R06.02", label: "Nasal congestion", confidence: 0.81 },
      { code: "M79.7", label: "Fibromyalgia", confidence: 0.38 },
    ],
    userFeedback: "incorrect",
  },
]

export default function HistoryPage() {
  const [expandedId, setExpandedId] = useState<string | null>(null)
  const [filterFeedback, setFilterFeedback] = useState<"all" | "helpful" | "partial" | "incorrect">("all")

  const filteredPredictions = filterFeedback === "all" 
    ? predictions 
    : predictions.filter(p => p.userFeedback === filterFeedback || (filterFeedback === "helpful" && !p.userFeedback))

  const handleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Prediction History</h1>
          <p className="text-foreground-muted mt-1">Review your past analyses and predictions</p>
        </div>
        <span className="px-3 py-1 rounded-full text-sm font-medium bg-white/[0.06] text-foreground-muted w-fit">
          {predictions.length} predictions
        </span>
      </div>

      {/* Filter and actions */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-foreground-muted" />
          <div className="flex gap-2">
            {["all", "helpful", "partial", "incorrect"].map((filter) => (
              <button
                key={filter}
                onClick={() => setFilterFeedback(filter as any)}
                className={`px-3 py-1.5 text-xs rounded-lg font-medium transition-colors ${
                  filterFeedback === filter
                    ? "bg-primary/20 text-primary border border-primary/30"
                    : "bg-white/[0.06] text-foreground hover:bg-white/[0.1] border border-white/[0.08]"
                }`}
              >
                {filter.charAt(0).toUpperCase() + filter.slice(1)}
              </button>
            ))}
          </div>
        </div>
        <button className="ml-auto hidden sm:flex items-center gap-2 px-3 py-1.5 text-sm rounded-lg bg-white/[0.06] border border-white/[0.08] text-foreground hover:bg-white/[0.1] transition-colors">
          <Download className="w-4 h-4" />
          Export
        </button>
      </div>

      {/* History cards */}
      <div className="space-y-3">
        {filteredPredictions.map((prediction, index) => (
          <div key={prediction.id} className={`animate-fade-in stagger-${index + 1}`}>
            <HistoryCard
              {...prediction}
              onExpand={handleExpand}
              isExpanded={expandedId === prediction.id}
            />
          </div>
        ))}
      </div>

      {filteredPredictions.length === 0 && (
        <GlassCard className="flex flex-col items-center justify-center py-16">
          <div className="w-16 h-16 rounded-2xl bg-white/[0.06] flex items-center justify-center">
            <Filter className="w-8 h-8 text-foreground-subtle" />
          </div>
          <h2 className="text-lg font-medium text-foreground mt-6">No predictions found</h2>
          <p className="text-foreground-muted text-sm mt-1 text-center max-w-sm">
            Try adjusting your filters to see more results.
          </p>
        </GlassCard>
      )}
    </div>
  )
}
