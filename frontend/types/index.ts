// ── Prediction ────────────────────────────────────────────────────────────────

export interface PredictedCode {
  rank: number
  code: string
  description: string
  confidence: number   // 0–1
  threshold: number    // 0–1
  above_threshold: boolean
}

export interface ActivatedConcept {
  concept: string
  score: number   // 0–1
  active: boolean
}

export interface PredictMetadata {
  inference_time_ms: number
  model_version: string
  threshold_source: string
}

export interface PredictResponse {
  predictions: PredictedCode[]
  activated_concepts: ActivatedConcept[]
  metadata: PredictMetadata
  prediction_id: string | null
}

// ── Sample Notes ──────────────────────────────────────────────────────────────

export interface SampleNote {
  id: string
  title: string
  category: string
  text: string
  note_length: number
  expected_codes?: string[]
}

// ── Chat ──────────────────────────────────────────────────────────────────────

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  created_at: string
}

export interface ChatSession {
  id: string
  doctor_id: string
  prediction_id: string | null
  llm_provider: string
  llm_model: string
  created_at: string
}

// ── Reviews ───────────────────────────────────────────────────────────────────

export interface ReviewPayload {
  prediction_id: string
  rating: number
  accuracy_rating?: number
  interpretability_rating?: number
  comment?: string
  corrections?: Record<string, unknown>
}

// ── Doctor ────────────────────────────────────────────────────────────────────

export interface Doctor {
  id: string
  full_name: string
  specialty: string | null
  institution: string | null
  email: string
  role: 'doctor' | 'admin'
  is_active: boolean
}

// ── Concept attribution ───────────────────────────────────────────────────────

export interface AttributionLink {
  conceptIndex: number
  diagnosisIndex: number
  strength: number  // 0–1
}
