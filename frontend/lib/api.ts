const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// ── Types ────────────────────────────────────────────────────────────────────

export interface PredictedCode {
  rank: number
  code: string
  description: string
  confidence: number
  threshold: number
  above_threshold: boolean
}

export interface ActivatedConcept {
  concept: string
  score: number
  active: boolean
}

export interface PredictResponse {
  predictions: PredictedCode[]
  activated_concepts: ActivatedConcept[]
  metadata: {
    inference_time_ms: number
    model_version: string
    threshold_source: string
  }
  prediction_id?: string
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

export async function predict(text: string, token: string): Promise<PredictResponse> {
  const res = await fetch(`${API_URL}/api/predict`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify({ text, apply_tuned_thresholds: true }),
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
