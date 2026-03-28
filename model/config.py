"""
ShifaMind Phase 1 — model configuration.

ICD-10 codes are in compact format (no dots) exactly matching the checkpoint's
top_50_codes list and optimal_thresholds.json keys.
Order is canonical — matches the diagnosis_head output indices.
"""

# ── 111 Clinical Concepts ─────────────────────────────────────────────────────
# Order matches concept_list.json and concept_head output indices.
CONCEPTS = [
    # Symptoms
    "fever", "cough", "dyspnea", "pain", "nausea", "vomiting", "diarrhea", "fatigue",
    "headache", "dizziness", "weakness", "confusion", "syncope", "chest", "abdominal",
    "dysphagia", "hemoptysis", "hematuria", "hematemesis", "melena", "jaundice",
    "edema", "rash", "pruritus", "weight", "anorexia", "malaise",
    # Vital sign abnormalities
    "hypotension", "hypertension", "tachycardia", "bradycardia", "tachypnea", "hypoxia",
    "hypothermia", "shock", "altered", "lethargic", "obtunded",
    # System involvement
    "cardiac", "pulmonary", "renal", "hepatic", "neurologic", "gastrointestinal",
    "respiratory", "cardiovascular", "genitourinary", "musculoskeletal", "endocrine",
    "hematologic", "dermatologic", "psychiatric",
    # Infectious
    "infection", "sepsis", "pneumonia", "uti", "cellulitis", "meningitis",
    # Pathophysiology
    "failure", "infarction", "ischemia", "hemorrhage", "thrombosis", "embolism",
    "obstruction", "perforation", "rupture", "stenosis", "regurgitation",
    "hypertrophy", "atrophy", "neoplasm", "malignancy", "metastasis",
    # Lab abnormalities
    "elevated", "decreased", "anemia", "leukocytosis", "thrombocytopenia",
    "hyperglycemia", "hypoglycemia", "acidosis", "alkalosis", "hypoxemia",
    "creatinine", "bilirubin", "troponin", "bnp", "lactate", "wbc", "cultures",
    # Imaging findings
    "infiltrate", "consolidation", "effusion", "cardiomegaly",
    # Diagnostics
    "ultrasound", "ct", "mri", "xray", "echo", "ekg",
    # Treatments
    "antibiotics", "diuretics", "vasopressors", "insulin", "anticoagulation",
    "oxygen", "ventilation", "dialysis", "transfusion", "surgery",
]

assert len(CONCEPTS) == 111, f"Expected 111 concepts, got {len(CONCEPTS)}"
NUM_CONCEPTS = 111

# ── 50 ICD-10 Target Codes ────────────────────────────────────────────────────
# Compact format (no dots) — matches checkpoint config['top_50_codes'] exactly.
# This order determines the diagnosis_head output index for each code.
ICD10_CODES = [
    "E785",   # Hyperlipidemia, unspecified
    "I10",    # Essential (primary) hypertension
    "Z87891", # Personal history of nicotine dependence
    "K219",   # Gastro-esophageal reflux disease without esophagitis
    "F329",   # Major depressive disorder, single episode, unspecified
    "I2510",  # Atherosclerotic heart disease of native coronary artery without angina
    "N179",   # Acute kidney failure, unspecified
    "F419",   # Anxiety disorder, unspecified
    "Z7901",  # Long-term (current) use of anticoagulants
    "Z794",   # Long-term (current) use of insulin
    "E039",   # Hypothyroidism, unspecified
    "E119",   # Type 2 diabetes mellitus without complications
    "G4733",  # Obstructive sleep apnea (adult) (pediatric)
    "D649",   # Anemia, unspecified
    "E669",   # Obesity, unspecified
    "I4891",  # Unspecified atrial fibrillation
    "F17210", # Nicotine dependence, cigarettes, uncomplicated
    "Y929",   # Unspecified place or not applicable
    "Z66",    # Do not resuscitate
    "J45909", # Unspecified asthma, uncomplicated
    "Z7902",  # Long-term (current) use of antithrombotics/antiplatelets
    "J449",   # Chronic obstructive pulmonary disease, unspecified
    "D62",    # Acute posthemorrhagic anemia
    "N390",   # Urinary tract infection, site unspecified
    "I129",   # Hypertensive chronic kidney disease with stage 1-4 CKD
    "E1122",  # Type 2 diabetes mellitus with diabetic chronic kidney disease, stage 2
    "E871",   # Hypo-osmolality and hyponatremia
    "I252",   # Old myocardial infarction
    "N189",   # Chronic kidney disease, unspecified
    "E872",   # Acidosis
    "Z8673",  # Personal history of TIA and cerebral infarction without residual deficits
    "Z955",   # Presence of coronary angioplasty implant and graft
    "Z86718", # Personal history of other venous thrombosis and embolism
    "G8929",  # Other chronic pain
    "I110",   # Hypertensive heart disease with heart failure
    "K5900",  # Constipation, unspecified
    "N400",   # Benign prostatic hyperplasia without lower urinary tract symptoms
    "N183",   # Chronic kidney disease, stage 3 (moderate)
    "I480",   # Paroxysmal atrial fibrillation
    "I130",   # Hypertensive heart and chronic kidney disease without heart failure
    "G4700",  # Insomnia, unspecified
    "D696",   # Unspecified thrombocytopenia
    "Z951",   # Presence of aortocoronary bypass graft
    "M109",   # Gout, unspecified
    "Y92239", # Operating room of unspecified hospital as place of occurrence
    "J9601",  # Acute and chronic respiratory failure with hypoxia
    "J189",   # Pneumonia, unspecified organism
    "Z23",    # Encounter for immunization
    "Y92230", # Unspecified place in hospital as place of occurrence
    "I5032",  # Chronic diastolic (congestive) heart failure
]

assert len(ICD10_CODES) == 50, f"Expected 50 codes, got {len(ICD10_CODES)}"
NUM_CODES = 50

# ── Default thresholds (overridden by optimal_thresholds.json at runtime) ─────
DEFAULT_THRESHOLD = 0.35
DEFAULT_CONCEPT_THRESHOLD = 0.50

# BERT encoder layers where concept fusion modules are inserted
CROSS_ATTENTION_LAYERS = [9, 11]

# BioClinicalBERT — used by the tokenizer loader only (model weights come from checkpoint)
BIOCLINICALBERT_MODEL = "emilyalsentzer/Bio_ClinicalBERT"
MAX_SEQ_LENGTH = 512
