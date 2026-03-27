"""
ShifaMind Phase 1 — model configuration.
111 clinical concepts, 50 ICD-10 target codes.
"""

# ── 111 Clinical Concepts ─────────────────────────────────────────────────────
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
ICD10_CODES = [
    "I50.9",   # Heart failure, unspecified
    "I50.32",  # Chronic diastolic heart failure
    "I50.22",  # Chronic systolic heart failure
    "I21.9",   # Acute myocardial infarction, unspecified
    "I48.91",  # Unspecified atrial fibrillation
    "I10",     # Essential hypertension
    "I63.9",   # Cerebral infarction, unspecified
    "I26.99",  # Other pulmonary embolism
    "J18.9",   # Pneumonia, unspecified
    "J44.1",   # COPD with acute exacerbation
    "J96.00",  # Acute respiratory failure, unspecified
    "J15.9",   # Unspecified bacterial pneumonia
    "N17.9",   # Acute kidney failure, unspecified
    "N18.6",   # End-stage renal disease
    "E11.9",   # Type 2 diabetes, without complications
    "E11.65",  # Type 2 diabetes with hyperglycemia
    "E10.10",  # Type 1 diabetes with ketoacidosis
    "E87.1",   # Hypo-osmolality and hyponatremia
    "E87.5",   # Hyperkalemia
    "A41.9",   # Sepsis, unspecified
    "A41.51",  # Sepsis due to Escherichia coli
    "B37.3",   # Candidiasis of vulva and vagina (UTI-related)
    "N39.0",   # Urinary tract infection, site unspecified
    "K92.1",   # Melena
    "K92.0",   # Hematemesis
    "K57.30",  # Diverticulosis of large intestine, unspecified
    "K74.60",  # Unspecified cirrhosis of liver
    "K70.30",  # Alcoholic cirrhosis of liver
    "K85.9",   # Acute pancreatitis, unspecified
    "G35",     # Multiple sclerosis
    "G43.909", # Migraine, unspecified
    "G20",     # Parkinson's disease
    "G45.9",   # Transient cerebral ischemic attack, unspecified
    "C34.90",  # Malignant neoplasm of bronchus and lung, unspecified
    "C18.9",   # Malignant neoplasm of colon, unspecified
    "C80.1",   # Malignant neoplasm without specification of site
    "D64.9",   # Anemia, unspecified
    "D69.6",   # Thrombocytopenia, unspecified
    "M54.5",   # Low back pain
    "M79.3",   # Panniculitis, unspecified
    "F10.20",  # Alcohol use disorder, moderate, uncomplicated
    "F32.9",   # Major depressive disorder, single episode, unspecified
    "Z87.891", # Personal history of other specified conditions
    "T81.10",  # Postprocedural shock, unspecified
    "R65.20",  # Severe sepsis without septic shock
    "R65.21",  # Severe sepsis with septic shock
    "R00.1",   # Bradycardia, unspecified
    "R00.0",   # Tachycardia, unspecified
    "R06.00",  # Dyspnea, unspecified
    "R55",     # Syncope and collapse
]

assert len(ICD10_CODES) == 50, f"Expected 50 codes, got {len(ICD10_CODES)}"
NUM_CODES = 50

# ── Default thresholds (overridden by optimal_thresholds.json at runtime) ─────
DEFAULT_THRESHOLD = 0.35
DEFAULT_CONCEPT_THRESHOLD = 0.50

# Concept indices for cross-attention layers (9 and 11)
CROSS_ATTENTION_LAYERS = [9, 11]

# BioClinicalBERT model name
BIOCLINICALBERT_MODEL = "emilyalsentzer/Bio_ClinicalBERT"
MAX_SEQ_LENGTH = 512
