"""
seed_notes.py — Load synthetic clinical note templates into Supabase `sample_notes`.

Templates align with the Phase-1 model's top ICD-10 codes (no-dot format, e.g. E785).

Usage (from `shifamind_test/`):
    python scripts/seed_notes.py

Reads `shifamind_test/.env` automatically (not your shell cwd). Requires:
    SUPABASE_URL
    SUPABASE_SERVICE_ROLE_KEY   (service_role / sb_secret — both work via REST)

Uses PostgREST + httpx (same pattern as the FastAPI backend), so newer `sb_secret_...`
keys are not blocked by older `supabase-py` JWT validation.

Dependencies: pip install httpx python-dotenv

Notes are clinically realistic but entirely synthetic (no real patient data).
"""

import os
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parent.parent

# One template per top-50 model code (expected_codes use the same strings the model emits).
SAMPLE_NOTES = [
    {
        "title": "Hyperlipidemia — routine follow-up",
        "category": "Endocrine / Metabolic",
        "expected_codes": ["E785"],
        "text": """52M here for annual physical. No chest pain or SOB. Diet heavy in fast food; exercises rarely.

Vitals: BP 128/82, HR 72, BMI 29.

Labs today: fasting lipid panel — LDL 168 mg/dL, HDL 38 mg/dL, TG 220 mg/dL, total cholesterol 248. A1c 5.6%, normal LFTs.

Assessment: Mixed hyperlipidemia, overweight.

Plan: Start atorvastatin 40 mg nightly, low saturated fat diet, repeat lipids in 8 weeks, discuss weight loss strategies.""",
    },
    {
        "title": "Essential hypertension — medication refill",
        "category": "Cardiology",
        "expected_codes": ["I10"],
        "text": """64F follow-up for blood pressure management. Reports good adherence to lisinopril 20 mg daily. Occasional headache, no vision changes, no chest pain.

Home BP log average 138/86 over 2 weeks.

Vitals today: BP 142/88, HR 76, afebrile.

Labs: BMP within normal limits, creatinine 0.9.

Assessment: Essential hypertension, suboptimally controlled.

Plan: Increase lisinopril to 40 mg daily, low sodium diet, home BP monitoring, cardiology if persistently >140/90.""",
    },
    {
        "title": "Tobacco cessation follow-up",
        "category": "Preventive / Social",
        "expected_codes": ["Z87891"],
        "text": """58M with documented 35 pack-year smoking history; quit cigarettes 14 months ago after prior nicotine dependence. Uses occasional nicotine gum when stressed.

No cough, no hemoptysis, no weight gain >10 lb.

Vitals: BP 122/78, SpO2 97% RA.

Assessment: Personal history of nicotine dependence; currently abstinent.

Plan: Reinforce quit success, continue prn nicotine replacement, offer counseling resources, annual lung cancer screening discussion.""",
    },
    {
        "title": "GERD — chronic heartburn",
        "category": "Gastroenterology",
        "expected_codes": ["K219"],
        "text": """45F with 6 months of post-prandial burning retrosternal discomfort and regurgitation, worse when lying flat, improved with antacids. No dysphagia, no melena, NSAID use minimal.

Exam: benign abdomen, no tenderness.

Assessment: Gastro-esophageal reflux disease without esophagitis documented on recent scope.

Plan: Omeprazole 20 mg daily before breakfast for 8 weeks, elevate HOB, avoid late meals, return if alarm symptoms.""",
    },
    {
        "title": "Major depression — single episode",
        "category": "Mental Health",
        "expected_codes": ["F329"],
        "text": """29F presents with 7 weeks low mood, anhedonia, early insomnia, poor concentration, and 5 lb weight loss. Denies SI/HI. Prior episode in college treated with SSRI.

PHQ-9 score 16.

MSE: depressed mood, psychomotor slowing, no psychosis.

Assessment: Major depressive disorder, single episode, moderate severity, unspecified.

Plan: Start sertraline 50 mg daily, weekly therapy referral, safety planning, follow-up 2 weeks.""",
    },
    {
        "title": "Primary hypothyroidism",
        "category": "Endocrine",
        "expected_codes": ["E039"],
        "text": """38F with fatigue, cold intolerance, dry skin, and constipation x4 months. No known thyroid disease.

Vitals: HR 58, BP 110/70, weight +8 lb from baseline.

Labs: TSH 18.4 mIU/L, free T4 0.7 ng/dL, negative TPO antibodies.

Assessment: Hypothyroidism, unspecified etiology.

Plan: Start levothyroxine 50 mcg daily on empty stomach, repeat TSH in 6 weeks, titrate to euthyroid.""",
    },
    {
        "title": "Type 2 diabetes on basal insulin",
        "category": "Endocrine",
        "expected_codes": ["Z794"],
        "text": """61M with type 2 diabetes mellitus on metformin 2000 mg daily and insulin glargine 24 units qHS. Fasting glucoses 140–190 at home. No hypoglycemia symptoms.

Vitals: BP 136/84, BMI 33.

Labs: A1c 8.2%, creatinine 1.0, eGFR >60.

Assessment: Type 2 DM; long-term (current) use of insulin.

Plan: Continue basal insulin, reinforce carb counting, consider GLP-1 discussion, ophthalmology foot exam referrals, A1c goal individualized.""",
    },
    {
        "title": "Stable CAD — prior PCI, no angina",
        "category": "Cardiology",
        "expected_codes": ["I2510"],
        "text": """69M with history of PCI to LAD 4 years ago for STEMI; on aspirin, ticagrelor, high-intensity statin, and metoprolol. No chest pain, no SOB on moderate exertion.

Vitals: BP 118/74, HR 62.

EKG: NSR, old Q-waves anterior leads, no acute ST changes.

Assessment: Atherosclerotic heart disease of native coronary artery without angina pectoris.

Plan: Continue secondary prevention, lipid panel, stress test if symptoms change, cardiology annual.""",
    },
    {
        "title": "COPD — chronic cough and dyspnea",
        "category": "Pulmonary",
        "expected_codes": ["J449"],
        "text": """67M former smoker 45 pack-years with chronic productive cough and exertional dyspnea over 3 years. Uses albuterol MDI 3–4x weekly.

Vitals: SpO2 93% RA, RR 18.

PFTs (prior): FEV1/FVC 62%, FEV1 55% predicted — obstructive pattern.

Assessment: Chronic obstructive pulmonary disease, unspecified.

Plan: Tiotropium daily + albuterol PRN, influenza and pneumococcal vaccines, pulm rehab referral, smoking cessation reinforcement.""",
    },
    {
        "title": "Generalized anxiety — primary care",
        "category": "Mental Health",
        "expected_codes": ["F419"],
        "text": """41F with 4 months excessive worry about work and family, restlessness, muscle tension, fatigue, and difficulty sleeping. Panic attacks denied.

GAD-7 score 14. No substance use.

Assessment: Anxiety disorder, unspecified type, clinically significant.

Plan: Start escitalopram 10 mg daily, CBT referral, sleep hygiene, follow-up 3 weeks for tolerability.""",
    },
    {
        "title": "Type 2 diabetes — diet controlled on oral agents",
        "category": "Endocrine",
        "expected_codes": ["E119"],
        "text": """55M type 2 diabetes diagnosed 6 years ago on metformin 1000 mg BID. Home glucoses mostly 120–160 fasting. No neuropathy complaints.

Foot exam intact monofilament.

Labs: A1c 7.0%, LDL 92, microalbumin normal.

Assessment: Type 2 diabetes mellitus without complications; not on insulin.

Plan: Continue metformin, MNT reinforcement, annual eye exam, statin per ASCVD risk.""",
    },
    {
        "title": "Atrial fibrillation on warfarin",
        "category": "Cardiology",
        "expected_codes": ["Z7901"],
        "text": """73F with permanent atrial fibrillation on warfarin for stroke prevention (CHA2DS2-VASc 4). INR today 2.4 (therapeutic). No bleeding, no falls.

Vitals: HR 78 controlled, BP 128/70.

Assessment: Long-term (current) use of anticoagulant.

Plan: Continue warfarin, INR monthly, fall precautions, avoid NSAIDs, cardiology follow-up.""",
    },
    {
        "title": "Tobacco dependence — active smoking",
        "category": "Preventive / Social",
        "expected_codes": ["F17210"],
        "text": """49M smokes 1 pack per day for 30 years; multiple prior quit attempts. Wants to try again before upcoming surgery.

CO level elevated on breath test.

Assessment: Nicotine dependence, cigarettes, uncomplicated.

Plan: Combination NRT patch + lozenge, varenicline counseling, quit date in 1 week, behavioral support referral.""",
    },
    {
        "title": "Obesity — BMI elevation",
        "category": "Endocrine / Metabolic",
        "expected_codes": ["E669"],
        "text": """36F BMI 38, weight stable over past year. Interested in weight management. No OSA symptoms yet, no DM.

Vitals: BP 132/84, HR 88.

Labs: fasting glucose 102, lipids mild elevation, LFTs normal.

Assessment: Obesity, unspecified class.

Plan: Calorie deficit diet, GLP-1 agonist trial discussed, exercise prescription, screen for comorbidities.""",
    },
    {
        "title": "Obstructive sleep apnea",
        "category": "Pulmonary / Sleep",
        "expected_codes": ["G4733"],
        "text": """52M with loud snoring, witnessed apneas, and daytime somnolence (ESS 14). Hypertension difficult to control.

Sleep study: AHI 32 events/hr, predominantly obstructive.

Assessment: Obstructive sleep apnea, adult.

Plan: CPAP titration, weight loss, avoid alcohol before bed, repeat BP monitoring on therapy.""",
    },
    {
        "title": "Unspecified anemia — fatigue",
        "category": "Hematology",
        "expected_codes": ["D649"],
        "text": """58F with progressive fatigue and pallor x2 months. Menorrhagia history. No melena.

Vitals: HR 98, BP 108/70, pale conjunctiva.

Labs: Hgb 9.2 g/dL, MCV 78 fL, ferritin 8 ng/mL, iron sat 12%.

Assessment: Anemia, unspecified — likely iron deficiency; workup ongoing.

Plan: Oral iron supplementation, GYN referral for bleeding, colonoscopy if male/postmenopausal per guidelines.""",
    },
    {
        "title": "On aspirin for secondary prevention",
        "category": "Cardiology",
        "expected_codes": ["Z7902"],
        "text": """71M s/p ischemic stroke 2 years ago on aspirin 81 mg daily for secondary prevention. No GI bleed history.

Vitals: BP 130/78.

Assessment: Long-term (current) use of antithrombotic/antiplatelet (aspirin).

Plan: Continue aspirin, GI protection if NSAIDs needed, discuss bleeding risk annually.""",
    },
    {
        "title": "Type 2 DM with diabetic kidney disease",
        "category": "Endocrine / Renal",
        "expected_codes": ["E1122"],
        "text": """63M long-standing type 2 diabetes with persistent microalbuminuria and eGFR 48 (down from 65 two years ago). On metformin and SGLT2 inhibitor.

Vitals: BP 146/88.

Labs: A1c 7.8%, UACR 180 mg/g, creatinine 1.5.

Assessment: Type 2 diabetes mellitus with diabetic chronic kidney disease.

Plan: Maximize RAAS blockade if tolerated, SGLT2 continue, nephrology co-management, strict BP and glucose goals.""",
    },
    {
        "title": "Acute blood loss anemia — GI bleed",
        "category": "Hematology / GI",
        "expected_codes": ["D62"],
        "text": """60M with melena x24h and orthostasis after NSAID use for back pain. Hemodynamically stable after 1L NS.

Vitals: HR 108, BP 98/62 supine.

Labs: Hgb 7.1 (baseline ~14), BUN/Cr ratio elevated, INR 1.1.

Assessment: Acute posthemorrhagic anemia.

Plan: Transfuse pRBC, PPI infusion, urgent EGD, hold NSAIDs, admit for observation.""",
    },
    {
        "title": "Chronic kidney disease — unspecified stage",
        "category": "Nephrology",
        "expected_codes": ["N179"],
        "text": """70F referred for elevated creatinine. History of hypertension and NSAID use. No edema.

Vitals: BP 152/88.

Labs: creatinine 2.1, eGFR 28, bland UA, renal US no hydronephrosis.

Assessment: Chronic kidney disease, unspecified stage.

Plan: Nephrology referral, avoid nephrotoxins, BP control, medication dose adjustment, CKD education.""",
    },
    {
        "title": "Atrial fibrillation — new diagnosis",
        "category": "Cardiology",
        "expected_codes": ["I4891"],
        "text": """76M presents with palpitations; found irregularly irregular rhythm on exam. EKG shows atrial fibrillation, VR 110, no acute ischemia.

TSH normal, echo pending.

CHA2DS2-VASc 4.

Assessment: Atrial fibrillation, unspecified type.

Plan: Rate control with beta blocker, anticoagulation initiation, cardiology for rhythm strategy, outpatient echo.""",
    },
    {
        "title": "Asthma — intermittent symptoms",
        "category": "Pulmonary",
        "expected_codes": ["J45909"],
        "text": """22F with seasonal wheeze and chest tightness with URI, uses albuterol 2x monthly. No prior intubations.

PFTs: mild reversible obstruction.

Assessment: Asthma, unspecified, uncomplicated.

Plan: Low-dose ICS-formoterol PRN regimen, asthma action plan, allergen avoidance, pulm follow-up if frequent use.""",
    },
    {
        "title": "DNR order on chart",
        "category": "Palliative / Ethics",
        "expected_codes": ["Z66"],
        "text": """88F with advanced dementia, nursing home resident, multiple comorbidities. Family and patient (when alert) agree on comfort-focused care.

Full code status changed to DNR/DNI after goals-of-care meeting.

Assessment: Do not resuscitate status documented.

Plan: Comfort measures, POLST signed, educate staff, symptom management for dyspnea/pain.""",
    },
    {
        "title": "Hyponatremia — SIADH suspected",
        "category": "Nephrology / Electrolytes",
        "expected_codes": ["E871"],
        "text": """65M on SSRI and thiazide with confusion and lethargy. Na 118 mEq/L on BMP, serum osmol low, urine sodium inappropriately concentrated.

Vitals: neurologically sluggish but arousable.

Assessment: Hypo-osmolality and hyponatremia.

Plan: Hold thiazide, fluid restriction, hypertonic saline per protocol, investigate and treat SIADH cause, slow correction.""",
    },
    {
        "title": "Metabolic acidosis — AKI",
        "category": "Nephrology / Electrolytes",
        "expected_codes": ["E872"],
        "text": """54M with diarrhea and poor PO intake, lethargic. Cr 3.8 from 1.1.

ABG: pH 7.25, HCO3 14, anion gap elevated.

Lactate borderline.

Assessment: Metabolic acidosis.

Plan: IV fluids, treat underlying sepsis vs dehydration, bicarbonate if severe, monitor anion gap and potassium.""",
    },
    {
        "title": "Paroxysmal atrial fibrillation",
        "category": "Cardiology",
        "expected_codes": ["I480"],
        "text": """59F episodic palpitations lasting 20–40 minutes, self-resolving. Holter shows paroxysmal AF burden 8%.

Echo: normal LV function, mild LA dilation.

Assessment: Paroxysmal atrial fibrillation.

Plan: Consider rhythm control vs rate only, stroke risk stratification, anticoagulation per CHA2DS2-VASc, cardiology EP referral.""",
    },
    {
        "title": "History of TIA — no deficits",
        "category": "Neurology",
        "expected_codes": ["Z8673"],
        "text": """72M 18 months s/p transient right arm weakness and slurred speech lasting 20 minutes; full resolution. MRI no infarct; carotids mild stenosis.

Now on aspirin and statin, BP controlled.

Assessment: Personal history of TIA without residual deficits.

Plan: Continue secondary prevention, strict vascular risk factors, return for recurrent neuro symptoms immediately.""",
    },
    {
        "title": "Urinary tract infection",
        "category": "Infectious Disease / GU",
        "expected_codes": ["N390"],
        "text": """34F dysuria, frequency, suprapubic pain x2 days, no fever. Not pregnant.

UA: positive leukocyte esterase, nitrites, many WBC.

Assessment: Urinary tract infection, site not specified.

Plan: Nitrofurantoin x5 days, increase fluids, return if fever or flank pain.""",
    },
    {
        "title": "Hypertension with CKD",
        "category": "Cardiology / Nephrology",
        "expected_codes": ["I129"],
        "text": """68M long-standing hypertension with CKD stage 3b (eGFR 38). Difficult BP control on two agents.

Vitals: BP 158/94.

Labs: creatinine 1.7, UACR elevated.

Assessment: Hypertensive chronic kidney disease with stage 1 through 4 CKD.

Plan: Add/optimize RAAS inhibitor if safe, loop diuretic prn, sodium restriction, nephrology co-care.""",
    },
    {
        "title": "Chronic pain — multi-site",
        "category": "Pain / PM&R",
        "expected_codes": ["G8929"],
        "text": """47F with chronic low back and bilateral knee pain >6 months after MVA. Functional limitation with stairs.

On NSAIDs PRN; avoids opioids.

Assessment: Other chronic pain, not elsewhere classified.

Plan: PT, topical NSAIDs, SNRI trial for neuropathic component, pain contract if opioids ever considered.""",
    },
    {
        "title": "History of pulmonary embolism",
        "category": "Cardiology / Pulmonary",
        "expected_codes": ["Z86718"],
        "text": """55M 3 years s/p PE on rivaroxaban completed 6 months; now off anticoagulation per hematology. No recurrent events.

Exercise tolerance good.

Assessment: Personal history of other circulatory disease (prior PE).

Plan: Risk factor modification, avoid estrogen, flight prophylaxis discussion, ED if SOB/chest pain.""",
    },
    {
        "title": "CKD stage 3 — lab follow-up",
        "category": "Nephrology",
        "expected_codes": ["N189"],
        "text": """59M CKD with eGFR 42, stable 1 year. HTN and DM controlled. No proteinuria on last check.

Vitals: BP 128/76.

Labs: creatinine 1.4, eGFR 42, A1c 6.8%.

Assessment: Chronic kidney disease, unspecified (stage 3 by eGFR).

Plan: Continue ACE inhibitor, avoid contrast nephropathy, monitor BMP q3–6 mo.""",
    },
    {
        "title": "Heart failure — preserved EF, diastolic",
        "category": "Cardiology",
        "expected_codes": ["I5032"],
        "text": """74F with exertional dyspnea and orthopnea, bilateral edema. Echo EF 55%, grade II diastolic dysfunction, elevated filling pressures clinically.

BNP 680.

Assessment: Chronic diastolic (congestive) heart failure.

Plan: Diuretics, tight BP control, rate/rhythm management if AF, sodium restriction, cardiology HF clinic.""",
    },
    {
        "title": "Hypertensive heart and kidney disease with HF",
        "category": "Cardiology / Nephrology",
        "expected_codes": ["I130"],
        "text": """66M with HFrEF symptoms, long-standing HTN, and CKD (eGFR 35). Crackles bilaterally, JVD +.

Echo: EF 38%, LVH.

Assessment: Hypertensive heart and chronic kidney disease with heart failure and stage 1–4 CKD.

Plan: GDMT for HFrEF, optimize RAAS pathway carefully, diuretics, cardiology/nephrology co-management.""",
    },
    {
        "title": "Hypertensive heart disease with heart failure",
        "category": "Cardiology",
        "expected_codes": ["I110"],
        "text": """71M presents with fluid overload and BP 188/102. History of LVH and prior HF admission.

Echo: EF 42%, concentric LVH, mild MR.

Assessment: Hypertensive heart disease with heart failure.

Plan: IV diuretics, afterload reduction, uptitrate GDMT, salt restriction, close outpatient follow-up.""",
    },
    {
        "title": "BPH — enlarged prostate, asymptomatic LUTS",
        "category": "Urology",
        "expected_codes": ["N400"],
        "text": """68M routine exam; DRE enlarged smooth prostate. Denies significant urinary symptoms, no nocturia >1, strong stream.

PSA 2.1.

Assessment: Benign prostatic hyperplasia without lower urinary tract symptoms.

Plan: Watchful waiting, annual PSA/DRE, return if obstructive symptoms develop.""",
    },
    {
        "title": "Acute hypoxemic respiratory failure",
        "category": "Pulmonary / Critical Care",
        "expected_codes": ["J9601"],
        "text": """63M with severe pneumonia, RR 34, SpO2 84% on NC requiring high-flow oxygen and later BiPAP.

ABG: pO2 54 on 6L, pCO2 38.

CXR: multilobar infiltrates.

Assessment: Acute respiratory failure with hypoxia.

Plan: ICU, treat sepsis, escalate oxygen/mechanical ventilation if needed, antibiotics, lung-protective strategy.""",
    },
    {
        "title": "Status post coronary angioplasty with stent",
        "category": "Cardiology",
        "expected_codes": ["Z955"],
        "text": """57M s/p drug-eluting stent to RCA 6 months ago for NSTEMI. On DAPT and high-intensity statin. No recurrent angina.

Vitals: BP 122/76.

Assessment: Presence of coronary angioplasty implant and graft.

Plan: Continue DAPT per protocol, cardiac rehab, risk factor modification, cardiology follow-up.""",
    },
    {
        "title": "Permanent pacemaker in place",
        "category": "Cardiology",
        "expected_codes": ["Z951"],
        "text": """79M with dual-chamber pacemaker for symptomatic bradycardia and intermittent heart block. Interrogation shows 15% ventricular pacing, good thresholds.

No syncope since implant.

Assessment: Presence of cardiac pacemaker.

Plan: Device check q6 months, MRI conditional precautions, monitor for HF symptoms.""",
    },
    {
        "title": "Thrombocytopenia — lab abnormality",
        "category": "Hematology",
        "expected_codes": ["D696"],
        "text": """44F incidental platelet count 85K on routine labs. No bleeding, no petechiae. Not on heparin.

Smear: no clumping.

Assessment: Thrombocytopenia, unspecified — workup for ITP vs marrow vs drug effect.

Plan: Repeat CBC, peripheral smear review, hold offending agents, hematology if persistent <100K.""",
    },
    {
        "title": "Chronic constipation",
        "category": "Gastroenterology",
        "expected_codes": ["K5900"],
        "text": """52F bowel movements every 4–5 days, hard stools, straining. No blood per rectum, weight stable.

Exam: benign abdomen.

Assessment: Constipation, unspecified.

Plan: Increase fiber and fluids, polyethylene glycol trial, TSH if refractory, colonoscopy per age guidelines.""",
    },
    {
        "title": "Type 2 DM — severe hyperglycemia",
        "category": "Endocrine",
        "expected_codes": ["E1165"],
        "text": """56M with polydipsia, polyuria, blurred vision. Random glucose 412, A1c 11.4%. Ketones negative.

Vitals: BP 138/88.

Assessment: Type 2 diabetes mellitus with hyperglycemia.

Plan: Start basal-bolus or basal plus correction, MNT, education, follow-up in 1 week, screen for complications.""",
    },
    {
        "title": "Acute gout flare — great toe",
        "category": "Rheumatology",
        "expected_codes": ["M109"],
        "text": """48M sudden onset red hot swollen first MTP joint after weekend of alcohol and shellfish. Fever 38.2°C.

Synovial fluid: negatively birefringent crystals.

Assessment: Gout, unspecified (acute flare).

Plan: NSAIDs or colchicine, rest, hydration, allopurinol after flare resolves, lifestyle counseling.""",
    },
    {
        "title": "Iron deficiency anemia",
        "category": "Hematology",
        "expected_codes": ["D509"],
        "text": """35F vegan diet with fatigue. Hgb 10.1, MCV 72, ferritin 6, low iron sat.

No GI symptoms.

Assessment: Iron deficiency anemia, unspecified.

Plan: Oral ferrous sulfate, dietary counseling, evaluate menorrhagia vs malabsorption if no response.""",
    },
    {
        "title": "Chronic insomnia",
        "category": "Sleep / Mental Health",
        "expected_codes": ["G4700"],
        "text": """40F difficulty initiating sleep 3–4 nights weekly for 6 months; ruminates about work. No sleep apnea symptoms.

Sleep diary: prolonged sleep latency.

Assessment: Insomnia, unspecified.

Plan: CBT-I first-line, sleep hygiene, consider low-dose melatonin or short-term hypnotic bridge, screen for depression.""",
    },
    {
        "title": "Palliative care visit",
        "category": "Palliative Care",
        "expected_codes": ["Z515"],
        "text": """82F with metastatic cancer, declining functional status, family requests symptom focus. Discussed prognosis, medications for pain and dyspnea, home hospice eligibility.

Assessment: Encounter for palliative care.

Plan: Palliative care follow-up weekly, advance care planning, medication simplification, psychosocial support.""",
    },
    {
        "title": "Old myocardial infarction — remote",
        "category": "Cardiology",
        "expected_codes": ["I252"],
        "text": """75M remote inferior MI 12 years ago on medical management. Q-waves II, III, aVF on EKG. Currently asymptomatic for angina.

Stress test last year negative for ischemia.

Assessment: Old myocardial infarction.

Plan: Continue statin, aspirin, BP control, annual cardiology, ED for typical angina.""",
    },
    {
        "title": "Hypokalemia — diuretic related",
        "category": "Electrolytes",
        "expected_codes": ["E876"],
        "text": """68F on HCTZ for BP with weakness and cramps. K+ 2.9, Mg low-normal.

EKG: U-waves present.

Assessment: Hypokalemia.

Plan: Oral/potassium repletion, hold thiazide temporarily, switch to K-sparing agent if appropriate, recheck BMP.""",
    },
    {
        "title": "Hyperkalemia — renal dysfunction",
        "category": "Electrolytes / Nephrology",
        "expected_codes": ["E875"],
        "text": """72M CKD stage 4 on lisinopril and spironolactone presents with fatigue. K+ 6.2.

EKG: peaked T-waves.

Assessment: Hyperkalemia.

Plan: Calcium stabilizer, insulin/dextrose, albuterol, kayexalate, stop RAAS drugs temporarily, emergent dialysis if refractory.""",
    },
    {
        "title": "Leukocytosis — infection workup",
        "category": "Hematology / ID",
        "expected_codes": ["D72829"],
        "text": """39M fever and productive cough x3 days. WBC 18.2 with left shift.

CXR: right lower lobe infiltrate.

Assessment: Elevated white blood cell count, unspecified — reactive to infection.

Plan: Antibiotics for CAP, repeat CBC with differential outpatient, further workup if persistent leukocytosis without source.""",
    },
]


def main():
    load_dotenv(_REPO_ROOT / ".env")

    base = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not base or not key:
        print(
            "Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set.\n"
            f"  Expected .env at: {_REPO_ROOT / '.env'}\n"
            "  Fix any dotenv parse errors (no shell commands in .env; quote values that contain !).",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        import httpx
    except ImportError:
        print("Error: httpx not installed. Run: pip install httpx", file=sys.stderr)
        sys.exit(1)

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    insert_headers = {**headers, "Prefer": "return=minimal"}

    created, skipped, failed = 0, 0, 0
    with httpx.Client(timeout=60.0) as client:
        for note in SAMPLE_NOTES:
            print(f"  Inserting: {note['title'][:55]}...", end=" ", flush=True)
            try:
                r = client.get(
                    f"{base}/rest/v1/sample_notes",
                    params={"title": f"eq.{note['title']}", "select": "id"},
                    headers=headers,
                )
                if r.status_code != 200:
                    print(f"FAILED — list {r.status_code}: {r.text[:200]}")
                    failed += 1
                    continue
                if r.json():
                    print("SKIPPED (exists)")
                    skipped += 1
                    continue

                r = client.post(
                    f"{base}/rest/v1/sample_notes",
                    headers=insert_headers,
                    json={
                        "id": str(uuid.uuid4()),
                        "title": note["title"],
                        "category": note["category"],
                        "text": note["text"].strip(),
                        "expected_codes": note["expected_codes"],
                        "is_active": True,
                    },
                )
                if r.status_code not in (200, 201):
                    print(f"FAILED — insert {r.status_code}: {r.text[:300]}")
                    failed += 1
                    continue
                print("OK")
                created += 1
            except Exception as e:
                print(f"FAILED — {e}")
                failed += 1

    print(f"\nDone: {created} inserted, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
