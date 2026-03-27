"""
seed_notes.py — Load 10 synthetic MIMIC-IV-style clinical notes into Supabase sample_notes table.

Usage:
    SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... python scripts/seed_notes.py

Notes are clinically realistic but entirely synthetic (no real patient data).
"""

import os
import sys
import uuid
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

SAMPLE_NOTES = [
    {
        "title": "Heart Failure with Bilateral Pleural Effusions",
        "category": "Cardiology",
        "expected_codes": ["I50.9", "I50.32", "J91.8"],
        "text": """72M with history of ischemic cardiomyopathy (EF 30%), hypertension, and type 2 diabetes presented with 2-week progressive dyspnea, orthopnea requiring 3-pillow positioning, and bilateral lower extremity edema to the knees.

Vitals on admission: BP 158/94, HR 102, RR 22, SpO2 89% on room air, afebrile.

Exam: JVD to 12 cm H2O, bibasilar crackles, S3 gallop, 3+ pitting edema bilateral LE to mid-thigh.

Labs: BNP 4200 pg/mL, creatinine 1.8 (baseline 1.4), sodium 131, troponin I 0.04.
CXR: Bilateral pleural effusions, cardiomegaly, Kerley B lines.
Echo: EF 28% (prior 32%), moderate MR, elevated filling pressures.

Assessment: Acute on chronic diastolic and systolic heart failure exacerbation with cardiorenal syndrome. Volume overloaded.

Plan: IV furosemide 80 mg BID, fluid restriction 1.5L/day, low-sodium diet, daily weights, telemetry, nephrology consult for creatinine trend.""",
    },
    {
        "title": "Community-Acquired Pneumonia with Sepsis",
        "category": "Pulmonary",
        "expected_codes": ["J18.9", "A41.9", "R65.20"],
        "text": """58F, never-smoker, presented via ED with 5 days of productive cough with rust-colored sputum, fever to 39.8°C, pleuritic chest pain right side, and new confusion.

PMH: Diabetes mellitus type 2, GERD. No recent travel or sick contacts.

Vitals: T 39.6, HR 118, BP 88/56, RR 28, SpO2 91% on 4L NC.

Exam: Ill-appearing, tachypneic, dull to percussion right lower lobe, bronchial breath sounds, egophony present.

Labs: WBC 22.4 (92% neutrophils, 8% bands), lactic acid 3.8, procalcitonin 18.4, creatinine 2.1, blood cultures x2 pending.
ABG: pH 7.28, pCO2 32, pO2 58, HCO3 15.
CXR: Dense right lower lobe consolidation with air bronchograms.

Assessment: Severe community-acquired pneumonia complicated by sepsis (qSOFA 3) and hypoxemic respiratory failure.

Plan: Broad-spectrum antibiotics (ceftriaxone + azithromycin), 30 mL/kg IVF bolus, vasopressors if refractory, ICU transfer, repeat cultures, ID consult.""",
    },
    {
        "title": "Septic Shock — Gram-Negative Source",
        "category": "Infectious Disease",
        "expected_codes": ["A41.51", "R65.21", "N39.0"],
        "text": """81M, nursing home resident, brought in with altered mental status, not responding to verbal commands, found diaphoretic and hypotensive.

PMH: BPH, chronic kidney disease stage 3, atrial fibrillation on warfarin.

Vitals: T 38.9, HR 124 (AF), BP 72/40 (MAP 47), RR 30, SpO2 88% on NRB mask.

Exam: Lethargic, not following commands, dry mucous membranes, suprapubic tenderness, indwelling Foley (3 weeks per facility), no skin findings.

Labs: WBC 28.6, lactate 5.2, creatinine 4.1 (baseline 1.9), UA: >100 WBC, many bacteria, nitrite positive, blood cultures x2 drawn.
ABG: pH 7.18, metabolic acidosis with respiratory compensation.
EKG: Rapid AF, rate 124.

Assessment: Septic shock presumed catheter-associated UTI / urosepsis. Acute kidney injury on CKD. Demand ischemia.

Plan: Norepinephrine infusion, MAP goal 65+, piperacillin-tazobactam, remove and replace Foley, 2L IVF, ICU admission, hold warfarin, nephrology consult.""",
    },
    {
        "title": "Acute Kidney Injury — Contrast Nephropathy",
        "category": "Renal",
        "expected_codes": ["N17.9", "E87.5", "E87.1"],
        "text": """67M with CKD stage 3 (baseline Cr 2.0) admitted 3 days after coronary CTA for worsening oliguria and fatigue. Cr now 5.4.

PMH: Hypertension, CAD, diabetes type 2, CKD. Medications include metformin (held before procedure), lisinopril.

Vitals: BP 178/102, HR 78, afebrile, RR 18, SpO2 96% on RA.

Exam: Mild bilateral ankle edema, no JVD, lungs clear.

Labs: Creatinine 5.4 (from 2.0 baseline), BUN 88, K+ 5.9, Na 133, bicarb 15, Hgb 9.2, UA: granular casts, no protein.
Urine output last 24h: 380 mL.

Renal US: No hydronephrosis, slightly echogenic kidneys, normal Dopplers.

Assessment: Acute kidney injury likely contrast-induced nephropathy on CKD. Hyperkalemia, metabolic acidosis, hyponatremia.

Plan: IV fluid hydration (NS 1 mL/kg/hr), hold nephrotoxins (lisinopril, NSAIDs, metformin), sodium bicarbonate, kayexalate for hyperkalemia, continuous renal monitoring, nephrology consult for dialysis planning if worsens.""",
    },
    {
        "title": "Diabetic Ketoacidosis — Type 1",
        "category": "Endocrine",
        "expected_codes": ["E10.10", "E87.1", "E11.65"],
        "text": """24F with known type 1 diabetes (on insulin pump, last A1c 11.2%) presented with 2-day nausea, vomiting, abdominal pain, and polyuria. Found to have missed multiple insulin doses due to pump malfunction.

Vitals: T 37.2, HR 128, BP 96/62, RR 32 (Kussmaul), SpO2 98%.

Exam: Fruity breath odor, dry mucous membranes, diffuse abdominal tenderness (non-surgical), decreased skin turgor.

Labs: Glucose 482, bicarb 7, anion gap 28, pH 7.12 (arterial), K+ 6.1, Na 128 (corrected 135), ketones large, beta-hydroxybutyrate 8.4 mmol/L, creatinine 1.6.

UA: Large glucose, large ketones.

Assessment: Severe DKA precipitated by insulin pump failure. Severe dehydration, hyperkalemia (total body K+ depleted), hyponatremia.

Plan: Insulin drip 0.1 units/kg/hr (after K+ ≥3.5), aggressive IV fluid resuscitation (NS 1L/hr x1, then 500 mL/hr), K+ replacement, q1h glucose/electrolytes, anion gap monitoring, endocrine consult, DKA protocol.""",
    },
    {
        "title": "Upper GI Bleed — Peptic Ulcer Disease",
        "category": "GI",
        "expected_codes": ["K92.0", "K25.4", "D64.9"],
        "text": """55M heavy alcohol user (>8 drinks/day for 20 years) presented with sudden onset hematemesis x3 episodes (estimated 600 mL blood), melena, lightheadedness.

PMH: Peptic ulcer disease (H. pylori positive, treated 2 years ago), liver cirrhosis (Child-Pugh B), GERD.

Vitals: T 37.1, HR 114, BP 90/58 (supine), orthostatic drop 20 mmHg, RR 20, SpO2 97%.

Exam: Pale, diaphoretic, epigastric tenderness, guaiac positive stool, no peritoneal signs. Spider angiomata, palmar erythema, mild splenomegaly.

Labs: Hgb 6.8 (MCV 104), INR 2.1, platelets 88K, creatinine 1.3, albumin 2.6, MELD score 18.
BUN/Cr ratio: 34 (elevated, consistent with UGI source).

Assessment: Active upper GI hemorrhage, likely peptic ulcer vs. variceal source given cirrhosis history. Hemodynamic compromise.

Plan: 2 large-bore IVs, pRBC transfusion (target Hgb >7), PPI infusion (pantoprazole 80 mg bolus then 8 mg/hr), octreotide, ceftriaxone (SBP prophylaxis), urgent EGD within 24h, GI/hepatology consult, ICU level care.""",
    },
    {
        "title": "Acute Ischemic Stroke — Left MCA Territory",
        "category": "Neurology",
        "expected_codes": ["I63.9", "I48.91", "G45.9"],
        "text": """78F with atrial fibrillation (not on anticoagulation, refused), hypertension, and dyslipidemia brought by family with sudden onset right arm weakness and aphasia, last known well 2 hours ago.

Vitals: T 37.0, HR 88 (irregular), BP 188/104, RR 16, SpO2 96% on RA.

Neuro exam: Alert, global aphasia (cannot follow commands, no fluent speech, no repetition), right face/arm weakness (3/5), right leg mildly weak (4/5), right homonymous hemianopia. NIHSS 16.

EKG: Atrial fibrillation, rate 88, no ST changes.

CT head non-contrast: No hemorrhage, early sulcal effacement left MCA territory.
CT perfusion: Large ischemic penumbra left MCA, core infarct ~18 mL, penumbra ~85 mL.
CT angiography: Left M1 occlusion, mild stenosis right ICA.

Assessment: Large vessel occlusion ischemic stroke, left MCA, within thrombectomy window.

Plan: Immediate transfer to interventional suite for mechanical thrombectomy. IV tPA 0.9 mg/kg (10% bolus, 90% over 60 min) initiated. Stroke protocol, neurology/neurosurgery at bedside, hold antihypertensives (target <180/105 pre-tPA).""",
    },
    {
        "title": "COPD Exacerbation with Respiratory Failure",
        "category": "Pulmonary",
        "expected_codes": ["J44.1", "J96.00", "J18.9"],
        "text": """70M with severe COPD (GOLD IV, FEV1 28% predicted), cor pulmonale, and 60 pack-year history presented with 4-day worsening dyspnea, increased sputum production (purulent, green), and decreased exercise tolerance (now SOB at rest).

PMH: 2 prior intubations, home O2 at 2L, COPD exacerbation x3 last year.

Vitals: T 37.8, HR 108, BP 144/88, RR 32, SpO2 82% on 4L NC.

Exam: Barrel chest, pursed-lip breathing, use of accessory muscles, tripod positioning. Diffuse expiratory wheeze, prolonged expiratory phase, distant breath sounds.
ABG (on 4L NC): pH 7.26, pCO2 72, pO2 52, HCO3 31.

CXR: Hyperinflation, flattened diaphragms, peribronchial cuffing, no infiltrate.
Sputum: Gram stain pending, prior cultures grew H. influenzae.

Assessment: Acute exacerbation COPD with hypercapnic respiratory failure. Likely infectious trigger.

Plan: Controlled O2 therapy (target SpO2 88-92%), high-flow BiPAP (IPAP 14, EPAP 6), ipratropium + albuterol nebs q4h, IV methylprednisolone 125 mg q8h x3 days then oral, azithromycin + amoxicillin-clavulanate, ICU monitoring, intubation threshold discussion with family.""",
    },
    {
        "title": "Atrial Fibrillation with Rapid Ventricular Response",
        "category": "Cardiology",
        "expected_codes": ["I48.91", "I50.9", "I10"],
        "text": """65F with history of paroxysmal atrial fibrillation (not on anticoagulation), hypertension, and obesity (BMI 38) presented with 6-hour onset palpitations, lightheadedness, and mild dyspnea.

PMH: HTN on amlodipine, OSA, no prior stroke or TIA.

Vitals: T 37.0, HR 152 (irregular), BP 146/90, RR 20, SpO2 95%.

Exam: Irregularly irregular rhythm, mild JVD, clear lungs bilaterally, no edema.

EKG: Atrial fibrillation, ventricular rate 152, no ST changes, no delta waves.
Labs: TSH 0.08 (suppressed), free T4 3.2 (elevated), troponin negative x2, BMP normal.
Echo (bedside): EF 55-60%, no wall motion abnormality, mild LA enlargement (4.3 cm).

CHA2DS2-VASc score: 3 (female sex, age, HTN).

Assessment: New symptomatic atrial fibrillation with rapid ventricular response. Hyperthyroidism likely precipitant. No hemodynamic instability.

Plan: Rate control with IV metoprolol 5 mg (titrate to HR <100), anticoagulation with rivaroxaban, endocrinology consult for hyperthyroidism, cardiology consult, DCCV if not converted in 48h, monitor for heart failure development.""",
    },
    {
        "title": "Multi-System Failure — Metastatic Malignancy",
        "category": "Multi-System",
        "expected_codes": ["C80.1", "N17.9", "D64.9", "R65.20"],
        "text": """68M with newly diagnosed metastatic non-small cell lung cancer (stage IV, brain + liver + bone mets, EGFR mutation positive, started erlotinib 3 weeks ago) admitted with progressive weakness, confusion, and inability to ambulate over 5 days.

PMH: 45 pack-year smoking history, COPD, hypertension, type 2 diabetes.

Vitals: T 38.2, HR 110, BP 100/64, RR 22, SpO2 90% on 2L NC. Weight loss 12 kg over 2 months.

Exam: Cachectic, confused, MMSE 18/30, right-sided weakness (3/5 arm, 4/5 leg), hypercalcemia signs (constipation, polyuria, band keratopathy), hepatomegaly 4 cm BCM, bilateral LE edema.

Labs: Ca2+ 13.8, creatinine 3.2 (baseline 0.9), BUN 78, Na 126, albumin 1.8, Hgb 7.2, WBC 14.2, LFTs: AST 220, ALT 180, alk phos 440, bili 2.8. PTHrP elevated.

CT head: Multiple brain metastases (largest 2.1 cm right parietal lobe, perilesional edema).
MRI spine: No cord compression.

Assessment: Multi-system failure in metastatic NSCLC. Hypercalcemia of malignancy (PTHrP-mediated), AKI (hypercalcemia + dehydration), hyponatremia (SIADH), anemia of chronic disease, hepatic involvement, brain metastases with focal neuro deficits.

Plan: IV zoledronic acid for hypercalcemia, aggressive hydration (NS 200 mL/hr), hold erlotinib temporarily, IV dexamethasone for brain edema, radiation oncology consult for brain SRS, palliative care consult, goals of care discussion, nephrology input, nutritional support.""",
    },
]


def main():
    try:
        from supabase import create_client
    except ImportError:
        print("Error: supabase package not installed. Run: pip install supabase")
        sys.exit(1)

    client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    created, skipped, failed = 0, 0, 0

    for note in SAMPLE_NOTES:
        print(f"  Inserting: {note['title'][:55]}...", end=" ")
        try:
            # Check if title already exists
            existing = client.table("sample_notes").select("id").eq("title", note["title"]).execute()
            if existing.data:
                print("SKIPPED (exists)")
                skipped += 1
                continue

            client.table("sample_notes").insert({
                "id": str(uuid.uuid4()),
                "title": note["title"],
                "category": note["category"],
                "text": note["text"].strip(),
                "expected_codes": note["expected_codes"],
                "is_active": True,
            }).execute()
            print("OK")
            created += 1
        except Exception as e:
            print(f"FAILED — {e}")
            failed += 1

    print(f"\nDone: {created} inserted, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
