import { createClient } from './supabase/client'
import type { PredictResponse, SampleNote, ReviewPayload } from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? ''

async function getAuthHeader(): Promise<Record<string, string>> {
  const supabase = createClient()
  const { data: { session } } = await supabase.auth.getSession()
  if (!session?.access_token) throw new Error('Not authenticated')
  return { Authorization: `Bearer ${session.access_token}` }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const authHeader = await getAuthHeader()
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...authHeader,
      ...init?.headers,
    },
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body?.detail ?? `API error ${res.status}`)
  }
  return res.json() as Promise<T>
}

// ── Predict ───────────────────────────────────────────────────────────────────

export async function predict(
  text: string,
  applyTunedThresholds = true
): Promise<PredictResponse> {
  return apiFetch<PredictResponse>('/api/predict', {
    method: 'POST',
    body: JSON.stringify({ text, apply_tuned_thresholds: applyTunedThresholds }),
  })
}

// ── Notes ─────────────────────────────────────────────────────────────────────

export async function listNotes(): Promise<SampleNote[]> {
  return apiFetch<SampleNote[]>('/api/notes')
}

export async function getNote(id: string): Promise<SampleNote> {
  return apiFetch<SampleNote>(`/api/notes/${id}`)
}

// ── Reviews ───────────────────────────────────────────────────────────────────

export async function submitReview(payload: ReviewPayload): Promise<{ id: string }> {
  return apiFetch<{ id: string }>('/api/reviews', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// ── Health ────────────────────────────────────────────────────────────────────

export async function healthCheck(): Promise<{ status: string; model_loaded: boolean }> {
  const res = await fetch(`${API_URL}/api/health`)
  return res.json()
}

// ── SSE (used by Part 3 chat) ─────────────────────────────────────────────────

export async function getAuthToken(): Promise<string> {
  const supabase = createClient()
  const { data: { session } } = await supabase.auth.getSession()
  if (!session?.access_token) throw new Error('Not authenticated')
  return session.access_token
}
