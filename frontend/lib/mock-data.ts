import type { PredictResponse, SampleNote } from '@/types'

// ── Mock predictions keyed by scenario slug ──────────────────────────────────

export const MOCK_SCENARIOS: Record<string, PredictResponse> = {
  heart_failure: {
    prediction_id: null,
    predictions: [
      { rank: 1, code: 'I50.9', description: 'Heart failure, unspecified', confidence: 0.91, threshold: 0.5, above_threshold: true },
      { rank: 2, code: 'I50.1', description: 'Left ventricular failure, unspecified', confidence: 0.84, threshold: 0.5, above_threshold: true },
      { rank: 3, code: 'I10',   description: 'Essential (primary) hypertension', confidence: 0.72, threshold: 0.5, above_threshold: true },
      { rank: 4, code: 'J96.0', description: 'Acute respiratory failure', confidence: 0.61, threshold: 0.5, above_threshold: true },
      { rank: 5, code: 'E11.9', description: 'Type 2 diabetes mellitus without complications', confidence: 0.44, threshold: 0.5, above_threshold: false },
    ],
    activated_concepts: [
      { concept: 'dyspnea', score: 0.94, active: true },
      { concept: 'bilateral_edema', score: 0.89, active: true },
      { concept: 'orthopnea', score: 0.86, active: true },
      { concept: 'elevated_BNP', score: 0.82, active: true },
      { concept: 'reduced_EF', score: 0.78, active: true },
      { concept: 'S3_gallop', score: 0.67, active: true },
      { concept: 'pulmonary_crackles', score: 0.65, active: true },
      { concept: 'hypertension', score: 0.61, active: true },
    ],
    metadata: { inference_time_ms: 142, model_version: 'demo', threshold_source: 'tuned' },
  },
  pneumonia: {
    prediction_id: null,
    predictions: [
      { rank: 1, code: 'J18.9', description: 'Pneumonia, unspecified organism', confidence: 0.88, threshold: 0.5, above_threshold: true },
      { rank: 2, code: 'J18.1', description: 'Lobar pneumonia, unspecified organism', confidence: 0.79, threshold: 0.5, above_threshold: true },
      { rank: 3, code: 'J96.0', description: 'Acute respiratory failure', confidence: 0.66, threshold: 0.5, above_threshold: true },
      { rank: 4, code: 'R05.9', description: 'Cough, unspecified', confidence: 0.58, threshold: 0.5, above_threshold: true },
      { rank: 5, code: 'A41.9', description: 'Sepsis, unspecified organism', confidence: 0.38, threshold: 0.5, above_threshold: false },
    ],
    activated_concepts: [
      { concept: 'fever', score: 0.91, active: true },
      { concept: 'productive_cough', score: 0.87, active: true },
      { concept: 'consolidation_on_CXR', score: 0.83, active: true },
      { concept: 'leukocytosis', score: 0.76, active: true },
      { concept: 'pleuritic_chest_pain', score: 0.69, active: true },
      { concept: 'decreased_O2_sat', score: 0.62, active: true },
    ],
    metadata: { inference_time_ms: 138, model_version: 'demo', threshold_source: 'tuned' },
  },
  aki: {
    prediction_id: null,
    predictions: [
      { rank: 1, code: 'N17.9', description: 'Acute kidney injury, unspecified', confidence: 0.92, threshold: 0.5, above_threshold: true },
      { rank: 2, code: 'N17.0', description: 'Acute kidney injury with tubular necrosis', confidence: 0.71, threshold: 0.5, above_threshold: true },
      { rank: 3, code: 'E87.5', description: 'Hyperkalemia', confidence: 0.65, threshold: 0.5, above_threshold: true },
      { rank: 4, code: 'N19',   description: 'Unspecified kidney failure', confidence: 0.54, threshold: 0.5, above_threshold: true },
      { rank: 5, code: 'I10',   description: 'Essential (primary) hypertension', confidence: 0.41, threshold: 0.5, above_threshold: false },
    ],
    activated_concepts: [
      { concept: 'rising_creatinine', score: 0.95, active: true },
      { concept: 'oliguria', score: 0.88, active: true },
      { concept: 'hyperkalemia', score: 0.72, active: true },
      { concept: 'metabolic_acidosis', score: 0.68, active: true },
      { concept: 'decreased_urine_output', score: 0.64, active: true },
      { concept: 'fluid_overload', score: 0.55, active: true },
    ],
    metadata: { inference_time_ms: 129, model_version: 'demo', threshold_source: 'tuned' },
  },
  sepsis: {
    prediction_id: null,
    predictions: [
      { rank: 1, code: 'A41.9', description: 'Sepsis, unspecified organism', confidence: 0.89, threshold: 0.5, above_threshold: true },
      { rank: 2, code: 'A41.01', description: 'Sepsis due to Methicillin susceptible Staph aureus', confidence: 0.67, threshold: 0.5, above_threshold: true },
      { rank: 3, code: 'R65.21', description: 'Severe sepsis with septic shock', confidence: 0.59, threshold: 0.5, above_threshold: true },
      { rank: 4, code: 'J18.9', description: 'Pneumonia, unspecified organism', confidence: 0.52, threshold: 0.5, above_threshold: true },
      { rank: 5, code: 'N17.9', description: 'Acute kidney injury, unspecified', confidence: 0.47, threshold: 0.5, above_threshold: false },
    ],
    activated_concepts: [
      { concept: 'fever', score: 0.88, active: true },
      { concept: 'tachycardia', score: 0.85, active: true },
      { concept: 'hypotension', score: 0.81, active: true },
      { concept: 'leukocytosis', score: 0.78, active: true },
      { concept: 'elevated_lactate', score: 0.74, active: true },
      { concept: 'altered_mental_status', score: 0.61, active: true },
      { concept: 'source_of_infection', score: 0.58, active: true },
    ],
    metadata: { inference_time_ms: 155, model_version: 'demo', threshold_source: 'tuned' },
  },
  stroke: {
    prediction_id: null,
    predictions: [
      { rank: 1, code: 'I63.9', description: 'Cerebral infarction, unspecified', confidence: 0.87, threshold: 0.5, above_threshold: true },
      { rank: 2, code: 'I63.5', description: 'Cerebral infarction due to unspecified occlusion or stenosis of cerebral artery', confidence: 0.75, threshold: 0.5, above_threshold: true },
      { rank: 3, code: 'G45.9', description: 'Transient cerebral ischaemic attack, unspecified', confidence: 0.58, threshold: 0.5, above_threshold: true },
      { rank: 4, code: 'I10',   description: 'Essential (primary) hypertension', confidence: 0.62, threshold: 0.5, above_threshold: true },
      { rank: 5, code: 'I48.91', description: 'Unspecified atrial fibrillation', confidence: 0.49, threshold: 0.5, above_threshold: false },
    ],
    activated_concepts: [
      { concept: 'sudden_focal_deficit', score: 0.93, active: true },
      { concept: 'facial_droop', score: 0.87, active: true },
      { concept: 'arm_weakness', score: 0.84, active: true },
      { concept: 'speech_difficulty', score: 0.79, active: true },
      { concept: 'diffusion_restriction_on_MRI', score: 0.71, active: true },
      { concept: 'hypertension', score: 0.65, active: true },
    ],
    metadata: { inference_time_ms: 133, model_version: 'demo', threshold_source: 'tuned' },
  },
}

// ── Keyword → scenario matching ───────────────────────────────────────────────

const KEYWORDS: Array<{ pattern: RegExp; scenario: keyof typeof MOCK_SCENARIOS }> = [
  { pattern: /heart failure|HF|CHF|cardiomyopathy|BNP|ejection fraction|EF|orthopnea|bilateral.*edema/i, scenario: 'heart_failure' },
  { pattern: /pneumonia|consolidation|lobar|productive cough|chest.*x.?ray|infiltrate/i, scenario: 'pneumonia' },
  { pattern: /AKI|acute kidney|creatinine|oliguria|renal failure|dialysis/i, scenario: 'aki' },
  { pattern: /sepsis|septic|bacteremia|lactic acid|lactate|SIRS/i, scenario: 'sepsis' },
  { pattern: /stroke|CVA|TIA|infarct|facial droop|hemiplegia|aphasia|MRI.*diffusion/i, scenario: 'stroke' },
]

export function selectMockResult(text: string): PredictResponse {
  for (const { pattern, scenario } of KEYWORDS) {
    if (pattern.test(text)) return MOCK_SCENARIOS[scenario]
  }
  return MOCK_SCENARIOS.heart_failure
}

// ── Mock sample notes ─────────────────────────────────────────────────────────

export const MOCK_NOTES: SampleNote[] = [
  {
    id: 'demo-hf-1',
    title: 'Congestive Heart Failure',
    category: 'Cardiology',
    note_length: 380,
    text: '72M with history of hypertension and T2DM presented with 3-day history of progressive dyspnea on exertion, orthopnea (3-pillow), and bilateral lower extremity edema. Exam: BP 158/96, HR 98, O2 sat 91% on RA. JVD present. Bilateral crackles at lung bases. 2+ pitting edema bilateral ankles. CXR: cardiomegaly, pulmonary vascular congestion. BNP 1240 pg/mL. Echo: EF 30%, dilated LV. Dx: decompensated CHF. Started on IV furosemide, ACE-I, beta-blocker.',
    expected_codes: ['I50.9', 'I50.1'],
  },
  {
    id: 'demo-pna-1',
    title: 'Community-Acquired Pneumonia',
    category: 'Pulmonary',
    note_length: 320,
    text: '58F presented with 4-day history of fever (Tmax 38.9°C), productive cough with yellow-green sputum, and right-sided pleuritic chest pain. Exam: HR 102, RR 22, O2 sat 94% on RA. Decreased breath sounds right lower lobe, dullness to percussion. WBC 16.4K. CXR: right lower lobe consolidation. Started on azithromycin + ceftriaxone. PSI Class III. Dx: community-acquired pneumonia.',
    expected_codes: ['J18.9', 'J18.1'],
  },
  {
    id: 'demo-aki-1',
    title: 'Acute Kidney Injury',
    category: 'Renal',
    note_length: 310,
    text: '65M with CKD stage 2 and diabetes presented with decreased urine output for 24h. No new nephrotoxins. Exam: BP 142/88, HR 84, 2+ edema. Labs: Cr 4.2 (baseline 1.4), BUN 68, K+ 5.8, bicarb 18, anion gap 16. UA: muddy brown casts. No obstruction on renal US. Dx: acute kidney injury, likely ATN. Renally dosed medications, nephrology consult, monitor for dialysis indications.',
    expected_codes: ['N17.9', 'N17.0'],
  },
  {
    id: 'demo-sep-1',
    title: 'Sepsis with Septic Shock',
    category: 'Infectious Disease',
    note_length: 345,
    text: '48M presented via EMS unresponsive with fever (39.4°C), BP 78/44, HR 128, RR 28. Found down at home. WBC 22K with left shift. Lactate 4.8 mmol/L. CXR: bilateral infiltrates. Blood cultures x2 drawn. Started on broad-spectrum IV antibiotics, 2L NS bolus, vasopressors (norepinephrine). Intubated for airway protection. Dx: severe sepsis with septic shock, presumed pulmonary source.',
    expected_codes: ['A41.9', 'R65.21'],
  },
  {
    id: 'demo-stroke-1',
    title: 'Acute Ischemic Stroke',
    category: 'Neurology',
    note_length: 330,
    text: '69F with Afib, hypertension, hyperlipidemia presented with sudden onset right facial droop, right arm weakness (4/5), and expressive aphasia beginning 90 minutes prior. NIHSS 12. BP 178/102. ECG: Afib. CT head: no hemorrhage. CTA head/neck: M1 occlusion left MCA. MRI DWI: restricted diffusion left MCA territory. IV tPA administered, transferred for thrombectomy. INR 1.1 (not on anticoagulation).',
    expected_codes: ['I63.9', 'I63.5'],
  },
]

// ── Mock chat responses ────────────────────────────────────────────────────────

export const MOCK_CHAT_RESPONSES: Record<string, string> = {
  default: `Based on the clinical note, the ShifaMind model identified several key activated concepts that contributed to these predictions.

The top diagnosis reflects the constellation of clinical findings. The confidence scores indicate the model's certainty based on patterns learned from clinical documentation.

**Key factors driving the top prediction:**
- Multiple high-scoring activated concepts aligned with the diagnosis
- Above-threshold confidence score indicating strong signal
- Consistent clinical narrative

**Suggested next steps:**
1. Review the Concepts tab to understand which clinical findings were most influential
2. Consider the Attribution map to see concept-to-diagnosis relationships
3. Correlate with clinical judgment — AI predictions are decision support, not replacement

*Note: This is a demo response. Connect the backend API for AI-powered clinical discussion.*`,
}

export function selectMockChatResponse(message: string): string {
  const lmsg = message.toLowerCase()
  if (lmsg.includes('heart failure') || lmsg.includes('chf') || lmsg.includes('predicted')) {
    return `Heart failure was predicted because the model detected a strong cluster of cardiac-specific concepts in the note.

**Key activated concepts:**
- **dyspnea** (0.94) — progressive exertional dyspnea is a cardinal symptom
- **orthopnea** (0.86) — positional dyspnea indicates elevated filling pressures
- **bilateral_edema** (0.89) — peripheral edema from venous congestion
- **elevated_BNP** (0.82) — directly reflects myocardial stretch and wall stress
- **reduced_EF** (0.78) — echocardiographic confirmation of systolic dysfunction

The combination of these concepts creates a very high-confidence prediction for heart failure (0.91), well above the tuned threshold of 0.50.

*Note: Demo response. Real analysis requires the backend API.*`
  }

  if (lmsg.includes('concept') || lmsg.includes('activated')) {
    return `The activated concepts represent clinical features the model extracted from the note.

Each concept has a score (0-1) indicating how strongly it was detected. Concepts with **active: true** exceeded the activation threshold and contributed positively to the top diagnoses.

**High-scoring concepts** (>0.8) have the strongest influence on predictions. You can see the full concept-to-diagnosis mapping in the **Attribution** tab.

*Note: Demo response. Real analysis requires the backend API.*`
  }

  if (lmsg.includes('workup') || lmsg.includes('recommend') || lmsg.includes('next')) {
    return `Based on the predicted diagnoses, consider the following workup:

**Immediate:**
- Repeat vital signs and clinical assessment
- Labs: CBC, CMP, relevant biomarkers (BNP, troponin, lactate as applicable)
- ECG and chest X-ray if not already obtained

**Confirmatory:**
- Echocardiogram for cardiac diagnoses
- CT or MRI depending on clinical context
- Specialist consultation as appropriate

**Monitoring:**
- Fluid balance and daily weights
- Serial labs to track trends
- Response to initial interventions

*This is AI-generated clinical decision support. Always apply clinical judgment. Demo response.*`
  }

  return MOCK_CHAT_RESPONSES.default
}
