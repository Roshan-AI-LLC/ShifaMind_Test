"use client"

import { useState } from "react"
import { Zap, Clock, MessageSquare } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { NoteInput } from "@/components/workspace/note-input"
import { PredictionsList } from "@/components/workspace/predictions-list"
import { ConceptsTab } from "@/components/workspace/concepts-tab"
import { AttributionTab } from "@/components/workspace/attribution-tab"
import { FeedbackWidget } from "@/components/workspace/feedback-widget"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"

// Mock predictions data
const mockPredictions = [
  {
    rank: 1,
    code: "E11.9",
    description: "Type 2 diabetes mellitus without complications",
    confidence: 0.96,
    isActive: true,
    concepts: [
      { name: "elevated_fasting_glucose", score: 0.92 },
      { name: "increased_thirst", score: 0.88 },
      { name: "frequent_urination", score: 0.85 },
    ],
  },
  {
    rank: 2,
    code: "E78.5",
    description: "Lipidemia, unspecified",
    confidence: 0.72,
    isActive: true,
    concepts: [
      { name: "abnormal_lipid_profile", score: 0.78 },
      { name: "metabolic_syndrome", score: 0.65 },
    ],
  },
  {
    rank: 3,
    code: "I10",
    description: "Essential (primary) hypertension",
    confidence: 0.68,
    isActive: false,
    concepts: [
      { name: "elevated_blood_pressure", score: 0.72 },
    ],
  },
  {
    rank: 4,
    code: "R06.02",
    description: "Tachypnea",
    confidence: 0.54,
    isActive: false,
    concepts: [
      { name: "rapid_breathing", score: 0.58 },
    ],
  },
]

const mockConcepts = [
  { name: "elevated_fasting_glucose", score: 0.92, active: true },
  { name: "increased_thirst", score: 0.88, active: true },
  { name: "frequent_urination", score: 0.85, active: true },
  { name: "abnormal_lipid_profile", score: 0.78, active: true },
  { name: "elevated_blood_pressure", score: 0.72, active: false },
  { name: "metabolic_syndrome", score: 0.65, active: false },
  { name: "rapid_breathing", score: 0.58, active: false },
]

const mockAttributions = [
  {
    diagnosisCode: "E11.9",
    diagnosisName: "Type 2 diabetes mellitus",
    concepts: ["elevated_fasting_glucose", "increased_thirst", "frequent_urination"],
  },
  {
    diagnosisCode: "E78.5",
    diagnosisName: "Lipidemia, unspecified",
    concepts: ["abnormal_lipid_profile", "metabolic_syndrome"],
  },
  {
    diagnosisCode: "I10",
    diagnosisName: "Essential hypertension",
    concepts: ["elevated_blood_pressure"],
  },
]

export default function WorkspacePage() {
  const [hasAnalyzed, setHasAnalyzed] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [showFeedback, setShowFeedback] = useState(false)
  const [selectedTab, setSelectedTab] = useState("diagnoses")

  const handleAnalyze = (note: string) => {
    setIsLoading(true)
    setTimeout(() => {
      setHasAnalyzed(true)
      setIsLoading(false)
    }, 1500)
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-foreground">Workspace</h1>
        <p className="text-foreground-muted mt-1">Analyze clinical notes with AI-powered ICD-10 predictions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[420px_1fr] gap-6">
        {/* Note Input Panel */}
        <NoteInput onAnalyze={handleAnalyze} />

        {/* Results Panel */}
        {!hasAnalyzed && !isLoading ? (
          <GlassCard className="flex flex-col items-center justify-center min-h-[600px]">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/30 to-primary/10 blur-2xl rounded-full" />
              <div className="relative w-16 h-16 rounded-2xl bg-white/[0.06] flex items-center justify-center">
                <Zap className="w-8 h-8 text-primary" />
              </div>
            </div>
            <h3 className="text-foreground font-medium mt-6">Ready to Analyze</h3>
            <p className="text-foreground-muted text-sm mt-1">Enter a clinical note to get started</p>
          </GlassCard>
        ) : isLoading ? (
          <GlassCard className="flex flex-col items-center justify-center min-h-[600px]">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/30 to-primary/10 blur-2xl rounded-full animate-pulse" />
              <div className="relative w-16 h-16 rounded-2xl bg-white/[0.06] flex items-center justify-center">
                <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
              </div>
            </div>
            <h3 className="text-foreground font-medium mt-6">Analyzing Note</h3>
            <p className="text-foreground-muted text-sm mt-1">Training BioClinicalBERT on your input...</p>
          </GlassCard>
        ) : (
          <GlassCard className="space-y-6">
            {/* Results Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-white/[0.06]">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2 py-1 rounded text-xs font-semibold bg-primary/20 text-primary">
                    Demo
                  </span>
                  <span className="text-xs text-foreground-muted flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    324ms inference
                  </span>
                </div>
                <h3 className="font-semibold text-foreground">
                  {mockPredictions.filter(p => p.isActive).length} Active Diagnoses
                </h3>
              </div>
              <button
                onClick={() => setShowFeedback(true)}
                className="px-4 py-2 rounded-lg bg-gold/20 border border-gold/30 text-sm text-gold hover:bg-gold/30 transition-colors font-medium"
              >
                Rate Prediction
              </button>
            </div>

            {/* Tabs */}
            <Tabs value={selectedTab} onValueChange={setSelectedTab} className="space-y-4">
              <TabsList>
                <TabsTrigger value="diagnoses">Diagnoses</TabsTrigger>
                <TabsTrigger value="concepts">Concepts</TabsTrigger>
                <TabsTrigger value="attribution">Attribution</TabsTrigger>
              </TabsList>

              <TabsContent value="diagnoses" className="space-y-3">
                <PredictionsList predictions={mockPredictions} />
                <button className="w-full px-4 py-3 rounded-lg bg-white/[0.06] border border-white/[0.08] text-foreground hover:bg-white/[0.1] transition-colors flex items-center justify-center gap-2 mt-4">
                  <MessageSquare className="w-4 h-4" />
                  Discuss in Chat →
                </button>
              </TabsContent>

              <TabsContent value="concepts">
                <ConceptsTab concepts={mockConcepts} />
              </TabsContent>

              <TabsContent value="attribution">
                <AttributionTab attributions={mockAttributions} />
              </TabsContent>
            </Tabs>
          </GlassCard>
        )}
      </div>

      {/* Feedback Modal */}
      {showFeedback && <FeedbackWidget onClose={() => setShowFeedback(false)} />}
    </div>
  )
}
