"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Zap, Clock, MessageSquare } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { NoteInput } from "@/components/workspace/note-input"
import { PredictionsList } from "@/components/workspace/predictions-list"
import { ConceptsTab } from "@/components/workspace/concepts-tab"
import { AttributionTab } from "@/components/workspace/attribution-tab"
import { FeedbackWidget } from "@/components/workspace/feedback-widget"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { useAuth } from "@/hooks/use-auth"
import { predict, submitReview, type PredictResponse } from "@/lib/api"
import { persistWorkspaceChatContext } from "@/lib/chat-context"

// ── Shape adapters ─────────────────────────────────────────────────────────

function toPredictionsList(data: PredictResponse) {
  return data.predictions.map((p) => ({
    rank: p.rank,
    code: p.code,
    description: p.description,
    confidence: p.confidence,
    isActive: p.above_threshold,
    concepts: data.activated_concepts
      .filter((c) => c.active)
      .slice(0, 3)
      .map((c) => ({ name: c.concept, score: c.score })),
  }))
}

function toConceptsList(data: PredictResponse) {
  return data.activated_concepts.map((c) => ({
    name: c.concept,
    score: c.score,
    active: c.active,
  }))
}

function toAttributions(data: PredictResponse) {
  const activeConcepts = data.activated_concepts.filter((c) => c.active).map((c) => c.concept)
  return data.predictions
    .filter((p) => p.above_threshold)
    .map((p) => ({
      diagnosisCode: p.code,
      diagnosisName: p.description,
      concepts: activeConcepts.slice(0, 3),
    }))
}

const DIAGNOSIS_LIST_LIMIT = 5

// ── Page ──────────────────────────────────────────────────────────────────

export default function WorkspacePage() {
  const router = useRouter()
  const { session } = useAuth()
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<PredictResponse | null>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [selectedTab, setSelectedTab] = useState("diagnoses")

  const handleAnalyze = async (note: string) => {
    setIsLoading(true)
    setErrorMsg(null)
    try {
      const token = session?.access_token
      if (!token) throw new Error("Not authenticated")
      const data = await predict(note, token)
      setResult(data)
    } catch (err: any) {
      setErrorMsg(err.message ?? "Prediction failed")
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmitReview = async (
    rating: number,
    accuracyRating: number,
    interpretabilityRating: number,
    comment: string
  ) => {
    if (!result?.prediction_id || !session?.access_token) return
    await submitReview(result.prediction_id, rating, session.access_token, {
      accuracyRating,
      interpretabilityRating,
      comment,
    })
  }

  const predictions = result
    ? toPredictionsList(result).slice(0, DIAGNOSIS_LIST_LIMIT)
    : []
  const concepts = result ? toConceptsList(result) : []
  const attributions = result ? toAttributions(result) : []
  const activeDiagnoses = result
    ? result.predictions.filter((p) => p.above_threshold).length
    : 0

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
        {errorMsg ? (
          <GlassCard className="flex flex-col items-center justify-center min-h-[600px]">
            <div className="text-center space-y-3">
              <div className="w-16 h-16 rounded-2xl bg-destructive/20 flex items-center justify-center mx-auto">
                <Zap className="w-8 h-8 text-destructive" />
              </div>
              <h3 className="text-foreground font-medium">Prediction Failed</h3>
              <p className="text-foreground-muted text-sm max-w-xs">{errorMsg}</p>
              <button
                onClick={() => setErrorMsg(null)}
                className="px-4 py-2 rounded-lg bg-white/[0.06] border border-white/[0.08] text-sm text-foreground hover:bg-white/[0.1] transition-colors"
              >
                Try Again
              </button>
            </div>
          </GlassCard>
        ) : !result && !isLoading ? (
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
            <p className="text-foreground-muted text-sm mt-1">Running BioClinicalBERT inference...</p>
          </GlassCard>
        ) : (
          <GlassCard className="space-y-6">
            {/* Results Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-white/[0.06]">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2 py-1 rounded text-xs font-semibold bg-primary/20 text-primary">
                    Live
                  </span>
                  <span className="text-xs text-foreground-muted flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {result?.metadata.inference_time_ms}ms inference
                  </span>
                </div>
                <h3 className="font-semibold text-foreground">
                  {activeDiagnoses} Active {activeDiagnoses === 1 ? "Diagnosis" : "Diagnoses"}
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
                <PredictionsList predictions={predictions} />
                {result && result.predictions.length > DIAGNOSIS_LIST_LIMIT && (
                  <p className="text-xs text-foreground-muted text-center">
                    Showing top {DIAGNOSIS_LIST_LIMIT} of {result.predictions.length} ranked codes.
                  </p>
                )}
                <button
                  type="button"
                  onClick={() => {
                    if (!result) return
                    persistWorkspaceChatContext(result)
                    router.push("/dashboard/chat")
                  }}
                  className="w-full px-4 py-3 rounded-lg bg-white/[0.06] border border-white/[0.08] text-foreground hover:bg-white/[0.1] transition-colors flex items-center justify-center gap-2 mt-4"
                >
                  <MessageSquare className="w-4 h-4" />
                  Discuss in Chat →
                </button>
              </TabsContent>

              <TabsContent value="concepts">
                <ConceptsTab concepts={concepts} />
              </TabsContent>

              <TabsContent value="attribution">
                <AttributionTab attributions={attributions} />
              </TabsContent>
            </Tabs>
          </GlassCard>
        )}
      </div>

      {/* Feedback Modal */}
      {showFeedback && (
        <FeedbackWidget
          onClose={() => setShowFeedback(false)}
          onSubmit={handleSubmitReview}
        />
      )}
    </div>
  )
}
