const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// ── Types ────────────────────────────────────────────────────────────────────

/** One matched mention of a concept in the note, with its character span. */
export interface ConceptSpan {
  start: number
  end: number
  surface: string
  /** affirmed | negated | hypothetical | family | historical */
  assertion: string
}

/** A concept's contribution to ONE code's logit. */
export interface CodeConcept {
  concept: string
  name: string
  /**
   * SIGNED contribution to this code's logit. Unbounded, typically -1 to +11.
   * Not a probability and not a percentage: it is the exact per-concept term
   * in `logit = bias + sum(contributions)`. Negative means this concept argues
   * AGAINST the code.
   */
  contribution: number
  /** Gate value in (0,1): how strongly the concept is asserted in this note. */
  gate: number
  spans: ConceptSpan[]
}

export interface PredictedCode {
  code: string
  title: string
  /** "diag" (ICD-10-CM) or "proc" (ICD-10-PCS) */
  kind: string
  probability: number
  above_threshold: boolean
  concepts: CodeConcept[]
  bias?: number
  recon_error?: number
}

/** A concept the note MENTIONS that the model then shut off: the gate closed,
 *  so it contributed nothing to any code. Usually a negated, hypothetical,
 *  family-history or historical mention. */
export interface SuppressedConcept {
  concept: string
  name: string
  gate: number
  spans: ConceptSpan[]
  assertion: string | null
}

export interface PredictResponse {
  codes: PredictedCode[]
  threshold: number
  /** True when nothing cleared the threshold and the top 10 are shown instead. */
  no_code_met_threshold: boolean
  routing: {
    concepts_matched: number
    concepts_routed: number
    concepts_suppressed: number
    truncated: boolean
    top_k: number
  }
  suppressed: SuppressedConcept[]
  tokens: number
  truncated_note: boolean
  /** 1.0 under strict composition, i.e. every logit came through concepts. */
  concept_share: number | null
  model: { tag: string; seed: number; compose: string }
  latency_ms: number
  prediction_id?: string
}

export interface ModelHealth {
  variant: string
  tag: string
  seed: number
  loaded: boolean
  codes: number
  concepts: number
  threshold: number
  device: string
  compose: string
  max_concurrency: number
}

export type SseEvent =
  | { type: 'token'; content: string }
  | { type: 'done'; session_id: string }
  | { type: 'error'; content: string }

export interface SampleNote {
  id: string
  title: string
  category: string
  text: string
  note_length: number
  expected_codes?: string[] | null
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function authHeaders(token: string): HeadersInit {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  }
}

// ── Endpoints ────────────────────────────────────────────────────────────────

/** What is actually serving. Unauthenticated, so the dashboard can show it
 *  before any prediction has been made. */
export async function getModelHealth(): Promise<ModelHealth | null> {
  try {
    const res = await fetch(`${API_URL}/api/health/model`)
    if (!res.ok) return null
    return res.json()
  } catch {
    return null
  }
}

export async function listSampleNotes(token: string): Promise<SampleNote[]> {
  const res = await fetch(`${API_URL}/api/notes`, {
    headers: authHeaders(token),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error((err as any).detail || `Failed to load sample notes (${res.status})`)
  }
  return res.json()
}

export async function predict(
  text: string,
  token: string,
  opts: { threshold?: number; topConcepts?: number } = {}
): Promise<PredictResponse> {
  const res = await fetch(`${API_URL}/api/predict`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify({
      text,
      threshold: opts.threshold ?? null,
      top_concepts: opts.topConcepts ?? 8,
    }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error((err as any).detail || `Prediction failed (${res.status})`)
  }
  return res.json()
}

export async function* streamChat(
  message: string,
  token: string,
  opts: { predictionId?: string; sessionId?: string } = {}
): AsyncGenerator<SseEvent> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify({
      message,
      prediction_id: opts.predictionId ?? null,
      session_id: opts.sessionId ?? null,
      stream: true,
    }),
  })

  if (!res.ok || !res.body) {
    const err = await res.json().catch(() => ({}))
    throw new Error((err as any).detail || `Chat failed (${res.status})`)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() ?? ''
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          yield JSON.parse(line.slice(6)) as SseEvent
        } catch {
          // malformed line — skip
        }
      }
    }
  }
}

export async function submitReview(
  predictionId: string,
  rating: number,
  token: string,
  opts: { accuracyRating?: number; interpretabilityRating?: number; comment?: string } = {}
): Promise<void> {
  const res = await fetch(`${API_URL}/api/reviews`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify({
      prediction_id: predictionId,
      rating,
      accuracy_rating: opts.accuracyRating ?? null,
      interpretability_rating: opts.interpretabilityRating ?? null,
      comment: opts.comment ?? null,
    }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error((err as any).detail || `Review failed (${res.status})`)
  }
}

export async function checkHealth(): Promise<{ status: string; model_loaded: boolean }> {
  const res = await fetch(`${API_URL}/api/health`)
  if (!res.ok) throw new Error('API unreachable')
  return res.json()
}

// ── Admin Endpoints ──────────────────────────────────────────────────────────

export interface AdminStatsResponse {
  total_predictions: number
  total_chat_sessions: number
  total_reviews: number
  active_doctors: number
  avg_rating: number | null
  top_icd10_codes: { code: string; count: number }[]
}

export interface AdminReview {
  id: string
  rating: number
  accuracy_rating: number | null
  interpretability_rating: number | null
  comment: string | null
  created_at: string
  doctor: {
    full_name: string
    email: string
    specialty: string
  }
  prediction: {
    id: string
    input_text: string
  }
}

export interface ReviewListResponse {
  reviews: AdminReview[]
  total: number
  limit: number
  offset: number
}

export async function fetchAdminStats(token: string): Promise<AdminStatsResponse> {
  const res = await fetch(`${API_URL}/api/admin/stats`, {
    headers: authHeaders(token),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error((err as any).detail || `Failed to load admin stats (${res.status})`)
  }
  return res.json()
}

export async function fetchAdminReviews(token: string, offset = 0, limit = 50): Promise<ReviewListResponse> {
  const res = await fetch(`${API_URL}/api/admin/reviews?offset=${offset}&limit=${limit}`, {
    headers: authHeaders(token),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error((err as any).detail || `Failed to load admin reviews (${res.status})`)
  }
  return res.json()
}
