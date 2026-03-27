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

// ── Convenience exports ───────────────────────────────────────────────────────

/** All mock predictions as a flat array (for consumers that need a list). */
export const MOCK_PREDICTIONS = Object.values(MOCK_SCENARIOS)

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

/** Alias used by components that want the named export. */
export const findMockPrediction = selectMockResult

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

/** Alias — preferred import name for note-selector components. */
export const MOCK_SAMPLE_NOTES = MOCK_NOTES

// ── Context-aware mock chat responses ─────────────────────────────────────────

type Prediction = PredictResponse['predictions'][number]
type Concept = PredictResponse['activated_concepts'][number]

function fmt(label: string) {
  return label.replace(/_/g, ' ')
}

export function generateMockChatResponse(
  userMessage: string,
  predictions: Prediction[],
  concepts: Concept[]
): string {
  const lmsg = userMessage.toLowerCase()
  const topDx = predictions[0]
  const secondDx = predictions[1]
  const activeConcepts = concepts.filter(c => c.active).slice(0, 5)
  const conceptList = activeConcepts
    .map(c => `- **${fmt(c.concept)}** (score: ${c.score.toFixed(2)})`)
    .join('\n')

  // "Why was X predicted?" / "What was predicted?" / "Explain the prediction"
  if (
    lmsg.includes('why') ||
    lmsg.includes('predicted') ||
    lmsg.includes('explain') ||
    lmsg.includes('reason')
  ) {
    if (topDx) {
      return `**${topDx.description} (${topDx.code})** was the top prediction with a confidence of ${(topDx.confidence * 100).toFixed(0)}%, well above the tuned threshold of ${(topDx.threshold * 100).toFixed(0)}%.

The BioClinicalBERT model extracted the following activated concepts as the primary drivers:
${conceptList}

The co-occurrence of these findings creates a high-confidence diagnostic signal. The model learned this concept cluster from de-identified clinical notes and associated it strongly with ${topDx.description}.${secondDx ? `\n\n**${secondDx.description} (${secondDx.code})** was ranked second at ${(secondDx.confidence * 100).toFixed(0)}% confidence, reflecting the clinical overlap common between these conditions. Reviewing the Attribution tab will show exactly which concepts link to each diagnosis.` : ''}

*This is a ShifaMind demo response. Connect the backend API for live AI-powered clinical discussion.*`
    }
  }

  // "What concepts were activated?" / "Key concepts" / "What features?"
  if (
    lmsg.includes('concept') ||
    lmsg.includes('activated') ||
    lmsg.includes('feature') ||
    lmsg.includes('key')
  ) {
    return `The model activated **${activeConcepts.length} concepts** above threshold from the clinical note. Each score (0–1) reflects detection strength:

${conceptList}

Concepts with scores above **0.80** have the strongest influence on the top predictions. The Concepts tab shows all ${concepts.length} extracted features with their scores, and the Attribution tab maps each concept to the diagnoses it contributed to.

High-scoring concepts like **${activeConcepts[0] ? fmt(activeConcepts[0].concept) : 'the top concept'}** are particularly important because they are specific to the leading diagnosis and rarely activated in other conditions.

*This is a ShifaMind demo response. Connect the backend API for real-time analysis.*`
  }

  // "What workup?" / "Next steps?" / "Recommend?"
  if (
    lmsg.includes('workup') ||
    lmsg.includes('recommend') ||
    lmsg.includes('next step') ||
    lmsg.includes('management') ||
    lmsg.includes('treatment')
  ) {
    const dxLine = topDx
      ? `Based on the top prediction of **${topDx.description} (${topDx.code})** at ${(topDx.confidence * 100).toFixed(0)}% confidence`
      : 'Based on the predicted diagnoses'

    return `${dxLine}, the following workup and management steps are worth considering:

**Immediate assessment:**
- Repeat focused history and physical exam to confirm clinical correlation
- Vital signs trending and hemodynamic stability assessment
- Relevant biomarkers and targeted labs based on the leading diagnosis

**Confirmatory investigations:**
- Imaging and diagnostic studies appropriate to the top-ranked ICD-10 codes
- Subspecialty consultation where indicated${secondDx ? ` (consider ${secondDx.description} in the differential)` : ''}

**Ongoing monitoring:**
- Serial labs to track key parameters identified by the model
- Clinical response to initial interventions
- Reassessment if clinical trajectory diverges from the predicted diagnosis

Remember that ShifaMind's predictions are clinical decision support — the final clinical judgment always rests with the treating physician.

*This is a ShifaMind demo response. Connect the backend API for context-grounded clinical discussion.*`
  }

  // "What differentials?" / "Other diagnoses?" / "Differential diagnosis"
  if (
    lmsg.includes('differential') ||
    lmsg.includes('other diagnos') ||
    lmsg.includes('alternative')
  ) {
    const abovePreds = predictions.filter(p => p.above_threshold)
    const belowPreds = predictions.filter(p => !p.above_threshold)
    const aboveList = abovePreds.map(p => `- **${p.code}** ${p.description} — ${(p.confidence * 100).toFixed(0)}%`).join('\n')
    const belowList = belowPreds.map(p => `- **${p.code}** ${p.description} — ${(p.confidence * 100).toFixed(0)}% *(below threshold)*`).join('\n')

    return `The model returned ${predictions.length} ranked diagnoses for this clinical presentation.

**Above-threshold predictions** (strong signal):
${aboveList || '- None'}

${belowList ? `**Below-threshold considerations** (weaker signal — worth keeping in mind):\n${belowList}\n\n` : ''}The threshold of ${topDx ? (topDx.threshold * 100).toFixed(0) : 50}% was tuned on validation data to optimize sensitivity-specificity balance. Below-threshold predictions should not be dismissed — they may represent early or atypical presentations.

Consider each code in the context of the full clinical picture. The Concepts tab can help you understand which features are driving each prediction.

*This is a ShifaMind demo response. Connect the backend API for AI-powered differential discussion.*`
  }

  // Default response — references top diagnosis and concepts
  const topLine = topDx
    ? `The analysis returned **${topDx.description} (${topDx.code})** as the top prediction at ${(topDx.confidence * 100).toFixed(0)}% confidence.`
    : 'The analysis returned several predictions for this clinical note.'

  return `${topLine} ${activeConcepts.length} concepts were activated above threshold, with the strongest signals from **${activeConcepts[0] ? fmt(activeConcepts[0].concept) : 'key clinical features'}** and **${activeConcepts[1] ? fmt(activeConcepts[1].concept) : 'supporting findings'}**.

You can explore the predictions further:
- **Diagnoses tab** — ranked ICD-10 codes with confidence scores
- **Concepts tab** — all extracted clinical features with activation scores
- **Attribution tab** — concept-to-diagnosis mapping showing which features drive each code

Feel free to ask me to explain the top prediction, walk through the differentials, or suggest workup steps based on these findings.

*This is a ShifaMind demo response. Connect the backend API for live AI-powered clinical discussion.*`
}

/** Legacy export — kept for backward compatibility. */
export function selectMockChatResponse(message: string): string {
  return generateMockChatResponse(message, [], [])
}
