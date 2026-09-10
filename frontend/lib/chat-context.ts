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
  const above = data.codes.filter((c) => c.above_threshold)
  const top = above[0] ?? data.codes[0] ?? null

  // The concepts that carried the TOP code, ranked by how much they carried it.
  // A global concept list would not tell the chat model which evidence produced
  // the prediction it is being asked about.
  const topConcepts = top
    ? [...top.concepts]
        .sort((a, b) => Math.abs(b.contribution) - Math.abs(a.contribution))
        .slice(0, 5)
        .map((cc) => ({ concept: cc.name, score: cc.contribution }))
    : []

  const distinct = new Set<string>()
  for (const c of data.codes) for (const cc of c.concepts) distinct.add(cc.concept)

  return {
    predictionId: data.prediction_id ?? null,
    topDiagnosis: top
      ? { code: top.code, description: top.title || top.code, confidence: top.probability }
      : null,
    topConcepts,
    inferenceTimeMs: data.latency_ms,
    totalConcepts: distinct.size,
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
