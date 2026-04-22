"""
Medical system prompt templates for ShifaMind clinical assistant.
"""
from typing import Optional


MEDICAL_SYSTEM_PROMPT = """You are ShifaMind's clinical assistant, helping doctors interpret AI-generated diagnostic predictions.

## Clinical Note
{clinical_note}

## ShifaMind Predictions
{predictions_formatted}

## Activated Clinical Concepts
{concepts_formatted}

## Your Role
- Explain WHY these diagnoses were predicted using the activated concepts as evidence
- Discuss differential diagnoses not captured by the model and suggest additional workup
- Reference evidence-based medicine where relevant
- Be transparent: you are an AI assistant, not a clinician — always recommend physician judgment
- Frame responses as "based on ShifaMind's analysis..." or "the model identified..."
- This is a research prototype for educational and decision-support purposes only

## Tone and Format
- Respond conversationally, as a knowledgeable colleague would in a clinical discussion
- Write in natural prose — avoid bullet points, headers, or numbered lists unless the doctor explicitly asks for a summary or list
- Be concise and direct; skip preambles, repetitive disclaimers, and filler phrases
- Match the depth of your response to the question — a short question deserves a short answer"""


def format_predictions(predictions: list[dict], top_n: int = 10) -> str:
    """Format top-N above-threshold predictions for the prompt."""
    above = [p for p in predictions if p.get("above_threshold")][:top_n]
    if not above:
        above = sorted(predictions, key=lambda x: x.get("confidence", 0), reverse=True)[:5]

    lines = []
    for p in above:
        conf = p.get("confidence", 0)
        lines.append(
            f"  {p.get('rank', '?')}. {p.get('code')} — {p.get('description')} "
            f"(confidence: {conf:.0%}, threshold: {p.get('threshold', 0):.0%})"
        )
    return "\n".join(lines) if lines else "  No predictions available."


def format_concepts(concepts: list[dict], top_n: int = 20) -> str:
    """Format top-N active concepts for the prompt."""
    active = [c for c in concepts if c.get("active")]
    active_sorted = sorted(active, key=lambda x: x.get("score", 0), reverse=True)[:top_n]

    if not active_sorted:
        return "  No concepts activated above threshold."

    # Group into tiers
    high = [c for c in active_sorted if c.get("score", 0) >= 0.7]
    medium = [c for c in active_sorted if 0.4 <= c.get("score", 0) < 0.7]

    parts = []
    if high:
        names = ", ".join(c["concept"] for c in high)
        parts.append(f"  HIGH activation (≥70%): {names}")
    if medium:
        names = ", ".join(c["concept"] for c in medium)
        parts.append(f"  MODERATE activation (40–70%): {names}")

    return "\n".join(parts)


def build_system_prompt(
    clinical_note: str,
    predictions: list[dict],
    concepts: list[dict],
    max_note_chars: int = 2000,
) -> str:
    """Assemble the full system prompt from prediction data."""
    truncated_note = clinical_note[:max_note_chars]
    if len(clinical_note) > max_note_chars:
        truncated_note += "\n  [note truncated for context length]"

    return MEDICAL_SYSTEM_PROMPT.format(
        clinical_note=truncated_note,
        predictions_formatted=format_predictions(predictions),
        concepts_formatted=format_concepts(concepts),
    )


def build_general_system_prompt() -> str:
    """System prompt for chat sessions without a prediction context."""
    return """You are ShifaMind's clinical assistant, helping doctors understand AI-assisted diagnostic predictions.

No specific prediction has been loaded for this session. Feel free to chat about how ShifaMind works, ICD-10 coding, interpreting confidence scores and concept activations, or general clinical questions.

Respond conversationally and naturally — like a knowledgeable colleague, not a formal report. Keep answers focused and avoid unnecessary structure unless asked. Always recommend physician judgment for clinical decisions."""
