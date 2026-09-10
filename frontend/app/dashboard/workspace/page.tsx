"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Zap, Clock, MessageSquare, FileText, Sparkles } from "lucide-react"
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
//
// The model returns concepts PER CODE, each with the exact signed contribution
// it made to that code's logit. The previous version attached the same global
// top-3 concepts to every prediction, which looked like attribution and was not.
// These adapters carry the real per-code evidence through.

function toPredictionsList(data: PredictResponse) {
  return data.codes.map((c, i) => ({
    rank: i + 1,
    code: c.code,
    description: c.title || c.code,
    confidence: c.probability,
    isActive: c.above_threshold,
    concepts: c.concepts.map((cc) => ({
      name: cc.name,
      // Kept for the badge's legacy percent mode; `contribution` wins when set.
      score: cc.gate,
      contribution: cc.contribution,
      span: cc.spans[0]?.surface ?? null,
      assertion: cc.spans[0]?.assertion ?? null,
    })),
  }))
}

/**
 * One row per distinct concept, ranked by the LARGEST absolute contribution it
 * made to any predicted code.
 *
 * Not by gate. The gate is saturated: essentially every routed concept sits at
 * 1.00, so a gate-ranked list is a list sorted by a constant, which is why this
 * tab used to render fifty chips all reading "100%". The contribution is the
 * quantity that actually varies, from about +10 down to -0.004, and it carries
 * the information a coder wants: which concept moved a prediction, and which
 * prediction it moved.
 */
function toConceptsList(data: PredictResponse) {
  const best = new Map<
    string,
    {
      name: string
      contribution: number
      code: string
      codeTitle: string
      gate: number
      span: string | null
      assertion: string | null
    }
  >()
  for (const code of data.codes) {
    for (const cc of code.concepts) {
      const prev = best.get(cc.concept)
      if (!prev || Math.abs(cc.contribution) > Math.abs(prev.contribution)) {
        best.set(cc.concept, {
          name: cc.name,
          contribution: cc.contribution,
          code: code.code,
          codeTitle: code.title || code.code,
          gate: cc.gate,
          span: cc.spans[0]?.surface ?? null,
          assertion: cc.spans[0]?.assertion ?? null,
        })
      }
    }
  }
  return [...best.values()].sort(
    (a, b) => Math.abs(b.contribution) - Math.abs(a.contribution)
  )
}

function toAttributions(data: PredictResponse) {
  return data.codes
    .filter((c) => c.above_threshold)
    .map((c) => ({
      diagnosisCode: c.code,
      diagnosisName: c.title || c.code,
      // Only supporting evidence in this view; objections have their own sign
      // in the diagnoses tab and would read as support in a bare name list.
      concepts: c.concepts
        .filter((cc) => cc.contribution > 0)
        .map((cc) => cc.name),
    }))
}

const DIAGNOSIS_LIST_LIMIT = 5
// Measured: p50 939 ms, p95 1,242 ms on CPU for a ~2,900-token note. The old
// value of 60 was for the 50-code model on very different hardware, and a
// progress bar that promises a minute for a one-second job reads as broken.
const EXPECTED_INFERENCE_SEC = 3

// ── Page ──────────────────────────────────────────────────────────────────

export default function WorkspacePage() {
  const router = useRouter()
  const { session } = useAuth()
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<PredictResponse | null>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [selectedTab, setSelectedTab] = useState("diagnoses")
  const [elapsedSec, setElapsedSec] = useState(0)

  useEffect(() => {
    if (!isLoading) {
      setElapsedSec(0)
      return
    }
    const start = Date.now()
    setElapsedSec(0)
    const id = setInterval(() => {
      setElapsedSec(Math.floor((Date.now() - start) / 1000))
    }, 1000)
    return () => clearInterval(id)
  }, [isLoading])

  const progressPct = Math.min(95, Math.round((elapsedSec / EXPECTED_INFERENCE_SEC) * 100))

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
  const suppressed = result?.suppressed ?? []
  const attributions = result ? toAttributions(result) : []
  const activeDiagnoses = result
    ? result.codes.filter((c) => c.above_threshold).length
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
          <GlassCard key="error" className="flex flex-col items-center justify-center min-h-[600px] animate-fade-in">
            <div className="text-center space-y-3">
              <div className="w-16 h-16 rounded-2xl bg-destructive/20 flex items-center justify-center mx-auto">
                <Zap className="w-8 h-8 text-destructive" />
              </div>
              <h3 className="text-foreground font-medium">Prediction Failed</h3>
              <p className="text-foreground-muted text-sm max-w-xs">{errorMsg}</p>
              <button
                onClick={() => setErrorMsg(null)}
                className="px-4 py-2 rounded-lg bg-secondary border border-border text-sm text-foreground hover:bg-secondary transition-colors"
              >
                Try Again
              </button>
            </div>
          </GlassCard>
        ) : !result && !isLoading ? (
          <GlassCard key="empty" className="flex flex-col items-center justify-center min-h-[600px] animate-fade-in">
            <div className="text-center space-y-5 max-w-sm px-6">
              <div className="relative mx-auto w-fit">
                <div className="absolute inset-0 bg-gradient-to-r from-primary/30 to-primary/10 blur-2xl rounded-full" />
                <div className="relative w-16 h-16 rounded-2xl bg-secondary flex items-center justify-center">
                  <Zap className="w-8 h-8 text-primary" />
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="text-foreground font-medium text-lg">Ready to Analyze</h3>
                <p className="text-foreground-muted text-sm leading-relaxed">
                  Paste a discharge summary or progress note on the left and click Analyze to surface ICD-10 predictions, activated concepts, and attribution.
                </p>
              </div>
              <div className="flex items-center justify-center gap-4 pt-2 text-xs text-foreground-muted">
                <span className="inline-flex items-center gap-1.5">
                  <FileText className="w-3.5 h-3.5" />
                  Clinical note
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  ShifaMind
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5" />
                  ~{EXPECTED_INFERENCE_SEC}s
                </span>
              </div>
            </div>
          </GlassCard>
        ) : isLoading ? (
          <GlassCard key="loading" className="flex flex-col items-center justify-center min-h-[600px] animate-fade-in">
            <div className="w-full max-w-sm space-y-6 text-center px-6">
              <div className="relative mx-auto w-fit">
                <div className="absolute inset-0 bg-gradient-to-r from-primary/30 to-primary/10 blur-2xl rounded-full animate-pulse" />
                <div className="relative w-16 h-16 rounded-2xl bg-secondary flex items-center justify-center">
                  <Zap className="w-8 h-8 text-primary" />
                </div>
              </div>
              <div className="space-y-1">
                <h3 className="text-foreground font-medium">Analyzing Note</h3>
                <p className="text-foreground-muted text-sm">Running ShifaMind inference…</p>
              </div>
              <div className="space-y-1">
                <div className="flex items-baseline justify-center gap-2">
                  <span className="text-3xl font-semibold tabular-nums text-foreground">{elapsedSec}</span>
                  <span className="text-sm text-foreground-muted">seconds elapsed</span>
                </div>
                <p className="text-xs text-foreground-muted">Typically takes ~{EXPECTED_INFERENCE_SEC}s</p>
              </div>
              <div
                className="relative h-1.5 w-full overflow-hidden rounded-full bg-secondary"
                role="progressbar"
                aria-valuemin={0}
                aria-valuemax={100}
                aria-valuenow={progressPct}
                aria-label="Inference progress"
              >
                <div
                  className="absolute inset-y-0 left-0 rounded-full bg-primary/60 transition-[width] duration-1000 ease-linear"
                  style={{ width: `${progressPct}%` }}
                />
                <div className="absolute inset-0 animate-shimmer rounded-full" />
              </div>
            </div>
          </GlassCard>
        ) : (
          <GlassCard key="result" className="space-y-6 animate-fade-in">
            {/* Results Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-border">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2 py-1 rounded text-xs font-semibold bg-primary/20 text-primary">
                    Live
                  </span>
                  <span className="text-xs text-foreground-muted flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {result?.latency_ms}ms inference
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
                {result?.no_code_met_threshold && (
                  <p className="text-xs text-gold text-center">
                    No code passed the {result.threshold.toFixed(2)} threshold.
                    Showing the highest-ranked codes anyway.
                  </p>
                )}
                {result && result.codes.length > DIAGNOSIS_LIST_LIMIT && (
                  <p className="text-xs text-foreground-muted text-center">
                    Showing top {DIAGNOSIS_LIST_LIMIT} of {result.codes.length} ranked codes.
                  </p>
                )}
                <button
                  type="button"
                  onClick={() => {
                    if (!result) return
                    persistWorkspaceChatContext(result)
                    router.push("/dashboard/chat")
                  }}
                  className="w-full px-4 py-3 rounded-lg bg-secondary border border-border text-foreground hover:bg-secondary transition-colors flex items-center justify-center gap-2 mt-4"
                >
                  <MessageSquare className="w-4 h-4" />
                  Discuss in Chat →
                </button>
              </TabsContent>

              <TabsContent value="concepts">
                <ConceptsTab concepts={concepts} suppressed={suppressed} />
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
