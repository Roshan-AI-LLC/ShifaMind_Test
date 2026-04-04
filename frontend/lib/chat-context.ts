import type { PredictResponse } from "@/lib/api"

const STORAGE_KEY = "shifamind:workspaceChatContext"
const SCHEMA_VERSION = 1 as const

export type ChatAnalysisContext = {
  v: typeof SCHEMA_VERSION
  savedAt: string
  predictionId?: string | null
  topDiagnosis: { code: string; description: string; confidence: number } | null
  topConcepts: { concept: string; score: number }[]
  inferenceTimeMs: number
  totalConcepts: number
  activeDiagnoses: number
}

export function buildChatContextFromPrediction(data: PredictResponse): Omit<ChatAnalysisContext, "v" | "savedAt"> {
  const above = data.predictions.filter((p) => p.above_threshold)
  const ranked = [...data.predictions].sort((a, b) => b.confidence - a.confidence)
  const top = above[0] ?? ranked[0] ?? null
  const topConcepts = [...data.activated_concepts]
    .filter((c) => c.active)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map((c) => ({ concept: c.concept, score: c.score }))

  return {
    predictionId: data.prediction_id ?? null,
    topDiagnosis: top
      ? { code: top.code, description: top.description, confidence: top.confidence }
      : null,
    topConcepts,
    inferenceTimeMs: data.metadata.inference_time_ms,
    totalConcepts: data.activated_concepts.length,
    activeDiagnoses: above.length,
  }
}

export function persistWorkspaceChatContext(data: PredictResponse): void {
  const payload: ChatAnalysisContext = {
    v: SCHEMA_VERSION,
    savedAt: new Date().toISOString(),
    ...buildChatContextFromPrediction(data),
  }
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
  } catch {
    // private mode / quota
  }
}

export function readWorkspaceChatContext(): ChatAnalysisContext | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    const p = JSON.parse(raw) as ChatAnalysisContext
    if (p.v !== SCHEMA_VERSION) return null
    return p
  } catch {
    return null
  }
}

export function clearWorkspaceChatContext(): void {
  try {
    sessionStorage.removeItem(STORAGE_KEY)
  } catch {
    /* ignore */
  }
}
