from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


# ── Predict ──────────────────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=50000)
    apply_tuned_thresholds: bool = True


class PredictedCode(BaseModel):
    rank: int
    code: str
    description: str
    confidence: float
    threshold: float
    above_threshold: bool


class ActivatedConcept(BaseModel):
    concept: str
    score: float
    active: bool


class PredictMetadata(BaseModel):
    inference_time_ms: int
    model_version: str
    threshold_source: str


class PredictResponse(BaseModel):
    predictions: list[PredictedCode]
    activated_concepts: list[ActivatedConcept]
    metadata: PredictMetadata
    prediction_id: Optional[str] = None


# ── Notes ─────────────────────────────────────────────────────────────────────

class SampleNote(BaseModel):
    id: str
    title: str
    category: str
    text: str
    note_length: int
    expected_codes: Optional[list[str]] = None


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    prediction_id: Optional[str] = None
    session_id: Optional[str] = None
    stream: bool = True


# ── Reviews ───────────────────────────────────────────────────────────────────

class ReviewRequest(BaseModel):
    prediction_id: str
    rating: int = Field(..., ge=1, le=5)
    accuracy_rating: Optional[int] = Field(None, ge=1, le=5)
    interpretability_rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    corrections: Optional[dict] = None


class ReviewResponse(BaseModel):
    id: str
    created_at: datetime


# ── Health ────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    llm_provider: str
    version: str = "1.0.0"
