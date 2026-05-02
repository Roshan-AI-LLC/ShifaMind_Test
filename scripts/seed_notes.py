"""
seed_notes.py — Wipe and reload synthetic clinical note templates into Supabase `sample_notes`.

Each note is a full inpatient discharge summary targeting 3000+ estimated tokens to match
the model's training distribution. Templates align with the Phase-1 model's top ICD-10 codes.

Usage (from repo root):
    python scripts/seed_notes.py

Reads .env automatically. Requires:
    SUPABASE_URL
    SUPABASE_SERVICE_ROLE_KEY

Dependencies: pip install httpx python-dotenv
Notes are clinically realistic but entirely synthetic (no real patient data).
"""

import os
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parent.parent

SAMPLE_NOTES = [
    {
        "title": "Acute Decompensated Heart Failure — HFpEF",
        "category": "Cardiology",
        "expected_codes": ["I5032"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Margaret Hollis, 74F | MRN: 4821093
Admission: 09/14/2025 | Discharge: 09/19/2025 | LOS: 5 days
Attending: Dr. A. Ramirez, MD | Service: Cardiology

CHIEF COMPLAINT
Progressive shortness of breath and bilateral leg swelling over five days.

HISTORY OF PRESENT ILLNESS
Ms. Hollis is a 74-year-old woman with known heart failure with preserved ejection fraction (HFpEF), hypertension, type 2 diabetes mellitus, and obesity who presents with a five-day history of worsening dyspnea on exertion, orthopnea requiring three pillows at night, and bilateral ankle and pretibial pitting edema. She reports a weight gain of approximately eight pounds over the preceding week and endorses markedly decreased functional capacity — she is now short of breath walking from the bedroom to the bathroom, whereas her baseline is walking two to three blocks without difficulty.

On further questioning, she admits to dietary indiscretion over the past two weeks, including increased sodium intake at a family celebration and a backyard gathering. She ran out of furosemide approximately ten days ago and did not refill it due to transportation barriers. She has been adherent to her other medications. She denies chest pain, pressure, radiation to the arm or jaw, diaphoresis, palpitations, syncope, fever, chills, or productive cough. She has no history of pulmonary embolism or deep vein thrombosis, no recent prolonged immobility, and no lower extremity trauma. She denies recent viral illness.

Her most recent echocardiogram, performed nine months prior at her cardiologist's office, demonstrated an LVEF of 56% with grade II diastolic dysfunction, mild left atrial enlargement, elevated estimated filling pressures, and an E/e' ratio of 15. She was considered compensated at that visit. Her last hospitalization for decompensated heart failure was eighteen months ago, when she responded well to IV diuresis and was discharged after four days on an optimized oral regimen with close outpatient follow-up.

In the emergency department she was found in moderate respiratory distress. Vital signs were notable for blood pressure 174/100 mmHg, heart rate 98 bpm in sinus rhythm, respiratory rate 22 breaths per minute, temperature 37.0°C, and oxygen saturation 87% on room air improving to 94% on 4L nasal cannula. She was placed in an upright position and given IV furosemide 80 mg with moderate early response. BNP on arrival was 1,964 pg/mL. Chest radiograph demonstrated bilateral pleural effusions, pulmonary vascular congestion, and cardiomegaly. She was admitted to the cardiology step-down unit for IV diuresis and optimization of her heart failure regimen.

PAST MEDICAL HISTORY
1. Heart failure with preserved ejection fraction (HFpEF), diagnosed four years ago
2. Essential hypertension, 12-year history
3. Type 2 diabetes mellitus, managed with metformin
4. Obesity (BMI 34)
5. Obstructive sleep apnea on CPAP
6. Hyperlipidemia on atorvastatin
7. Hypothyroidism, stable on levothyroxine
8. Osteoarthritis of bilateral knees

PAST SURGICAL HISTORY
Right total knee arthroplasty six years ago. Appendectomy in young adulthood. Cesarean sections x2 (remote).

MEDICATIONS ON ADMISSION
1. Metoprolol succinate 50 mg orally daily
2. Lisinopril 20 mg orally daily
3. Furosemide 40 mg orally daily — not taking for ten days
4. Potassium chloride 20 mEq orally daily
5. Atorvastatin 40 mg orally nightly
6. Metformin 500 mg orally twice daily
7. Levothyroxine 75 mcg orally daily on empty stomach
8. Aspirin 81 mg orally daily

ALLERGIES
Sulfonamides (rash). Codeine (nausea and vomiting).

SOCIAL HISTORY
Retired schoolteacher. Widowed, lives alone in a single-story home. Two adult daughters nearby and involved in her care. Former smoker, 15 pack-year history, quit 20 years ago. No alcohol or illicit drug use. Independent in ADLs at baseline but functional decline noted over the past year. Medicare Part D coverage. Pharmacy access is limited — transportation a recurring barrier.

FAMILY HISTORY
Father died of myocardial infarction at age 68. Mother had hypertension and ischemic stroke. One sibling with atrial fibrillation.

REVIEW OF SYSTEMS
Positive: dyspnea on exertion, orthopnea (three-pillow), paroxysmal nocturnal dyspnea, bilateral lower extremity edema, weight gain 8 lbs over 7 days, fatigue, reduced appetite.
Negative: chest pain, palpitations, syncope, hemoptysis, productive cough, fever, chills, abdominal pain, nausea, vomiting, diarrhea, dysuria, focal neurological symptoms.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 37.0°C, BP 174/100 mmHg (right arm), HR 98 bpm regular, RR 22 breaths/min, SpO2 87% RA → 94% on 4L NC, Wt 94.6 kg (estimated dry weight 86 kg)
General: Obese older woman in moderate respiratory distress, tachypneic, speaking in short sentences, sitting upright and leaning forward. Alert and oriented x3.
HEENT: Jugular venous distension estimated at 13 cm at 45 degrees. Mild facial puffiness. No lymphadenopathy.
Cardiovascular: Regular rate and rhythm. S1 and S2 present. S4 gallop appreciated at the apex. No S3. 2/6 holosystolic murmur at the apex with radiation to the axilla consistent with mitral regurgitation. PMI laterally displaced.
Pulmonary: Dullness to percussion at bilateral lung bases extending to mid-scapular line. Fine inspiratory crackles bilaterally from bases to mid-lung fields. Mild decreased air entry at the bases. No wheeze.
Abdomen: Soft, mildly distended. Mild hepatomegaly, liver edge palpable 3 cm below right costal margin. No ascites on exam. Non-tender.
Extremities: 3+ pitting edema bilateral lower extremities extending to mid-thigh. Skin warm and intact. No ulceration. Peripheral pulses 2+.
Neurological: Alert and oriented to person, place, date. Cranial nerves II–XII grossly intact. Motor strength 5/5 all extremities. Sensation intact. No focal deficits.

LABORATORY DATA
Admission BMP: Na 138 mEq/L, K 4.2 mEq/L, Cl 100 mEq/L, HCO3 24 mEq/L, BUN 30 mg/dL, Creatinine 1.5 mg/dL (baseline 1.1), Glucose 174 mg/dL
CBC: WBC 9.2 K/uL, Hemoglobin 11.4 g/dL, Hematocrit 34.5%, Platelets 204 K/uL
BNP: 1,964 pg/mL (markedly elevated)
Troponin I: 0.06 ng/mL — mildly elevated; serial troponin 6h: 0.05 ng/mL — stable, non-rising, no acute ACS pattern
LFTs: AST 42, ALT 36, Alkaline phosphatase 118, Total bilirubin 1.4 — mild elevation consistent with hepatic congestion
HbA1c: 7.4%
TSH: 2.6 mIU/L — within normal limits
Lipid panel: Total cholesterol 192, LDL 98, HDL 42, Triglycerides 168
Urinalysis: Specific gravity 1.024, trace protein, no nitrites, no leukocyte esterase, 0–2 RBC/hpf
Magnesium: 1.8 mg/dL
Phosphorus: 3.4 mg/dL

Hospital Day 3 BMP: Na 139, K 3.8, BUN 22, Cr 1.2, glucose 148 — improving renal function with diuresis
Discharge BMP: Na 140, K 4.0, BUN 18, Cr 1.1, glucose 142 — at baseline

IMAGING AND DIAGNOSTICS
Chest X-Ray (Admission): Cardiomegaly with cardiothoracic ratio 0.60. Bilateral pleural effusions, right greater than left. Pulmonary vascular congestion with cephalization of flow and Kerley B lines at the right costophrenic angle. No lobar consolidation. No pneumothorax.
Chest X-Ray (Hospital Day 3): Interval decrease in pulmonary vascular congestion. Bilateral pleural effusions reduced in size. No new infiltrate.
Chest X-Ray (Day 5, Pre-Discharge): Near complete resolution of pulmonary edema. Small residual right pleural effusion. Persistent cardiomegaly. No acute cardiopulmonary process.
12-Lead ECG (Admission): Normal sinus rhythm at 98 bpm. Left axis deviation. Left ventricular hypertrophy by voltage criteria (Sokolow-Lyon positive). QTc 440 ms. No acute ST-T wave changes. No Q-waves to suggest prior infarction. No delta waves.
Echocardiogram (Hospital Day 2): LVEF 55%, preserved. Concentric left ventricular hypertrophy. Grade II diastolic dysfunction. E/e' ratio 17, indicating elevated left ventricular filling pressure. Left atrial volume index 40 mL/m² (mildly enlarged). Mild mitral regurgitation. Mild tricuspid regurgitation. Estimated RVSP 44 mmHg, mildly elevated. IVC 2.2 cm with reduced respiratory variation (<50%), consistent with elevated right atrial pressure. No pericardial effusion. No wall motion abnormality to suggest ischemia.

HOSPITAL COURSE
Ms. Hollis was admitted to the cardiology step-down unit and placed on telemetry, daily weights, strict intake and output monitoring, and a 2-gram sodium, 1.5-liter fluid-restricted diet. IV furosemide was initiated at 80 mg twice daily with a target net negative fluid balance of 1.0–1.5 liters per 24 hours. Over the first 24 hours she diuresed 2.9 liters with net negative balance of 2.2 liters. Her dyspnea improved substantially by the morning of hospital day 2. She was weaned off supplemental oxygen by day 2 and ambulated to the hallway without significant breathlessness.

Electrolytes were monitored every 12 hours during active IV diuresis. Potassium trended to 3.6 mEq/L on hospital day 2 and oral potassium chloride was increased to 40 mEq twice daily until stable above 4.0. Magnesium was repleted with IV magnesium sulfate 2g on hospital day 1. Renal function initially worsened slightly (Cr peak 1.6 on day 1) but improved with ongoing diuresis and was at her estimated baseline of 1.1 by discharge, suggesting the initial creatinine rise was consistent with cardiorenal syndrome in the setting of low cardiac output rather than intrinsic injury.

Serial troponins were measured and remained stable without a rising pattern, and the echocardiogram showed no wall motion abnormalities. Acute coronary syndrome was effectively excluded. The mild troponin elevation was attributed to demand-related myocardial stress from elevated filling pressures.

Blood pressure remained poorly controlled through hospital day 2 (range 162–178/88–104). Amlodipine 5 mg daily was added on day 2 for additional afterload reduction. Lisinopril was uptitrated from 20 mg to 40 mg daily on day 3 when renal function was improving. By day 4, blood pressure was consistently 130–142/76–88 mmHg. She was transitioned from IV to oral furosemide 80 mg twice daily on day 4, with continued response and weight decreasing to 87.8 kg by discharge day.

Physical therapy evaluated the patient on hospital day 3. She was ambulating independently in the hallway on room air without supplemental oxygen. Occupational therapy confirmed she was safe for discharge to home. Social work arranged for medication delivery services, pharmacy coordination, and enrollment in a daily telephone check-in program for two weeks post-discharge. Comprehensive heart failure education was provided to the patient and her daughter, covering daily weights, sodium restriction, fluid limits, medication adherence, and a written action plan with specific thresholds for calling the clinic or presenting to the emergency department.

She is discharged home in stable, improved condition on hospital day 5 with close cardiology follow-up in one week.

DISCHARGE DIAGNOSES
1. Acute decompensated chronic diastolic (congestive) heart failure with preserved ejection fraction — primary admission diagnosis
2. Essential hypertension, suboptimally controlled — contributing comorbidity
3. Type 2 diabetes mellitus without complications, managed with metformin — active comorbidity
4. Obesity, BMI 34 — active comorbidity
5. Obstructive sleep apnea on CPAP — active comorbidity
6. Hyperlipidemia — active comorbidity
7. Hypothyroidism, stable on levothyroxine — active comorbidity
8. Medication non-adherence (furosemide lapse x10 days) — precipitating factor
9. Dietary sodium excess — precipitating factor

DISCHARGE CONDITION
Stable. Ambulatory on room air without supplemental oxygen. Dyspnea resolved at rest, minimal with exertion. Bilateral lower extremity edema reduced from 3+ to trace. Weight decreased 6.8 kg from admission. Tolerating oral diet and medications.

DISCHARGE MEDICATIONS
1. Furosemide 80 mg orally twice daily — INCREASED from 40 mg daily; do not stop without physician guidance
2. Potassium chloride 40 mEq orally daily — increased dose
3. Lisinopril 40 mg orally daily — increased from 20 mg
4. Amlodipine 5 mg orally daily — NEW medication for blood pressure
5. Metoprolol succinate 50 mg orally daily — unchanged
6. Atorvastatin 40 mg orally nightly — unchanged
7. Aspirin 81 mg orally daily — unchanged
8. Metformin 500 mg orally twice daily — hold if contrast procedure planned
9. Levothyroxine 75 mcg orally daily on empty stomach — unchanged

DISCHARGE INSTRUCTIONS
You were admitted because your heart failure was not well controlled, partly due to running out of your water pill (furosemide). Your heart squeezes normally but is stiff, causing fluid to back up into your lungs and legs. Weigh yourself every morning before eating and after using the restroom — write it down every day. If you gain more than 2 pounds in one day or 5 pounds in one week, call your cardiologist immediately. If you develop severe shortness of breath that does not improve sitting up, call 911. Limit sodium (salt) to 2 grams per day. Avoid canned soups, processed meats, restaurant meals, fast food, and table salt. Limit total fluid intake to 6 cups (1.5 liters) daily including water, coffee, juice, and soup. Take all medications every day as prescribed. Continue wearing your CPAP every night.

FOLLOW-UP
1. Cardiology (Dr. Ramirez): 7 days post-discharge — weight check, electrolytes, diuretic adjustment
2. Primary Care: 2 weeks post-discharge
3. Home Health Physical Therapy: Arranged, begins within 48 hours of discharge
4. Pharmacy: Medication synchronization and home delivery arranged""",
    },
    {
        "title": "Atrial Fibrillation with Rapid Ventricular Response — New Diagnosis",
        "category": "Cardiology",
        "expected_codes": ["I4891"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Robert Tan, 72M | MRN: 3047821
Admission: 10/03/2025 | Discharge: 10/06/2025 | LOS: 3 days
Attending: Dr. S. Patel, MD | Service: Cardiology

CHIEF COMPLAINT
Palpitations and lightheadedness for eight hours, found to have irregular heart rhythm in the emergency department.

HISTORY OF PRESENT ILLNESS
Mr. Tan is a 72-year-old man with a history of essential hypertension, hyperlipidemia, and type 2 diabetes mellitus who presents with an eight-hour history of palpitations, mild lightheadedness, and decreased exercise tolerance. He describes the sensation as a rapid fluttering in his chest that began while he was sitting quietly at home watching television. He denies chest pain, shortness of breath at rest, presyncope, or syncope. He has no prior history of arrhythmia and has never been told he had an irregular heartbeat. He denies palpitations in the past.

He reports two weeks of mild fatigue and reduced tolerance to his usual two-mile morning walks, attributing this to seasonal allergies and poor sleep. In retrospect, he now believes the fatigue may have been an early symptom of his arrhythmia. He denies fever, chills, recent illness, excessive caffeine or alcohol intake, new medications, or illicit drug use. He has not started any new over-the-counter supplements. His wife noted that his pulse felt irregular when she checked it at home and encouraged him to come to the emergency department.

In the emergency department, his blood pressure was 148/92 mmHg and his initial ECG demonstrated atrial fibrillation with rapid ventricular response at a rate of 138 bpm. He was hemodynamically stable without signs of acute decompensation. He was given IV metoprolol 5 mg x2 doses over 30 minutes with rate reduction to 96 bpm. Troponin was negative x2. BNP was mildly elevated at 310 pg/mL. TSH was normal. He was admitted to the telemetry unit for rate control, anticoagulation initiation, and further evaluation.

PAST MEDICAL HISTORY
1. Essential hypertension, 10-year history, well-controlled on lisinopril
2. Hyperlipidemia on rosuvastatin
3. Type 2 diabetes mellitus, managed with metformin and sitagliptin
4. Benign prostatic hyperplasia on tamsulosin
5. Osteoarthritis of the right hip, managed with acetaminophen
6. Prediabetes first noted 15 years ago, progressed to T2DM 8 years ago

PAST SURGICAL HISTORY
Right hip arthroplasty four years ago. Cholecystectomy age 58.

MEDICATIONS ON ADMISSION
1. Lisinopril 20 mg orally daily
2. Rosuvastatin 20 mg orally nightly
3. Metformin 1000 mg orally twice daily
4. Sitagliptin 100 mg orally daily
5. Tamsulosin 0.4 mg orally nightly
6. Acetaminophen 500 mg orally as needed for pain
7. Aspirin 81 mg orally daily (self-initiated for cardiovascular prevention)

ALLERGIES
Penicillin (angioedema). No other known drug allergies.

SOCIAL HISTORY
Retired civil engineer. Married, lives with his wife in a two-story home. Two adult children locally. Nonsmoker. Occasional alcohol — one to two glasses of wine on weekends, denied binge drinking. No illicit drugs. Exercises regularly with morning walks 2 miles daily. Diet is generally balanced; moderate sodium intake.

FAMILY HISTORY
Father had atrial fibrillation diagnosed in his late 70s, died of stroke at age 81. Mother had hypertension and coronary artery disease. One sibling with type 2 diabetes.

REVIEW OF SYSTEMS
Positive: palpitations, mild lightheadedness, fatigue for two weeks, mildly reduced exercise tolerance.
Negative: chest pain, shortness of breath, orthopnea, paroxysmal nocturnal dyspnea, lower extremity edema, syncope, near-syncope, fever, chills, cough, hemoptysis, dysuria, focal neurological symptoms, visual changes, arm or jaw discomfort, diaphoresis.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 36.9°C, BP 148/92 mmHg, HR 138 bpm irregularly irregular, RR 16 breaths/min, SpO2 98% RA, Wt 84 kg
General: Well-appearing man in no acute distress. Alert and oriented x3. Mild anxious affect.
HEENT: No jugular venous distension. No thyromegaly or thyroid nodule palpated. No lymphadenopathy.
Cardiovascular: Irregularly irregular rhythm, rate approximately 138. No murmurs, rubs, or gallops appreciated. PMI non-displaced. Peripheral pulses present and irregular bilaterally.
Pulmonary: Clear to auscultation bilaterally. No wheeze, rhonchi, or crackles. Respiratory effort unlabored.
Abdomen: Soft, non-tender, non-distended. No hepatosplenomegaly. Normoactive bowel sounds.
Extremities: No lower extremity edema. No calf tenderness. Skin warm and dry. Peripheral pulses 2+ bilaterally.
Neurological: Alert and oriented. Speech fluent. Cranial nerves II–XII intact. Motor 5/5 all extremities. No focal neurological deficits. Gait not tested in the ED setting.

LABORATORY DATA
CBC: WBC 8.4 K/uL, Hemoglobin 13.8 g/dL, Hematocrit 41.2%, Platelets 228 K/uL — normal
BMP: Na 140 mEq/L, K 4.0 mEq/L, Cl 104 mEq/L, HCO3 25 mEq/L, BUN 18 mg/dL, Creatinine 1.0 mg/dL, Glucose 138 mg/dL
Troponin I (x2, 6h apart): <0.02 and <0.02 — negative
BNP: 310 pg/mL — mildly elevated, likely rate-related
TSH: 1.8 mIU/L — normal, hyperthyroidism excluded
HbA1c: 7.1%
INR: 1.0 (baseline, not on anticoagulation)
Lipid panel: Total cholesterol 178, LDL 88, HDL 48, TG 142
Magnesium: 2.0 mg/dL
Coagulation: PT/INR 1.0, aPTT 28 seconds — normal

IMAGING AND DIAGNOSTICS
12-Lead ECG (Admission, ED): Atrial fibrillation with rapid ventricular response at 138 bpm. No P waves. Irregularly irregular narrow complex rhythm. No delta waves. No ST-segment elevation. T-wave inversions in V1–V2 — likely rate-related, resolved on repeat ECG after rate control. QTc 430 ms.
12-Lead ECG (Hospital Day 2, after rate control): Atrial fibrillation with ventricular rate controlled at 74 bpm. Rate-related T-wave changes resolved. No ST-T wave abnormality. QTc 432 ms. No Q-waves.
Chest X-Ray (Admission): Mild cardiomegaly. No pulmonary edema. No pleural effusions. No pneumothorax. No acute pulmonary process.
Transthoracic Echocardiogram (Hospital Day 1): Left ventricular ejection fraction 52%, low-normal, mildly reduced compared to an estimated prior normal. Mild left atrial enlargement (LA diameter 4.2 cm, LA volume index 32 mL/m²). No intracardiac thrombus identified — though note that transthoracic echo has limited sensitivity for left atrial appendage thrombus. No significant valvular disease. No pericardial effusion. Mildly impaired relaxation (Grade I diastolic dysfunction). No wall motion abnormality.

HOSPITAL COURSE
Mr. Tan was admitted to the telemetry unit for rate control, anticoagulation initiation, and cardiac monitoring. He remained hemodynamically stable throughout his hospital stay. On hospital day 1 he was transitioned to oral metoprolol tartrate 25 mg three times daily with good rate control, with heart rate maintained between 68 and 82 bpm. His lightheadedness resolved by hospital day 1 afternoon.

The cardiology team reviewed his case and determined his CHA₂DS₂-VASc score to be 4 points (age ≥75: 1 point, hypertension: 1 point, diabetes: 1 point, male sex: 0 additional points beyond age category, vascular disease given atherosclerotic risk: 1 point). Given this score and the absence of high bleeding risk factors, anticoagulation was initiated with apixaban 5 mg twice daily after shared decision-making discussion with the patient and his wife. The risks of stroke without anticoagulation and the risks of major bleeding on anticoagulation were reviewed in detail. The patient elected to proceed with anticoagulation and understood the need for indefinite therapy.

Transthoracic echocardiogram on hospital day 1 showed a mildly reduced LVEF of 52% with mild left atrial enlargement. This was discussed with the patient as likely tachycardia-induced cardiomyopathy (rate-related) expected to improve with sustained rate control. A repeat echocardiogram was arranged for six to eight weeks after discharge to reassess ejection fraction.

The electrophysiology team was consulted and agreed with rate control as the initial strategy given the patient's age, symptom burden, and preference to avoid cardioversion at this time. A discussion of long-term rhythm vs. rate control strategy was deferred to outpatient follow-up once the patient had time to review the information. He was counseled that cardioversion may still be appropriate in the future and that his options would be revisited at the follow-up appointment.

Aspirin was continued for now given his cardiovascular risk, with a plan to reassess whether antiplatelet therapy adds benefit over anticoagulation alone at the outpatient cardiology visit. He was educated regarding AFib triggers including excess caffeine, alcohol, sleep deprivation, and dehydration. He was discharged on hospital day 3 in stable condition with controlled ventricular rate and no neurological symptoms.

DISCHARGE DIAGNOSES
1. Atrial fibrillation, unspecified type — new diagnosis, primary admission diagnosis
2. Atrial fibrillation with initial rapid ventricular response, rate-controlled prior to discharge
3. Essential hypertension — active comorbidity, contributing to AF substrate
4. Type 2 diabetes mellitus — active comorbidity
5. Hyperlipidemia — active comorbidity
6. Benign prostatic hyperplasia — active comorbidity
7. Mildly reduced left ventricular ejection fraction (52%), likely tachycardia-induced — to be reassessed outpatient

DISCHARGE CONDITION
Stable. Heart rate 72–78 bpm on telemetry. No palpitations at rest. No lightheadedness. Ambulatory without assistance. Tolerating oral diet and medications. No anticoagulation-related bleeding complications during admission.

DISCHARGE MEDICATIONS
1. Apixaban (Eliquis) 5 mg orally twice daily — NEW; take with or without food; do not stop without physician guidance; bleeding precautions reviewed
2. Metoprolol succinate 50 mg orally twice daily — NEW for rate control (changed from tartrate to succinate at discharge)
3. Lisinopril 20 mg orally daily — unchanged
4. Rosuvastatin 20 mg orally nightly — unchanged
5. Metformin 1000 mg orally twice daily — unchanged
6. Sitagliptin 100 mg orally daily — unchanged
7. Tamsulosin 0.4 mg orally nightly — unchanged
8. Acetaminophen 500 mg orally as needed for pain — unchanged

DISCHARGE INSTRUCTIONS
You were diagnosed with atrial fibrillation (AFib) — an irregular heart rhythm where the upper chambers of your heart beat chaotically. This increases your risk of blood clots and stroke, which is why you are now taking a blood thinner (apixaban). Do not stop apixaban without calling your doctor first. If you experience unusual bleeding — blood in your urine or stool, vomiting blood, or bleeding that will not stop — go to the emergency department. Take your metoprolol twice daily to keep your heart rate controlled. Limit alcohol to one drink or fewer per day. Reduce caffeine. If palpitations return or worsen, call your cardiologist. If you develop sudden weakness on one side, facial drooping, slurred speech, or vision loss, call 911 immediately — these are signs of stroke.

FOLLOW-UP
1. Cardiology Electrophysiology Clinic: 4 weeks post-discharge — rhythm vs. rate control discussion, cardioversion consideration
2. Repeat Echocardiogram: 6–8 weeks post-discharge — reassess LVEF
3. Primary Care: 2 weeks post-discharge — blood pressure, diabetes, medication reconciliation
4. INR monitoring: Not required (apixaban does not require routine INR monitoring)""",
    },
    {
        "title": "COPD Exacerbation — Acute on Chronic",
        "category": "Pulmonary",
        "expected_codes": ["J449"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Donald Briggs, 68M | MRN: 6193047
Admission: 11/08/2025 | Discharge: 11/13/2025 | LOS: 5 days
Attending: Dr. K. Osei, MD | Service: Pulmonary Medicine

CHIEF COMPLAINT
Worsening shortness of breath, increased sputum production, and change in sputum color over four days.

HISTORY OF PRESENT ILLNESS
Mr. Briggs is a 68-year-old man with a significant smoking history and established chronic obstructive pulmonary disease (COPD), GOLD Stage III (severe), who presents with a four-day history of worsening dyspnea, increased frequency and volume of sputum production, and a change in sputum from his usual white to yellow-green in color. He reports he is unable to perform his usual activities of daily living without becoming short of breath and required two nights of sleeping in a recliner chair to avoid orthopnea. He has been using his rescue albuterol inhaler every two to three hours over the past two days without adequate relief.

He began feeling unwell approximately five days ago following a brief URI in his wife. He developed a low-grade fever (38.0°C at home) for two days that has since defervesced. No pleuritic chest pain. No hemoptysis. He reports mild ankle swelling which he attributes to sitting more due to his breathlessness but denies severe bilateral edema. He has had three COPD exacerbations in the past 18 months, one of which required a brief hospitalization 11 months ago and two treated outpatient with prednisone and antibiotics. He was discharged on scheduled tiotropium and a moderate-dose ICS-LABA inhaler following his last hospitalization but reports inconsistent adherence to his maintenance inhalers, particularly tiotropium, due to difficulty affording the medication.

In the emergency department, oxygen saturation was 82% on room air, rising to 91% on 4L nasal cannula and 94% on 40% Venturi mask. He was in moderate respiratory distress with use of accessory muscles and pursed-lip breathing. Arterial blood gas on Venturi mask showed pH 7.34, PaCO₂ 56 mmHg, PaO₂ 68 mmHg — mild hypercapnia with partial respiratory compensation. He received nebulized albuterol and ipratropium in the ED, was initiated on IV methylprednisolone, and admitted to the pulmonary medicine service for further management.

PAST MEDICAL HISTORY
1. Chronic obstructive pulmonary disease, GOLD Stage III (severe), FEV₁ 42% predicted on most recent PFTs
2. Essential hypertension on amlodipine
3. Hyperlipidemia on pravastatin
4. Type 2 diabetes mellitus, diet-controlled
5. Prior COPD exacerbation requiring hospitalization 11 months ago
6. Obstructive sleep apnea on CPAP, partially adherent
7. Peripheral vascular disease, managed conservatively

PAST SURGICAL HISTORY
Appendectomy age 30. Bilateral inguinal hernia repair age 55.

MEDICATIONS ON ADMISSION
1. Tiotropium 18 mcg inhaled once daily — inconsistently taken due to cost
2. Fluticasone-salmeterol 250/50 mcg inhaled twice daily — adherent
3. Albuterol 90 mcg MDI 2 puffs every 4–6 hours as needed — using every 2–3 hours at home for 2 days
4. Amlodipine 10 mg orally daily
5. Pravastatin 40 mg orally nightly
6. Aspirin 81 mg orally daily
7. CPAP machine at home — inconsistent use

ALLERGIES
Tetracycline (GI intolerance). No other known drug allergies.

SOCIAL HISTORY
Retired electrician. Married, lives with wife in a two-story home. Two adult children. Active smoker — 52 pack-year history (1.5 PPD for approximately 35 years), reluctant to quit; has tried nicotine replacement twice without sustained success. Minimal alcohol — one to two beers per week. No illicit drug use. Limited mobility due to dyspnea; previously walked for exercise but has not done so in over a year. Medicare and supplemental insurance; cost of tiotropium has been a recurring barrier.

FAMILY HISTORY
Father died of emphysema and lung cancer. Mother had hypertension. One sibling with asthma.

REVIEW OF SYSTEMS
Positive: progressive dyspnea on exertion and now at rest, orthopnea requiring recliner, increased sputum production, sputum color change to yellow-green, low-grade fever (now resolved), accessory muscle use, mild bilateral ankle edema.
Negative: hemoptysis, pleuritic chest pain, new chest wall tenderness, palpitations, syncope, urinary symptoms, abdominal pain, nausea, vomiting, recent travel or sick contacts other than wife.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 37.4°C, BP 142/88 mmHg, HR 104 bpm, RR 26 breaths/min, SpO2 82% RA → 94% on 40% Venturi mask, Wt 78 kg
General: Barrel-chested man in moderate respiratory distress, using accessory muscles (sternocleidomastoid and scalene), pursed-lip breathing at rest. Alert and oriented x3. Speaking in short phrases.
HEENT: Pursed-lip breathing. Mild central cyanosis. No JVD. No cervical lymphadenopathy.
Cardiovascular: Tachycardic and regular. S1 and S2 present. No murmurs. No S3 or S4. Distant heart sounds.
Pulmonary: Significant barrel-chest deformity. Decreased breath sounds throughout with diffuse end-expiratory wheeze bilaterally. Prolonged expiratory phase. Scattered coarse rhonchi bilaterally, right greater than left. No dullness to percussion. No crackles.
Abdomen: Soft, non-tender, non-distended. No organomegaly. Normoactive bowel sounds.
Extremities: 1+ pitting edema bilateral ankles. No calf tenderness or cord. Peripheral pulses 2+. Mild digital clubbing.
Neurological: Alert and oriented. Mildly lethargic — improved with oxygen supplementation. No asterixis. No focal deficits. Cranial nerves intact.

LABORATORY DATA
ABG on 40% Venturi mask: pH 7.34, PaCO₂ 56 mmHg, PaO₂ 68 mmHg, HCO₃ 30 mEq/L, SaO₂ 94% — chronic hypercapnia with partially compensated respiratory acidosis; elevated bicarbonate consistent with chronic CO₂ retention
CBC: WBC 13.8 K/uL (elevated, neutrophil predominant with 82% PMNs), Hemoglobin 15.2 g/dL (polycythemia consistent with chronic hypoxemia), Hematocrit 46.1%, Platelets 248 K/uL
BMP: Na 137 mEq/L, K 3.5 mEq/L, Cl 98 mEq/L, HCO₃ 30 mEq/L (chronically elevated), BUN 22 mg/dL, Creatinine 1.0 mg/dL, Glucose 188 mg/dL (steroid-related on repeat)
Procalcitonin: 0.64 ng/mL — mildly elevated, supporting bacterial component
Troponin I: <0.02 — negative
BNP: 188 pg/mL — mildly elevated
Sputum culture: Sent on admission; resulted on day 3: Haemophilus influenzae, susceptible to amoxicillin-clavulanate and levofloxacin, resistant to ampicillin

Hospital Day 3 ABG (on 2L NC): pH 7.38, PaCO₂ 52 mmHg, PaO₂ 72 mmHg — improvement in ventilation
Discharge BMP: Na 138, K 3.8, BUN 18, Cr 0.9, Glucose 148 — glucose improving as steroids tapered

IMAGING AND DIAGNOSTICS
Chest X-Ray (Admission): Hyperinflation with flattened diaphragms and increased AP diameter consistent with emphysema. Increased interstitial markings in the right lower lobe raising concern for superimposed pneumonia vs. atelectasis. No frank lobar consolidation. No pneumothorax. No pleural effusion. Cardiomegaly, borderline.
Chest X-Ray (Hospital Day 3): Slight improvement in right lower lobe haziness. Persistent hyperinflation. No new infiltrate. No pneumothorax.
CT Chest without contrast (Hospital Day 1, to evaluate for PE and characterize infiltrate): No pulmonary embolism identified. Emphysematous changes predominantly in the upper lobes bilaterally with areas of bullous disease. Mild bronchial wall thickening consistent with chronic airway disease. Ground-glass opacity in the right lower lobe consistent with early infectious or inflammatory consolidation. No pleural effusion. No pneumothorax. No mediastinal adenopathy.
12-Lead ECG: Sinus tachycardia at 104 bpm. Right axis deviation. P pulmonale (tall, peaked P waves in lead II). Low-voltage QRS. No acute ST-T wave changes. No Q-waves.

HOSPITAL COURSE
Mr. Briggs was admitted to the pulmonary medicine floor with continuous pulse oximetry and supplemental oxygen titrated to maintain SpO₂ 90–94% (avoiding over-oxygenation given chronic CO₂ retention). He was placed on continuous bronchodilator therapy with ipratropium nebulizations every four hours and albuterol nebulizations every four hours initially, transitioning to every six hours by day 2 as his clinical status improved.

IV methylprednisolone 125 mg every six hours was initiated in the emergency department and transitioned to 40 mg IV every 12 hours on admission to the floor. Given the sputum purulence, leukocytosis, and CT findings of right lower lobe infiltrate, empirical antibiotic therapy was initiated with azithromycin 500 mg IV daily targeting atypical organisms in addition to coverage for typical community-acquired pathogens. When sputum culture resulted on day 3 growing Haemophilus influenzae, antibiotics were narrowed to levofloxacin 750 mg orally daily for a total five-day course.

Corticosteroids were transitioned to oral prednisone 40 mg daily on hospital day 3 and tapered to 30 mg on day 4, with discharge on a 10-day outpatient oral steroid taper regimen. Hyperglycemia developed with glucose values ranging 200–280 mg/dL in the setting of corticosteroid therapy; sliding scale insulin was implemented with acceptable glucose control, and the patient was educated about steroid-induced hyperglycemia and instructed to monitor home glucose values during the taper. His home diabetes regimen does not include insulin, so the team communicated glucose monitoring instructions clearly.

His dyspnea improved progressively. Oxygen requirements decreased from 40% Venturi mask on admission to 2L nasal cannula by day 3 and 1L nasal cannula by day 4. By hospital day 5 he maintained SpO₂ 92% on room air at rest and 89% with ambulation to the hallway. Given his chronic hypoxemia at baseline, no additional supplemental oxygen was prescribed for home beyond his prior level.

Respiratory therapy evaluated the patient and performed inhaler technique education. A pharmacist enrolled him in a patient assistance program for tiotropium to address the cost barrier. Smoking cessation counseling was again offered; he declined varenicline but agreed to nicotine patch therapy and accepted a referral to a behavioral health tobacco cessation program. He was ambulatory with minimal assistance by discharge and deemed safe for home with close outpatient follow-up arranged.

DISCHARGE DIAGNOSES
1. Acute exacerbation of chronic obstructive pulmonary disease, unspecified — primary admission diagnosis
2. Superimposed bacterial lower respiratory tract infection — Haemophilus influenzae, right lower lobe, confirmed on sputum culture
3. Chronic hypercapnic respiratory failure — baseline, partially compensated
4. Essential hypertension — active comorbidity
5. Type 2 diabetes mellitus — active comorbidity, complicated by steroid-induced hyperglycemia during admission
6. Hyperlipidemia — active comorbidity
7. Obstructive sleep apnea — active comorbidity
8. Nicotine dependence, cigarettes, active ongoing use — primary modifiable risk factor for COPD progression
9. Peripheral vascular disease — active comorbidity

DISCHARGE CONDITION
Improved but not at baseline. Dyspnea at rest resolved. Able to ambulate to the hallway. SpO₂ 92% on room air at rest. Sputum production decreased. Off nebulizers; on inhaler therapy. Tolerating oral medications.

DISCHARGE MEDICATIONS
1. Tiotropium 18 mcg inhaled once daily — patient assistance program enrolled, supply provided at discharge
2. Fluticasone-salmeterol 250/50 mcg inhaled twice daily — continued
3. Albuterol 90 mcg MDI 2 puffs every 4–6 hours as needed — continued
4. Prednisone 30 mg orally daily x2 days, then 20 mg x2 days, then 10 mg x2 days, then stop (6-day taper from discharge)
5. Levofloxacin 750 mg orally daily — complete 5-day course; 2 days remaining at discharge
6. Amlodipine 10 mg orally daily — unchanged
7. Pravastatin 40 mg orally nightly — unchanged
8. Aspirin 81 mg orally daily — unchanged
9. Nicotine patch 21 mg/24 hours, apply to upper arm daily — new, for smoking cessation

DISCHARGE INSTRUCTIONS
You are being discharged after treatment for a COPD flare-up caused by a bacterial lung infection. Your breathing has improved but you are not yet back to your usual baseline. Complete the full antibiotic course (levofloxacin) and the full steroid taper (prednisone) as directed — do not stop either early. Use your inhalers every day as prescribed. Use your rescue inhaler (albuterol) as needed for breakthrough symptoms, but if you are using it more than every four hours you need to call your doctor or go to the emergency department. If your breathing gets significantly worse, your lips or fingernails turn blue, or you become confused, call 911. Check your blood sugar twice daily during the steroid taper and write the values down. Stopping smoking is the single most important thing you can do to slow this disease — please use the nicotine patch every day and keep your tobacco cessation program appointment.

FOLLOW-UP
1. Pulmonary Medicine (Dr. Osei): 7 days post-discharge — reassess spirometry, adjust inhaler regimen, review glucose log
2. Primary Care: 10 days post-discharge — blood pressure, diabetes management
3. Tobacco Cessation Program: Appointment arranged within 2 weeks
4. Pulmonary Rehabilitation: Referral placed — patient to be contacted for enrollment""",
    },
    {
        "title": "Acute Hypoxemic Respiratory Failure — Severe CAP",
        "category": "Pulmonary / Critical Care",
        "expected_codes": ["J9601"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Gloria Mendez, 61F | MRN: 8820341
Admission: 10/21/2025 | Discharge: 10/29/2025 | LOS: 8 days
Attending: Dr. T. Nguyen, MD | Service: Medical ICU / Pulmonary Critical Care

CHIEF COMPLAINT
Severe shortness of breath, high fever, and confusion for two days, found to have critical hypoxemia on arrival.

HISTORY OF PRESENT ILLNESS
Ms. Mendez is a 61-year-old woman with a history of type 2 diabetes mellitus, hypertension, and obesity who presents with a two-day history of progressive dyspnea, high fever (39.6°C at home), productive cough with rust-colored sputum, and altered mental status noted by her daughter, who describes her mother as confused and unable to complete sentences. The patient reports that she felt a mild sore throat and body aches approximately five days before admission, which she initially treated with over-the-counter medications. Over the subsequent two to three days, her symptoms escalated dramatically with onset of shaking chills, pleuritic right-sided chest pain, worsening productive cough, and profound fatigue preventing her from leaving bed.

Her daughter brought her to the emergency department after finding her disoriented and noting her lips appeared bluish. She had not eaten or taken her medications for approximately 48 hours prior to admission. She had not received this season's influenza vaccine and has never received pneumococcal vaccination. She denies sick contacts in the prior two weeks, recent travel, aspiration event, animal exposures, or recent healthcare exposures. She has no history of recurrent pneumonia, structural lung disease, or immunocompromising conditions. She has not been on corticosteroids or immunosuppressants.

On arrival to the emergency department, she was in severe respiratory distress with an oxygen saturation of 72% on room air. She was immediately placed on high-flow nasal cannula at 60 L/min with FiO₂ 100%, with oxygen saturation improving to 88%. She was subsequently transitioned to non-invasive positive pressure ventilation (BIPAP: IPAP 14, EPAP 8, FiO₂ 80%) with improvement in SpO₂ to 92–94% and some improvement in her mental status. Chest radiograph demonstrated right lower lobe and right middle lobe consolidation with associated moderate right-sided pleural effusion. Initial ABG revealed pH 7.28, PaCO₂ 48, PaO₂ 52 on high-flow oxygen. She was emergently admitted to the MICU.

PAST MEDICAL HISTORY
1. Type 2 diabetes mellitus, 10-year history on metformin and glipizide
2. Essential hypertension on lisinopril and hydrochlorothiazide
3. Obesity, BMI 38
4. Hyperlipidemia on simvastatin
5. Gastroesophageal reflux disease on omeprazole
6. No known history of pulmonary disease

PAST SURGICAL HISTORY
Laparoscopic cholecystectomy age 52. C-section age 28.

MEDICATIONS ON ADMISSION
1. Metformin 1000 mg orally twice daily
2. Glipizide 10 mg orally twice daily
3. Lisinopril 20 mg orally daily
4. Hydrochlorothiazide 25 mg orally daily
5. Simvastatin 40 mg orally nightly
6. Omeprazole 20 mg orally daily

ALLERGIES
No known drug allergies.

SOCIAL HISTORY
Works as a school cafeteria supervisor. Lives with her adult daughter. No tobacco use. Rare alcohol — one to two drinks per year at celebrations. No illicit drug use. Originally from Guatemala, has lived in the US for 25 years. Spanish-speaking, medical interpreter used throughout hospitalization. Limited healthcare access historically; last PCP visit was approximately two years prior.

FAMILY HISTORY
Mother had diabetes and died of stroke. Father had hypertension and coronary artery disease. No known family history of immunodeficiency.

REVIEW OF SYSTEMS
Positive: fever (39.6°C at home), shaking chills, severe dyspnea at rest, productive cough with rust-colored sputum, right pleuritic chest pain, altered mental status (confusion noted by family), profound fatigue, anorexia, decreased oral intake x48 hours, myalgias.
Negative: hemoptysis, abdominal pain, diarrhea, urinary symptoms, rash, joint pain, recent travel, sick contacts, recent hospitalizations.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 39.4°C, BP 96/58 mmHg (hypotensive), HR 122 bpm, RR 32 breaths/min, SpO₂ 72% RA → 88% on HFNC 60L/100% FiO₂, Wt 98 kg
General: Obese woman in severe respiratory distress. Markedly tachypneic, using all accessory muscles. Altered mental status — responds to voice but disoriented to date and place. Mild central cyanosis.
HEENT: Dry mucous membranes. Mild central cyanosis of lips. No JVD. No lymphadenopathy. No meningismus.
Cardiovascular: Tachycardic and regular. No murmurs. Hypotensive.
Pulmonary: Dullness to percussion right lung base through mid-field. Decreased breath sounds right lower and middle lobes. Coarse crackles right lung field throughout. Egophony at right lung base. Bronchial breath sounds over consolidation. Left lung relatively clear with mild transmitted sounds.
Abdomen: Soft, non-tender, mildly distended. No organomegaly. Hypoactive bowel sounds.
Extremities: No significant edema. Peripheral pulses present but weak. Capillary refill approximately 3 seconds.
Neurological: Responds to verbal stimuli. Disoriented x2 (person, time). Follows simple commands inconsistently. No focal motor deficits. No Babinski. No asterixis.

LABORATORY DATA
ABG (on HFNC/BIPAP): pH 7.28, PaCO₂ 48 mmHg, PaO₂ 52 mmHg, HCO₃ 22 mEq/L, SpO₂ 88% — acute hypoxemic and partially hypercapnic respiratory failure; P/F ratio 52 consistent with severe ARDS criteria
CBC: WBC 22.4 K/uL (markedly elevated, 90% PMNs, 8% bands), Hemoglobin 11.8 g/dL, Hematocrit 35.4%, Platelets 96 K/uL (thrombocytopenia, likely sepsis-related)
BMP: Na 131 mEq/L (hyponatremia), K 3.2 mEq/L, Cl 96 mEq/L, HCO₃ 22 mEq/L, BUN 42 mg/dL, Creatinine 2.1 mg/dL (baseline unknown, likely AKI), Glucose 384 mg/dL (severe hyperglycemia)
Lactate: 4.2 mmol/L — elevated, consistent with septic shock
Procalcitonin: 28.4 ng/mL — markedly elevated, consistent with severe bacterial infection
HbA1c: 10.8% — poorly controlled diabetes
Blood cultures (x2 sets): Streptococcus pneumoniae, penicillin-susceptible, both bottles positive — bacteremic pneumococcal pneumonia
Urine Legionella antigen: Negative
Urine pneumococcal antigen: Positive
Respiratory viral panel: Negative (influenza A/B, RSV, COVID-19)
Sputum culture: Streptococcus pneumoniae — concordant with blood cultures
LFTs: Mildly elevated AST 68, ALT 44 — likely sepsis-related
Coagulation: PT/INR 1.6, aPTT 44 seconds, fibrinogen 680 — early DIC pattern
Ferritin: 2,840 ng/mL

IMAGING AND DIAGNOSTICS
Chest X-Ray (Admission): Right lower lobe and right middle lobe consolidation. Moderate right-sided pleural effusion. No pneumothorax. Left lung relatively preserved. Cardiomegaly borderline.
CT Chest with IV contrast (Hospital Day 1): Extensive right lower lobe and right middle lobe consolidation consistent with lobar pneumonia. Moderate right-sided parapneumonic pleural effusion without frank empyema (non-loculated, no internal septations). No pulmonary embolism. Left lung with scattered small patchy ground-glass opacities suggesting early bilateral involvement. No mediastinal adenopathy. No cavitation.
Chest X-Ray (Hospital Day 4): Interval improvement in right-sided consolidation. Reduced pleural effusion. New left lower lobe patchy opacities.
Chest X-Ray (Day 7, pre-discharge): Significant interval improvement. Residual right lower lobe haziness. Small residual right pleural effusion. Left lower lobe changes resolving.
Transthoracic Echo (Hospital Day 2): LVEF 55%, preserved. No significant valvular disease. No wall motion abnormality. No pericardial effusion. IVC mildly dilated. Consistent with sepsis-related physiology.

HOSPITAL COURSE
Ms. Mendez was admitted directly to the MICU for management of severe sepsis/septic shock in the setting of bacteremic pneumococcal pneumonia complicated by acute hypoxemic respiratory failure. Sepsis resuscitation was initiated per protocol with 30 mL/kg IV crystalloid bolus (2.9 L given her weight) over the first three hours, followed by vasopressor initiation with norepinephrine for persistent hypotension despite fluid resuscitation. Blood pressure improved to the 100–110/60–70 mmHg range on norepinephrine within six hours.

Empirical antibiotic therapy was initiated with ceftriaxone 2g IV daily and azithromycin 500 mg IV daily. When blood and sputum cultures confirmed penicillin-susceptible Streptococcus pneumoniae on hospital day 2, azithromycin was discontinued and ceftriaxone was continued as definitive monotherapy. She completed a 10-day course of ceftriaxone IV (transitioned to amoxicillin-clavulanate orally on day 8).

She was managed on BiPAP for the first 36 hours. Given her clinical deterioration with worsening P/F ratio (nadir 48 on hospital day 2) and increased work of breathing, the decision was made on hospital day 2 to proceed with endotracheal intubation and mechanical ventilation using a lung-protective strategy (tidal volume 6 mL/kg ideal body weight, PEEP 12 cmH₂O, plateau pressure <30 cmH₂O, FiO₂ titrated to SpO₂ 92–95%). She was sedated with propofol and fentanyl drips.

Vasopressor support was weaned over hospital days 3–4 as her hemodynamics improved with antibiotics and infection source control. Norepinephrine was discontinued on hospital day 4. Renal function peaked at creatinine 2.6 on day 2 then improved progressively — consistent with sepsis-associated AKI resolving with treatment. No renal replacement therapy was required.

She was successfully extubated on hospital day 5 following a spontaneous breathing trial. Post-extubation, she required supplemental oxygen via nasal cannula at 3L for two days, weaned to room air on hospital day 7. Mental status cleared fully by hospital day 4 after the acute infection was treated. Glucose management was initiated with an insulin drip in the ICU, transitioned to a basal-bolus insulin regimen on the floor. Endocrinology was consulted and adjusted her outpatient diabetes regimen given the markedly elevated HbA1c of 10.8%.

She was ambulatory with physical therapy assistance by hospital day 7 and discharged home with her daughter in stable condition on hospital day 8 with close follow-up arranged.

DISCHARGE DIAGNOSES
1. Acute respiratory failure with hypoxia — primary admission diagnosis, secondary to pneumococcal pneumonia
2. Severe community-acquired pneumonia — bacteremic Streptococcus pneumoniae, right lower and middle lobe
3. Septic shock, resolved
4. Acute kidney injury, resolved — peak creatinine 2.6, at baseline 1.0 at discharge
5. Type 2 diabetes mellitus with hyperglycemia — poorly controlled; HbA1c 10.8%
6. Thrombocytopenia — sepsis-related, resolving
7. Essential hypertension — active comorbidity
8. Obesity, BMI 38 — active comorbidity
9. Hyperlipidemia — active comorbidity

DISCHARGE CONDITION
Stable. Ambulatory with mild assistance. SpO₂ 96% on room air. Afebrile >72 hours. Mental status at baseline. Tolerating oral diet and medications.

DISCHARGE MEDICATIONS
1. Amoxicillin-clavulanate 875/125 mg orally twice daily — complete 10-day antibiotic course; 2 days remaining
2. Insulin glargine 20 units subcutaneously at bedtime — NEW; endocrinology-recommended
3. Metformin 500 mg orally twice daily — REDUCED dose during recovery; resume 1000 mg BID in 4 weeks per endocrinology
4. Glipizide 5 mg orally daily — REDUCED dose
5. Lisinopril 20 mg orally daily — resumed; was held during acute illness
6. Hydrochlorothiazide 25 mg orally daily — resumed
7. Simvastatin 40 mg orally nightly — unchanged
8. Omeprazole 20 mg orally daily — unchanged

DISCHARGE INSTRUCTIONS
You were very ill with a serious bacterial lung infection (pneumonia) caused by bacteria in your blood, and your lungs were not getting enough oxygen. You needed a breathing tube and intensive care. You have recovered significantly. Complete the antibiotics as prescribed. Take all your medications daily. Your blood sugar was very high during your illness — you now have insulin added to your regimen. Test your blood sugar twice daily and write down the numbers to review with your endocrinologist. If you develop fever above 38.5°C, severe shortness of breath, confusion, or blood sugar above 400, go to the emergency department immediately. Get your pneumococcal and influenza vaccines as soon as you are recovered — ask your primary care doctor.

FOLLOW-UP
1. Pulmonary Medicine (Dr. Nguyen): 2 weeks post-discharge — repeat chest imaging, lung function assessment
2. Endocrinology: 2 weeks post-discharge — insulin titration, diabetes management
3. Primary Care: 1 week post-discharge — medication review, vaccines
4. Infectious Disease: Outpatient follow-up 2 weeks — review blood culture sensitivities, ensure treatment complete""",
    },
    {
        "title": "Type 2 Diabetes — Severe Hyperglycemia and HHS",
        "category": "Endocrine",
        "expected_codes": ["E1165"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Carl Whitfield, 67M | MRN: 5539204
Admission: 09/02/2025 | Discharge: 09/07/2025 | LOS: 5 days
Attending: Dr. R. Sharma, MD | Service: Internal Medicine / Endocrinology

CHIEF COMPLAINT
Confusion, extreme thirst, and weakness for three days; found to have glucose 940 mg/dL and altered mental status in the emergency department.

HISTORY OF PRESENT ILLNESS
Mr. Whitfield is a 67-year-old man with a ten-year history of type 2 diabetes mellitus managed with oral agents who was brought to the emergency department by his son after three days of worsening confusion, extreme polydipsia, polyuria, generalized weakness, and inability to care for himself. The son reports that his father appeared disoriented at home, did not recognize his address, and was consuming large amounts of water without relief of his thirst. He had not eaten significant solid food for approximately four days. He had not been taking his metformin or glipizide for at least one week — he ran out of both medications and told his son he felt too ill to go to the pharmacy.

On further history, the patient has had progressively worsening hyperglycemic symptoms over two to three weeks including polydipsia, polyuria estimated at 10–15 voidings per day, blurred vision, fatigue, and a 15-pound unintentional weight loss over the past month. He denies fever, chest pain, shortness of breath, or abdominal pain. He endorses nausea but no vomiting. He has no prior history of diabetic ketoacidosis or hyperosmolar hyperglycemic state. He has not received any new medications and denies glucocorticoid use.

On arrival to the emergency department, his blood glucose was 940 mg/dL, serum sodium 148 mEq/L (corrected sodium approximately 158 mEq/L), serum osmolality calculated at 368 mOsm/kg, and pH 7.38 (no significant acidosis). Urine ketones trace. He was alert but disoriented to time and place. He was markedly dehydrated on examination with tachycardia at 118 bpm and blood pressure 88/54 mmHg (sepsis-like hypotension from profound dehydration). He was admitted to a monitored bed for management of hyperosmolar hyperglycemic state (HHS).

PAST MEDICAL HISTORY
1. Type 2 diabetes mellitus, diagnosed 10 years ago, previously managed with metformin and glipizide
2. Essential hypertension on lisinopril
3. Hyperlipidemia on atorvastatin
4. Obesity, BMI 33
5. Prior episodes of poorly controlled diabetes with HbA1c > 9% documented on two prior occasions in the past three years, each time associated with medication non-adherence
6. Benign prostatic hyperplasia on tamsulosin

PAST SURGICAL HISTORY
No significant surgical history.

MEDICATIONS ON ADMISSION
1. Metformin 1000 mg orally twice daily — not taking for at least one week
2. Glipizide 10 mg orally twice daily — not taking for at least one week
3. Lisinopril 10 mg orally daily
4. Atorvastatin 40 mg orally nightly
5. Tamsulosin 0.4 mg orally nightly

ALLERGIES
Sulfonamides (rash).

SOCIAL HISTORY
Retired postal worker. Widowed, lives alone in a single-story home. One adult son lives locally. Former smoker, 20 pack-year history, quit 15 years ago. Occasional alcohol, one to two drinks weekly. No illicit drug use. Fixed income, Medicare coverage. Has difficulty accessing pharmacy due to lack of consistent transportation. History of food insecurity noted — son reports father has limited food variety at home.

FAMILY HISTORY
Mother had type 2 diabetes. Father had hypertension and died of ischemic heart disease at age 72. One sibling with type 2 diabetes.

REVIEW OF SYSTEMS
Positive: polydipsia, polyuria (estimated 10–15 voids daily for 2–3 weeks), blurred vision, confusion (3 days), generalized weakness, fatigue, anorexia, nausea, 15-lb unintentional weight loss over past month.
Negative: vomiting, abdominal pain, chest pain, shortness of breath, fever, chills, productive cough, diarrhea, focal neurological deficits, headache, seizure activity, skin breakdown, lower extremity ulcers.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 37.2°C, BP 88/54 mmHg (hypotensive), HR 118 bpm, RR 18 breaths/min, SpO₂ 97% RA, Wt 87 kg
General: Obese older man, appearing fatigued and mildly confused. Markedly dry mucous membranes. Skin tenting present. Speaks slowly but follows commands.
HEENT: Dry oral mucosa. Sunken eyes. Mucous membranes parched. No JVD. No thyromegaly.
Cardiovascular: Tachycardic, regular. No murmurs. Hypotensive.
Pulmonary: Clear to auscultation bilaterally. No wheeze, crackles, or rhonchi. Respiratory effort unlabored, no Kussmaul breathing (distinguishes from DKA).
Abdomen: Soft, mildly tender diffusely without guarding or rebound. No organomegaly. Hypoactive bowel sounds. No peritoneal signs.
Extremities: No lower extremity edema. No active ulcers or wounds. Decreased skin turgor. Peripheral pulses present but weak. Capillary refill 3–4 seconds.
Neurological: Alert but disoriented to date and location. Follows simple commands. Slow responses. No focal motor deficits. No Babinski. Cranial nerves grossly intact.

LABORATORY DATA
Point-of-care glucose: 940 mg/dL — critically elevated
BMP (Admission): Na 148 mEq/L (hypernatremia), K 3.8 mEq/L, Cl 108 mEq/L, HCO₃ 24 mEq/L (normal — no significant acidosis), BUN 68 mg/dL, Creatinine 2.8 mg/dL (baseline unknown), Glucose 940 mg/dL
Corrected sodium (for hyperglycemia): Na corrected = 148 + 1.6 × [(940–100)/100] = ~162 mEq/L — severe hypernatremia when corrected
Calculated serum osmolality: 2 × 148 + 940/18 + 68/2.8 = approximately 370 mOsm/kg — severely elevated (HHS threshold >320)
ABG: pH 7.38, PaCO₂ 38 mmHg, PaO₂ 92 mmHg, HCO₃ 22 mEq/L — no significant acidosis; confirms HHS rather than DKA
Serum ketones: Trace — consistent with HHS (mild ketonemia from starvation, not DKA)
Urine ketones: Trace
CBC: WBC 14.2 K/uL (mildly elevated — likely stress/dehydration response), Hemoglobin 16.8 g/dL (hemoconcentration), Hematocrit 50.4%, Platelets 312 K/uL
HbA1c: 13.4% — severely uncontrolled; consistent with months of poor glycemic control
Lactate: 2.1 mmol/L — mildly elevated, likely from hypoperfusion and dehydration
Troponin I: <0.02 — negative
Urinalysis: Specific gravity 1.040 (markedly concentrated), 4+ glucose, no leukocyte esterase, no nitrites — no UTI to suggest precipitating infection
Blood cultures (x2): No growth at 72 hours
LFTs: Within normal limits
Lipase: 28 (normal)
Phosphorus: 2.1 mg/dL (hypophosphatemia on repletion anticipated)

Hospital Day 2 BMP: Na 142, K 3.6, BUN 48, Cr 1.8, Glucose 420 — improving with rehydration and insulin
Hospital Day 4 BMP: Na 140, K 4.0, BUN 26, Cr 1.2, Glucose 188 — near normalization
Discharge BMP: Na 139, K 4.1, BUN 20, Cr 1.0, Glucose 162 — at estimated baseline

IMAGING AND DIAGNOSTICS
Chest X-Ray (Admission): No acute cardiopulmonary process. No pneumonia. No pulmonary edema. Normal cardiac silhouette.
12-Lead ECG (Admission): Sinus tachycardia at 118 bpm. No acute ST changes. No peaked T-waves (hyperkalemia excluded). No QTc prolongation. No ischemic changes.
CT Head without contrast (Hospital Day 1, due to altered mental status): No acute intracranial abnormality. No hemorrhage. No large territorial infarct. Mild cortical atrophy appropriate for age.
Right lower extremity Doppler ultrasound (Day 2, due to mild right calf swelling): No deep vein thrombosis identified.

HOSPITAL COURSE
Mr. Whitfield was admitted to a monitored internal medicine bed with telemetry and hourly glucose monitoring for management of hyperosmolar hyperglycemic state. Aggressive IV fluid resuscitation was initiated as the cornerstone of HHS management. Given his estimated free water deficit of approximately 9–10 liters (calculated using corrected sodium and body weight), he was started on 0.9% normal saline at 1 liter per hour for the first two hours, then transitioned to 0.45% half-normal saline at 500 mL/hour targeting a reduction in serum osmolality of no more than 3 mOsm/kg/hour to avoid cerebral edema. His blood pressure improved to 108/68 mmHg after the initial two-liter fluid bolus and vasopressors were not required.

An insulin drip was initiated at 0.1 units/kg/hour (8.7 units/hour) once the serum potassium was confirmed at 3.8 mEq/L and IV fluids were running. Glucose was checked hourly and the insulin drip rate adjusted per protocol to target glucose reduction of 50–75 mg/dL/hour. Glucose decreased from 940 to 620 mg/dL in the first six hours. When glucose reached 300 mg/dL on hospital day 2, dextrose was added to the IV fluid to prevent hypoglycemia while continuing insulin to clear any residual ketonemia.

Electrolytes were monitored every four hours during active treatment. Potassium supplementation was administered proactively as expected with insulin therapy and hydration; potassium remained in the range of 3.6–4.2 mEq/L throughout. Phosphorus dropped to 1.8 mg/dL on day 2 and was repleted with IV sodium phosphate per protocol. Magnesium was also repleted as needed.

Mental status improved substantially by hospital day 2 after approximately 12 hours of IV fluid resuscitation and glucose reduction. By day 3 he was oriented x3, engaging in appropriate conversation, and able to participate in diabetes education. The insulin drip was transitioned to subcutaneous basal-bolus insulin therapy on hospital day 3 (glargine 30 units at bedtime + lispro sliding scale with meals) with continued glucose monitoring every four hours. Endocrinology was consulted and recommended a regimen of glargine plus low-dose glipizide with plan to reassess the need for insulin at 3-month follow-up based on outpatient glucose logs.

A diabetes educator and pharmacist met with the patient and his son on hospital days 3 and 4. Insulin injection technique, glucometer use, hypoglycemia recognition and treatment, sick day management, and the critical importance of medication adherence were reviewed extensively. The son was educated and expressed willingness to assist with pharmacy pickup and medication monitoring. A social work consult was placed and a connection to a community health worker program was arranged for ongoing support. A 90-day supply of glipizide and metformin was filled via the hospital's charity pharmacy program prior to discharge.

DISCHARGE DIAGNOSES
1. Type 2 diabetes mellitus with hyperglycemia, hyperosmolar hyperglycemic state — primary admission diagnosis
2. Severe dehydration, resolved with IV fluid resuscitation
3. Acute kidney injury, resolved — peak creatinine 2.8, at baseline at discharge
4. Hypernatremia, resolved
5. Hypophosphatemia, repleted
6. Medication non-adherence — primary precipitating factor
7. Essential hypertension — active comorbidity
8. Hyperlipidemia — active comorbidity
9. Benign prostatic hyperplasia — active comorbidity
10. Obesity — active comorbidity

DISCHARGE CONDITION
Stable. Alert and oriented x3 at baseline. Ambulatory without assistance. Blood glucose 162 on morning of discharge. Tolerating oral diet. No IV access required.

DISCHARGE MEDICATIONS
1. Insulin glargine 30 units subcutaneously at bedtime — NEW
2. Lispro insulin 4 units subcutaneously with each meal — NEW (with sliding scale guidance provided)
3. Glipizide 5 mg orally daily with breakfast — REDUCED from 10 mg twice daily
4. Metformin 500 mg orally twice daily — REDUCED dose; increase to 1000 mg BID in 4 weeks if tolerated
5. Lisinopril 10 mg orally daily — resumed
6. Atorvastatin 40 mg orally nightly — unchanged
7. Tamsulosin 0.4 mg orally nightly — unchanged

DISCHARGE INSTRUCTIONS
You were admitted because your blood sugar was dangerously high (over 900) and you were severely dehydrated. This happened because you ran out of your diabetes medications. Never stop your diabetes medications without talking to your doctor. You now have insulin added to your regimen — your son has been taught how to help you give injections. Check your blood sugar every morning before eating and before bedtime. Write down every result. If your blood sugar is above 400, call your doctor or go to the emergency room. If you feel shaky, sweaty, or confused, eat 15 grams of fast-acting carbohydrate (4 glucose tablets or half a cup of juice) immediately. Drink water throughout the day. Keep all follow-up appointments — they are essential to adjusting your medications.

FOLLOW-UP
1. Endocrinology: 2 weeks post-discharge — insulin titration, HbA1c recheck at 3 months
2. Primary Care: 1 week post-discharge — blood pressure, kidney function, medication review
3. Diabetes Education (outpatient): Arranged, within 2 weeks
4. Social Work / Community Health Worker: Enrolled — first home visit within one week""",
    },
    {
        "title": "Type 2 Diabetes with Diabetic Chronic Kidney Disease",
        "category": "Endocrine / Nephrology",
        "expected_codes": ["E1122"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Patricia Nguyen, 59F | MRN: 7203841
Admission: 08/18/2025 | Discharge: 08/23/2025 | LOS: 5 days
Attending: Dr. M. Clarke, MD | Service: Internal Medicine / Nephrology

CHIEF COMPLAINT
Worsening leg swelling, decreased urine output, and elevated creatinine found on outpatient labs prompting urgent admission.

HISTORY OF PRESENT ILLNESS
Ms. Nguyen is a 59-year-old woman with a 15-year history of type 2 diabetes mellitus, hypertension, and known stage 3b chronic kidney disease (eGFR baseline 38 mL/min/1.73m²) who presents following a call from her nephrologist after outpatient labs showed creatinine 3.1 mg/dL (baseline 1.8–2.0) and potassium 5.8 mEq/L with a concurrent increase in urine albumin-to-creatinine ratio to 1,480 mg/g (prior value 680 mg/g six months ago). She endorses a three-week history of progressive bilateral leg swelling significantly worse than her usual mild ankle edema, decreased urine output over the past ten days, and facial puffiness noted by her family for the past week. She also reports new exertional dyspnea with one flight of stairs that she previously climbed without difficulty.

She denies fever, chills, gross hematuria, flank pain, or urinary symptoms. She has not started any new medications. She did use ibuprofen approximately three to four times weekly for knee pain over the past month — a practice she acknowledges was against her nephrologist's standing instruction to avoid NSAIDs. She has been adherent to her other medications. She has not had any contrast studies. She has had no recent diarrhea, vomiting, or poor oral intake. She has not changed her diet significantly, though she acknowledges her sodium intake has been higher than usual at family meals. She has no history of nephrotic syndrome or nephritic syndrome previously evaluated.

Her diabetes has been suboptimally controlled over the past year with HbA1c values ranging from 8.2 to 9.0%. She has had diabetic nephropathy as the presumed etiology of her CKD based on diabetic retinopathy confirmed by ophthalmology, absent hematuria, and a non-invasive clinical picture consistent with diabetic glomerulosclerosis. A kidney biopsy was performed three years ago confirming Class IIb diabetic nephropathy on the Tervaert classification.

PAST MEDICAL HISTORY
1. Type 2 diabetes mellitus, 15-year history; history of poor glycemic control
2. Chronic kidney disease Stage 3b, eGFR baseline 38, secondary to diabetic nephropathy confirmed on biopsy
3. Hypertension, 12-year history
4. Diabetic retinopathy — non-proliferative, managed by ophthalmology
5. Peripheral diabetic neuropathy — bilateral lower extremities
6. Hyperlipidemia on atorvastatin
7. Anemia of chronic kidney disease, managed with iron supplementation
8. Obesity, BMI 36

PAST SURGICAL HISTORY
Kidney biopsy three years ago (percutaneous, uncomplicated). Hysterectomy age 44.

MEDICATIONS ON ADMISSION
1. Metformin 500 mg orally twice daily (dose-reduced for CKD; eGFR 38 permits continued use)
2. Glipizide 5 mg orally daily
3. Lisinopril 40 mg orally daily
4. Amlodipine 10 mg orally daily
5. Atorvastatin 40 mg orally nightly
6. Furosemide 40 mg orally daily
7. Ferrous sulfate 325 mg orally twice daily
8. Sodium bicarbonate 650 mg orally three times daily (for CKD-associated metabolic acidosis)
9. Calcium carbonate 500 mg orally with meals (phosphate binding)
10. Ibuprofen 400 mg orally as needed — patient using 3–4x/week (NSAID use against medical advice)

ALLERGIES
Penicillin (rash, childhood history). ACE inhibitor cough was noted but patient prefers to continue lisinopril given renoprotective benefit; cough present but tolerable.

SOCIAL HISTORY
Works part-time as a medical records clerk. Lives with her husband and one adult child. Nonsmoker. No alcohol use. No illicit drug use. Vietnamese-American; diet higher in rice and some salted preserved foods. Medical interpreter available as needed (English proficient but family uses Vietnamese at home). Medicare and Medicaid dual coverage.

FAMILY HISTORY
Mother had type 2 diabetes and died of end-stage renal disease on dialysis at age 71. Father had hypertension and coronary artery disease. One sibling with type 2 diabetes.

REVIEW OF SYSTEMS
Positive: bilateral lower extremity edema (worsening 3 weeks), facial edema (1 week), decreased urine output (10 days), exertional dyspnea (1 flight of stairs, new), fatigue, generalized weakness.
Negative: fever, chills, chest pain at rest, orthopnea, paroxysmal nocturnal dyspnea, gross hematuria, flank pain, dysuria, frequency, nausea, vomiting, diarrhea, joint pain beyond chronic knee OA, rash, weight gain >2 lbs (she doesn't weigh herself routinely).

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 36.8°C, BP 164/96 mmHg, HR 84 bpm, RR 18 breaths/min, SpO₂ 95% RA, Wt 98.4 kg (prior visit 94.1 kg — approximately 4.3 kg weight gain over past 6 weeks)
General: Obese woman in no acute distress at rest. Alert and oriented x3. Mild periorbital puffiness.
HEENT: Periorbital edema present bilaterally. Oral mucosa moist. No JVD at 45 degrees. No lymphadenopathy.
Cardiovascular: Regular rate and rhythm. S1 and S2. No S3 or S4. No murmurs. No rubs.
Pulmonary: Mild dullness to percussion at bilateral bases. Fine inspiratory crackles at bilateral lung bases. No wheeze. Respiratory effort unlabored.
Abdomen: Soft, non-tender, mildly distended. No organomegaly. Shifting dullness present (ascites possible vs bowel). Normoactive bowel sounds.
Extremities: 3+ pitting edema bilateral lower extremities to the mid-shin. Mild pretibial edema. Skin intact, no open wounds. Pulses 2+ bilaterally. Diminished monofilament sensation bilateral feet (consistent with known neuropathy).
Neurological: Alert and oriented. No focal deficits. Absent Achilles reflexes bilaterally (peripheral neuropathy).

LABORATORY DATA
Admission BMP: Na 138 mEq/L, K 5.8 mEq/L (hyperkalemia), Cl 104 mEq/L, HCO₃ 18 mEq/L (metabolic acidosis), BUN 62 mg/dL, Creatinine 3.1 mg/dL (worsened from baseline 1.8–2.0), Glucose 198 mg/dL
eGFR (CKD-EPI): 17 mL/min/1.73m² — acutely worsened, consistent with AKI on CKD
Urine albumin-to-creatinine ratio: 1,480 mg/g — markedly worsened from 680 mg/g six months prior
HbA1c: 8.9% — suboptimally controlled
CBC: WBC 7.8 K/uL, Hemoglobin 9.4 g/dL (anemia of CKD), Hematocrit 28.2%, MCV 82 fL (normocytic), Platelets 222 K/uL
Serum albumin: 2.8 g/dL — hypoalbuminemia, consistent with nephrotic-range proteinuria
Parathyroid hormone (intact iPTH): 182 pg/mL — elevated, consistent with secondary hyperparathyroidism of CKD
25-OH Vitamin D: 14 ng/mL — deficient
Phosphorus: 5.4 mg/dL (hyperphosphatemia)
ECG: Sinus rhythm, PR interval 180 ms, peaked T-waves in precordial leads — concerning for hyperkalemia; repeat ECG after kayexalate showed improvement
Urine sodium: 62 mEq/L (elevated, suggesting intrinsic renal disease rather than prerenal)
Urine protein/creatinine ratio: 4.2 — nephrotic range
Spot urine microscopy: No casts, no RBCs — consistent with diabetic nephropathy rather than glomerulonephritis

Hospital Day 3 BMP: Na 138, K 4.8, BUN 48, Cr 2.4, HCO₃ 20 — improving with NSAID cessation and diuresis
Discharge BMP: Na 139, K 4.6, BUN 40, Cr 2.0, HCO₃ 22 — approaching baseline

IMAGING AND DIAGNOSTICS
Renal Ultrasound (Hospital Day 1): Right kidney 9.8 cm, left kidney 10.1 cm. Bilateral diffusely echogenic kidneys consistent with chronic medical renal disease (prior documented). No hydronephrosis. No renal calculi. No cysts. Normal corticomedullary differentiation preserved though diminished. No focal lesion.
Chest X-Ray (Admission): Mild cardiomegaly. Bilateral pleural effusions, small. Mild pulmonary vascular congestion. No lobar pneumonia.
12-Lead ECG (Admission): Normal sinus rhythm. Peaked T-waves V2–V5 — hyperkalemia pattern. PR interval 188 ms. No ST changes. After treatment on day 2: peaked T-waves resolved.
Echocardiogram (Hospital Day 2): LVEF 58%, preserved. Left ventricular hypertrophy, concentric. Grade II diastolic dysfunction. Mild mitral and tricuspid regurgitation. Estimated RVSP 38 mmHg. No pericardial effusion. Bilateral small pleural effusions confirmed.

HOSPITAL COURSE
Ms. Nguyen was admitted for management of acute-on-chronic kidney disease superimposed on her established diabetic nephropathy with hyperkalemia, hypoalbuminemia, and fluid overload. NSAIDs were immediately discontinued on admission as the most likely precipitant of AKI on CKD given her documented ibuprofen use over the preceding month. All nephrotoxic medications were reviewed and metformin was held pending improvement in creatinine below 1.8 mg/dL.

Hyperkalemia (K 5.8) with ECG changes was managed urgently with calcium gluconate 1g IV for membrane stabilization, sodium bicarbonate 50 mEq IV, regular insulin 10 units IV with dextrose 25g, and patiromer 8.4g orally daily initiated as a long-term potassium binder. The home sodium bicarbonate dose was increased to correct ongoing metabolic acidosis. Potassium decreased to 5.1 by day 2 and 4.6 by discharge, with resolution of ECG changes.

Diuresis was optimized with IV furosemide 80 mg twice daily for the first three days, transitioning to oral furosemide 80 mg twice daily on day 4. A net negative fluid balance of 0.8–1.2 liters daily was achieved. Weight decreased from 98.4 kg to 95.0 kg by discharge. Bilateral pleural effusions reduced significantly on repeat chest imaging.

Nephrology co-managed the patient throughout the admission. Creatinine improved from 3.1 to 2.0 mg/dL with NSAID cessation and appropriate diuresis. The team counseled the patient extensively and firmly about lifetime NSAID avoidance given her CKD stage, the irreversibility of further nephron loss, and the trajectory toward end-stage renal disease. The patient acknowledged her error and agreed to use acetaminophen for pain management going forward. Tramadol at reduced doses was offered as an alternative for breakthrough pain. A frank conversation regarding CKD progression, the anticipated need for renal replacement therapy planning within two to three years, and options for peritoneal vs. hemodialysis vs. renal transplant was initiated.

Vitamin D deficiency was treated with ergocalciferol 50,000 IU weekly for 8 weeks. Phosphate binder calcium carbonate was continued and sevelamer was added given persistent hyperphosphatemia. iPTH management was deferred to outpatient nephrology. Anemia of CKD (Hgb 9.4) was evaluated — ferritin was 280 ng/mL and TSAT 22%, suggesting iron-adequate anemia; nephrology recommended outpatient consideration of erythropoiesis-stimulating agent.

DISCHARGE DIAGNOSES
1. Type 2 diabetes mellitus with diabetic chronic kidney disease — primary diagnosis, NSAID-precipitated acute-on-chronic exacerbation
2. Acute kidney injury superimposed on CKD Stage 3b — creatinine peak 3.1 from baseline 1.8, secondary to NSAID nephrotoxicity
3. Hyperkalemia, resolved — managed with membrane stabilization, redistribution, and patiromer
4. Nephrotic-range proteinuria — worsened, UACR 1,480 mg/g
5. Metabolic acidosis — partially corrected
6. Hypertension, uncontrolled — contributing to CKD progression
7. Anemia of chronic kidney disease — stable
8. Secondary hyperparathyroidism — outpatient management
9. Hyperlipidemia — active comorbidity
10. Obesity — active comorbidity

DISCHARGE CONDITION
Improved but not at baseline. Creatinine 2.0 approaching but not yet at prior baseline of 1.8. Potassium 4.6. Volume status improved with partial resolution of edema. Ambulatory without assistance. Tolerating oral diet.

DISCHARGE MEDICATIONS
1. Furosemide 80 mg orally twice daily — increased from 40 mg daily
2. Patiromer (Veltassa) 8.4g orally daily with food — NEW potassium binder; do not take within 3 hours of other medications
3. Lisinopril 40 mg orally daily — continued; hold if Cr rises above 3.0 and call doctor
4. Amlodipine 10 mg orally daily — continued
5. Sevelamer 800 mg orally three times daily with meals — NEW phosphate binder
6. Calcium carbonate 500 mg orally twice daily with meals (reduced from three times daily)
7. Sodium bicarbonate 650 mg orally three times daily — continued
8. Ergocalciferol 50,000 IU orally weekly — NEW, 8-week course
9. Atorvastatin 40 mg orally nightly — continued
10. Ferrous sulfate 325 mg orally twice daily — continued
11. Glipizide 5 mg orally daily — continued
12. Metformin HELD — resume only when creatinine returns to baseline and nephrologist approves

DISCHARGE INSTRUCTIONS
You were admitted because your kidneys got worse, partly because you were using ibuprofen (a pain reliever that damages kidneys). You must never take ibuprofen, naproxen, aspirin for pain, or any other non-steroidal anti-inflammatory pain medication again — these medications cause serious kidney damage. For pain, use only acetaminophen (Tylenol) up to 2 grams daily unless your doctor says otherwise. Weigh yourself every morning. If you gain more than 2 pounds in one day, call your nephrologist. Take all medications as prescribed. Do not skip your blood pressure pills. Keep all nephrology appointments — your kidneys are being closely monitored and the team is preparing a plan for your future kidney care.

FOLLOW-UP
1. Nephrology (primary): 1 week post-discharge — creatinine recheck, volume status, patiromer adjustment
2. Primary Care / Endocrinology: 2 weeks — HbA1c, metformin restart discussion, diabetes management
3. Ophthalmology: Scheduled in 4 weeks — annual diabetic retinopathy screening
4. CKD Education Class: Enrolled — starts in 3 weeks (RRT planning, dietary counseling, transplant evaluation)""",
    },
    {
        "title": "Hypertensive Urgency — Severe Uncontrolled Hypertension",
        "category": "Internal Medicine / Cardiology",
        "expected_codes": ["I10"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Beverly Okafor, 58F | MRN: 1038402
Admission: 11/14/2025 | Discharge: 11/16/2025 | LOS: 2 days
Attending: Dr. P. Castillo, MD | Service: Internal Medicine

CHIEF COMPLAINT
Severe throbbing headache, blurred vision, and blood pressure 218/124 mmHg on arrival to the emergency department.

HISTORY OF PRESENT ILLNESS
Ms. Okafor is a 58-year-old woman with a 12-year history of essential hypertension who presents with a six-hour history of severe occipital and frontal headache rated 9/10 in intensity, associated with blurred vision bilaterally, mild nausea without vomiting, and general malaise. She reports her headache began suddenly in the early morning hours. She denies any focal neurological deficits, chest pain, shortness of breath, palpitations, diaphoresis, hematuria, or decreased urine output. She denies any recent change in her medications.

On further questioning she discloses that she ran out of amlodipine approximately three weeks ago and did not refill it because she felt well and believed her blood pressure would remain controlled on lisinopril alone. She has been checking her blood pressure at a local pharmacy and notes that values over the past two weeks have been in the range of 170–190 systolic, which she attributed to "white coat" effect. She has no prior history of hypertensive emergency, stroke, or heart attack. She denies any recent high-sodium dietary indiscretion. She has not started any new medications, herbal supplements, or over-the-counter decongestants. She reports no new psychological stressors beyond her usual work demands.

In the emergency department, blood pressure on arrival was 218/124 mmHg in the right arm and 214/118 mmHg in the left arm, confirming severe bilateral hypertension. Heart rate was 88 bpm in sinus rhythm. She was afebrile with oxygen saturation 98% on room air. Fundoscopic examination by the emergency physician revealed bilateral early papilledema without hemorrhage or exudate, raising concern for early hypertensive emergency affecting the optic nerve. Given the presence of papilledema, ophthalmology was urgently consulted and confirmed Grade III hypertensive retinopathy with early disc edema bilaterally. Neurological examination was intact. ECG showed left ventricular hypertrophy by voltage criteria without acute ischemic changes. Head CT without contrast showed no acute intracranial hemorrhage, no ischemic changes. She was admitted for blood pressure lowering, close monitoring for end-organ damage, and medication optimization.

PAST MEDICAL HISTORY
1. Essential (primary) hypertension, 12-year history
2. Hyperlipidemia on rosuvastatin
3. Type 2 diabetes mellitus, diet-controlled
4. Obesity, BMI 32
5. Chronic low back pain, managed conservatively
6. Remote history of gestational hypertension with second pregnancy

PAST SURGICAL HISTORY
Cesarean section x2 (remote). No other surgeries.

MEDICATIONS ON ADMISSION
1. Lisinopril 20 mg orally daily — adherent
2. Amlodipine 10 mg orally daily — not taking for approximately 3 weeks (ran out)
3. Rosuvastatin 20 mg orally nightly — adherent
4. Acetaminophen 500 mg orally as needed for pain — using for headaches
5. Aspirin 81 mg orally daily — adherent

ALLERGIES
Hydrochlorothiazide (hyponatremia requiring hospitalization in 2019). No other known drug allergies.

SOCIAL HISTORY
Elementary school principal. Married, lives with husband in a two-story home. Two adult children. Nonsmoker. Occasional alcohol — one glass of wine on weekends. No illicit drug use. Diet higher in sodium than recommended by history; acknowledges frequent restaurant meals. Exercise limited to walking. Good insurance coverage (commercial PPO). Pharmacy refill reminder system not in place.

FAMILY HISTORY
Mother had severe hypertension and died of hemorrhagic stroke at age 64. Father had hypertension and coronary artery disease. One sibling with hypertension. Maternal aunt with chronic kidney disease attributed to hypertension.

REVIEW OF SYSTEMS
Positive: severe headache (occipital and frontal), blurred vision bilaterally, nausea, malaise, fatigue.
Negative: chest pain, shortness of breath, palpitations, focal neurological deficits (weakness, sensory loss, speech changes, facial droop), diplopia, tinnitus, epistaxis, hematuria, dysuria, flank pain, leg swelling, confusion.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 36.9°C, BP 218/124 mmHg (right arm), 214/118 mmHg (left arm), HR 88 bpm regular, RR 16 breaths/min, SpO2 98% RA, Wt 86 kg, BMI 32
General: Well-nourished obese woman in moderate distress due to headache. Alert and oriented x3. Appropriate affect. Not diaphoretic.
HEENT: Fundoscopy — bilateral Grade III hypertensive retinopathy with arteriolar narrowing, arteriovenous nicking, and bilateral early disc edema confirmed by ophthalmology. No hemorrhage or hard exudates. Papilledema Grade I-II by Frisen scale. Oral mucosa moist. No JVD.
Cardiovascular: Regular rate and rhythm. S1 and S2. S4 gallop at apex. No S3. No murmurs. PMI slightly displaced laterally — consistent with left ventricular hypertrophy.
Pulmonary: Clear to auscultation bilaterally. No wheeze or crackles.
Abdomen: Soft, non-tender, non-distended. No aortic bruit. No renal bruits appreciated.
Extremities: No lower extremity edema. Peripheral pulses 2+ bilaterally. No calf tenderness.
Neurological: Alert, oriented x3. Speech fluent. Cranial nerves II–XII intact. Motor 5/5 all extremities. Sensation intact. Reflexes 2+ symmetric. No Babinski. No asterixis. Gait steady.

LABORATORY DATA
BMP: Na 139 mEq/L, K 4.2 mEq/L, Cl 102 mEq/L, HCO3 24 mEq/L, BUN 18 mg/dL, Creatinine 0.9 mg/dL (baseline), Glucose 128 mg/dL
CBC: WBC 7.8 K/uL, Hemoglobin 13.2 g/dL, Hematocrit 39.4%, Platelets 256 K/uL — normal
Urinalysis: Specific gravity 1.018, trace protein, no RBC, no casts, no nitrites — no significant proteinuria or hematuria; no evidence of hypertensive nephropathy at this evaluation
Urine albumin-to-creatinine ratio: 42 mg/g — mildly elevated, within microalbuminuria range; to be monitored outpatient
Troponin I: <0.02 — negative; no evidence of myocardial injury
BNP: 88 pg/mL — borderline, mildly elevated; no acute decompensated heart failure
Lipid panel: Total cholesterol 204, LDL 118, HDL 52, Triglycerides 170 — suboptimally controlled LDL
HbA1c: 6.4% — diabetes well controlled on diet alone
Thyroid function: TSH 2.1 mIU/L — normal; secondary hypertension from thyroid disease excluded
Plasma metanephrines (fractionated, free): Normal — pheochromocytoma excluded in setting of refractory hypertension

IMAGING AND DIAGNOSTICS
12-Lead ECG: Normal sinus rhythm. LVH by Sokolow-Lyon voltage criteria (SV1 + RV5 = 38 mm). Left axis deviation. No acute ST-T wave changes. QTc 442 ms.
CT Head without contrast: No acute intracranial hemorrhage. No acute ischemic changes. Mild periventricular white matter changes — likely small vessel ischemic disease. No mass. No midline shift.
Chest X-Ray: Mild cardiomegaly. No pulmonary edema. No pleural effusions. No acute cardiopulmonary process.
Renal ultrasound (ordered for secondary hypertension workup, performed day 2): Bilateral kidneys normal in size (right 10.8 cm, left 11.0 cm). No hydronephrosis. No renal artery calcification. Doppler not performed at this visit; deferred to outpatient.

HOSPITAL COURSE
Ms. Okafor was admitted to a monitored bed for blood pressure lowering in the setting of hypertensive urgency with Grade III hypertensive retinopathy and early papilledema. Given the ophthalmology-confirmed papilledema, she was managed as a hypertensive emergency (optic nerve end-organ involvement) despite the absence of neurological deficits.

She was started on IV labetalol for controlled blood pressure reduction — the goal being a 20–25% reduction in mean arterial pressure over the first hour, with gradual further reduction over 24–48 hours to avoid ischemic complications from overly rapid lowering. She received labetalol 20 mg IV over 2 minutes, then 40 mg IV at 10 minutes for persistent hypertension, achieving MAP reduction from 155 to 128 mmHg (approximately 17% reduction) at 1 hour. Blood pressure at 2 hours was 186/104 mmHg — appropriate initial response.

Amlodipine 10 mg orally was resumed on admission night and lisinopril was continued at 20 mg. On hospital day 2 she was transitioned off IV medications to oral antihypertensives with blood pressure monitoring every two hours. Lisinopril was uptitrated to 40 mg given her microalbuminuria and diabetic comorbidity. Blood pressure on day 2 ranged 148–162/88–96 mmHg — appropriate gradual lowering. By discharge she was maintaining blood pressures of 142–154/82–90 mmHg, which was deemed a safe and appropriate target range for the first week post-urgency (full target of <130/80 to be achieved over two to four weeks outpatient).

Ophthalmology confirmed papilledema had not progressed between hospital days 1 and 2. No new visual field defects on formal testing. Repeat fundoscopy scheduled outpatient at one week. Neurology was not consulted given intact neurological examination and head CT showing only chronic white matter changes.

Pharmacy counseled the patient on the critical importance of medication adherence, auto-refill enrollment, and the consequences of antihypertensive lapse. A 90-day mail-order supply of amlodipine was arranged prior to discharge. She was given a home blood pressure cuff and instructed on proper technique and a daily log. Dietary counseling was provided focusing on the DASH diet and sodium restriction to less than 2 grams daily.

DISCHARGE DIAGNOSES
1. Essential (primary) hypertension, severe uncontrolled — hypertensive urgency/emergency with Grade III hypertensive retinopathy and papilledema; primary admission diagnosis
2. Medication non-adherence (amlodipine lapse x3 weeks) — precipitating factor
3. Left ventricular hypertrophy — hypertensive end-organ effect, on ECG
4. Microalbuminuria — early hypertensive nephropathy, outpatient follow-up required
5. Type 2 diabetes mellitus, diet-controlled — active comorbidity
6. Hyperlipidemia, suboptimally controlled — active comorbidity
7. Obesity — active comorbidity

DISCHARGE CONDITION
Stable. Blood pressure 144/86 mmHg on discharge. No headache. Vision returned to baseline. Neurologically intact. Tolerating all oral medications.

DISCHARGE MEDICATIONS
1. Amlodipine 10 mg orally daily — RESUMED; auto-refill enrolled; do not skip doses
2. Lisinopril 40 mg orally daily — INCREASED from 20 mg
3. Rosuvastatin 20 mg orally nightly — unchanged
4. Aspirin 81 mg orally daily — unchanged
5. Acetaminophen 500 mg orally as needed (max 2g/day) — for headache if needed

DISCHARGE INSTRUCTIONS
Your blood pressure was dangerously high because you ran out of one of your blood pressure medications (amlodipine). Never stop blood pressure medications without talking to your doctor. Check your blood pressure at home every morning and evening and write it down. Target: below 140/90 for the first week, then below 130/80 long-term. If your blood pressure exceeds 180/110 or you develop severe headache, vision loss, confusion, weakness, or chest pain, go to the emergency department immediately. Follow the DASH diet — limit sodium to 2 grams (about one teaspoon of salt) daily. Avoid canned foods, deli meats, restaurant meals, and adding salt at the table. Return to ophthalmology in one week to check your eyes.

FOLLOW-UP
1. Internal Medicine (Dr. Castillo): 1 week post-discharge — blood pressure check, labs (BMP, urine ACR)
2. Ophthalmology: 1 week post-discharge — repeat fundoscopy for papilledema resolution
3. Cardiology: 4 weeks — LVH assessment, echocardiogram
4. Pharmacy: Auto-refill enrolled for all medications""",
    },
    {
        "title": "Hypertensive Heart Disease with Heart Failure",
        "category": "Cardiology / Internal Medicine",
        "expected_codes": ["I110"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Gerald Russo, 71M | MRN: 2847103
Admission: 10/09/2025 | Discharge: 10/14/2025 | LOS: 5 days
Attending: Dr. B. Singh, MD | Service: Cardiology

CHIEF COMPLAINT
Progressive shortness of breath, lower extremity edema, and fatigue over three weeks.

HISTORY OF PRESENT ILLNESS
Mr. Russo is a 71-year-old man with a 20-year history of essential hypertension and known hypertensive heart disease who presents with a three-week history of progressive dyspnea on exertion, bilateral ankle and leg swelling, and fatigue severe enough to limit his activity to basic household tasks. He reports he was previously able to walk one mile on flat terrain without difficulty but is now short of breath after walking from his bedroom to the kitchen. He sleeps with two pillows at night and denies frank orthopnea at rest. He endorses mild paroxysmal nocturnal dyspnea on two occasions in the past week, waking from sleep with breathlessness that resolved with sitting upright after five to ten minutes.

He has been closely followed by his cardiologist for hypertensive heart disease with concentric left ventricular hypertrophy documented on echocardiogram eighteen months ago. His prior echocardiogram at that time showed preserved ejection fraction of 60% with Grade II diastolic dysfunction and mildly elevated filling pressures, E/e' ratio of 14. His blood pressure has been modestly controlled with two antihypertensives but has been running higher than usual on home monitoring over the past four weeks — values ranging 158–176/90–102 mmHg versus his usual target of 125–135/80 mmHg. He attributes the blood pressure elevation to increased stress related to a family matter.

He reports a weight gain of approximately 6 pounds over the past three weeks. He has been adherent to all medications. He denies chest pain, palpitations, syncope, fever, chills, or productive cough. He has no known history of coronary artery disease, prior myocardial infarction, or valvular disease. He denies recent contrast exposure or NSAID use.

In the emergency department, blood pressure was 168/98 mmHg, heart rate 94 bpm, respiratory rate 20, and oxygen saturation 91% on room air improving to 96% on 2L nasal cannula. BNP was 1,242 pg/mL. Chest radiograph demonstrated cardiomegaly with pulmonary vascular congestion and bilateral pleural effusions. He was admitted for IV diuresis and blood pressure optimization.

PAST MEDICAL HISTORY
1. Essential hypertension, 20-year history; hypertensive heart disease diagnosed 4 years ago
2. Concentric left ventricular hypertrophy on echocardiography
3. Diastolic dysfunction Grade II, documented 18 months ago
4. Hyperlipidemia on atorvastatin
5. Type 2 diabetes mellitus on metformin
6. Chronic kidney disease Stage 2 (eGFR 68), attributed to hypertensive nephrosclerosis
7. Obstructive sleep apnea on CPAP, moderately adherent
8. Gout, managed with allopurinol

PAST SURGICAL HISTORY
Appendectomy age 42. Right inguinal hernia repair age 58.

MEDICATIONS ON ADMISSION
1. Lisinopril 40 mg orally daily
2. Amlodipine 10 mg orally daily
3. Furosemide 20 mg orally daily
4. Metformin 1000 mg orally twice daily
5. Atorvastatin 40 mg orally nightly
6. Allopurinol 300 mg orally daily
7. Aspirin 81 mg orally daily
8. CPAP — used 4–5 nights per week

ALLERGIES
Sulfonamides (rash). No other known drug allergies.

SOCIAL HISTORY
Retired plumber. Married, lives with wife in a one-story home. Three adult children. Former smoker — 30 pack-year history, quit 18 years ago. Occasional alcohol — two to three beers per week. No illicit drug use. Diet higher in sodium, frequently eating canned soups and processed meats by wife's report. Previously active, now limited by dyspnea. Medicare with supplemental coverage.

FAMILY HISTORY
Father had hypertension and died of heart failure at age 74. Mother had stroke at age 70. Two siblings with hypertension. One sibling with diabetes.

REVIEW OF SYSTEMS
Positive: progressive dyspnea on exertion, paroxysmal nocturnal dyspnea x2 episodes, two-pillow orthopnea, bilateral lower extremity edema, 6-lb weight gain over 3 weeks, fatigue, reduced functional capacity.
Negative: chest pain, palpitations, syncope, fever, chills, cough, hemoptysis, nausea, vomiting, abdominal pain, hematuria, dysuria, focal neurological deficits.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 36.8°C, BP 168/98 mmHg, HR 94 bpm regular, RR 20 breaths/min, SpO2 91% RA → 96% on 2L NC, Wt 89.6 kg (dry weight estimate 83 kg)
General: Obese older man in mild respiratory distress at rest, able to speak in full sentences. Alert and oriented x3.
HEENT: JVD estimated 11 cm at 45 degrees. No lymphadenopathy. No thyromegaly.
Cardiovascular: Regular rate and rhythm. S1 and S2. S4 gallop at apex — consistent with reduced left ventricular compliance. No S3. No murmurs. PMI laterally displaced.
Pulmonary: Dullness to percussion bilateral bases to mid-scapulae. Bibasilar crackles to mid-lung fields. No wheeze.
Abdomen: Soft, mildly distended. Liver edge palpable 2 cm below right costal margin — mild hepatomegaly consistent with venous congestion. No ascites. Non-tender.
Extremities: 2+ pitting edema bilateral lower extremities to mid-shin. Skin warm, intact. No ulcers. Peripheral pulses 2+.
Neurological: Alert and oriented x3. No focal deficits. Motor strength 5/5. Cranial nerves intact.

LABORATORY DATA
BMP: Na 138 mEq/L, K 4.4 mEq/L, Cl 101 mEq/L, HCO3 25 mEq/L, BUN 26 mg/dL, Creatinine 1.4 mg/dL (baseline 1.1–1.2), Glucose 164 mg/dL
CBC: WBC 8.6 K/uL, Hemoglobin 12.8 g/dL, Hematocrit 38.4%, Platelets 210 K/uL
BNP: 1,242 pg/mL — markedly elevated
Troponin I x2: <0.02 — negative; no acute myocardial injury
LFTs: AST 48, ALT 38, Alk Phos 122, Total bili 1.6 — mildly elevated, consistent with hepatic venous congestion
HbA1c: 7.6%
Magnesium: 1.9 mg/dL
Lipid panel: LDL 82, HDL 38, Total cholesterol 166, TG 184
Urine albumin-to-creatinine ratio: 88 mg/g — microalbuminuria, consistent with hypertensive nephropathy

Day 3 BMP: Na 139, K 3.9, BUN 20, Cr 1.2, Glucose 148 — improving renal function with optimized diuresis
Discharge BMP: Na 140, K 4.1, BUN 18, Cr 1.1, Glucose 138 — at baseline

IMAGING AND DIAGNOSTICS
Chest X-Ray (Admission): Cardiomegaly (CTR 0.58). Bilateral pleural effusions, right greater than left. Pulmonary vascular congestion with upper lobe diversion. Kerley B lines. No lobar consolidation.
Chest X-Ray (Day 4): Interval reduction in bilateral pleural effusions. Improved pulmonary vascular congestion. Persistent cardiomegaly.
12-Lead ECG: Normal sinus rhythm at 94 bpm. LVH by voltage criteria. Left axis deviation. No acute ST-T wave changes. QTc 448 ms. No Q-waves.
Echocardiogram (Hospital Day 2): LVEF 57%, preserved. Severe concentric left ventricular hypertrophy (LV wall thickness 1.4 cm posterior wall, 1.5 cm septum). Grade II-III diastolic dysfunction. E/e' ratio 19, elevated left ventricular filling pressure. LA volume index 44 mL/m², moderately enlarged. Mild mitral regurgitation. Estimated RVSP 42 mmHg. IVC 2.4 cm with reduced respiratory variation — elevated RA pressure. No wall motion abnormality. No pericardial effusion.

HOSPITAL COURSE
Mr. Russo was admitted for management of acute decompensated heart failure in the setting of hypertensive heart disease with preserved ejection fraction and worsening diastolic dysfunction. He was placed on cardiac telemetry, daily weights, strict input/output monitoring, and a 2-gram sodium, 1.5-liter fluid-restricted diet.

IV furosemide was initiated at 80 mg twice daily. He diuresed 2.4 liters net negative on day 1 with substantial improvement in dyspnea. Oxygen requirements decreased from 2L to room air by the morning of day 2. Electrolytes were monitored every 12 hours during active IV diuresis; potassium was supplemented with oral KCl 20 mEq twice daily when trending to 3.8 mEq/L on day 1 and remained stable thereafter.

Blood pressure optimization was prioritized as a parallel intervention given the central role of hypertension in his decompensation. Carvedilol 6.25 mg twice daily was added on hospital day 2 — a beta-blocker with alpha-blockade providing both rate control and afterload reduction favorable for diastolic dysfunction. Amlodipine was continued at 10 mg. Lisinopril was continued at 40 mg and the dose held on day 3 when creatinine transiently peaked at 1.6 mg/dL, then resumed once creatinine improved. Blood pressure by day 4 ranged 132–148/78–88 mmHg — approaching target.

He was transitioned from IV to oral furosemide 80 mg twice daily on day 4. He maintained net negative fluid balance with continued improvement in weight (84.8 kg by discharge) and edema. By hospital day 5, bilateral edema was reduced from 2+ to trace, bibasilar crackles resolved, and he was ambulating the hallway on room air without dyspnea. He was able to climb one flight of stairs with the physical therapist without supplemental oxygen, returning to near his prior functional baseline.

Sleep medicine was consulted; CPAP adherence was reinforced, as untreated OSA drives nocturnal hypertension and sympathetic activation — both major contributors to diastolic dysfunction in hypertensive heart disease. A CPAP compliance download showed only 60% adherence over the past month. He was counseled on the cardiovascular consequences of non-adherence.

Cardiology team arranged outpatient follow-up in one week with repeat BMP and BNP. Patient and wife received heart failure education including daily weight log, sodium restriction, fluid limits, action plan for weight gain thresholds, and medication adherence.

DISCHARGE DIAGNOSES
1. Hypertensive heart disease with heart failure — acute decompensated diastolic heart failure, primary admission diagnosis
2. Essential hypertension, suboptimally controlled — primary precipitant
3. Diastolic dysfunction, Grade II-III — established, worsened from prior
4. Acute kidney injury, mild — resolved; peak Cr 1.6, baseline at discharge
5. Type 2 diabetes mellitus — active comorbidity
6. Chronic kidney disease Stage 2 — active comorbidity, microalbuminuria present
7. Hyperlipidemia — active comorbidity
8. Obstructive sleep apnea, partially treated — contributing comorbidity
9. Gout — active comorbidity, stable

DISCHARGE CONDITION
Stable. Ambulating on room air without dyspnea. Weight 84.8 kg (down from 89.6 kg on admission). Trace bilateral lower extremity edema. Blood pressure 140/82 mmHg on discharge.

DISCHARGE MEDICATIONS
1. Furosemide 80 mg orally twice daily — INCREASED from 20 mg daily
2. Carvedilol 6.25 mg orally twice daily — NEW; take with food; do not stop abruptly
3. Lisinopril 40 mg orally daily — unchanged
4. Amlodipine 10 mg orally daily — unchanged
5. Potassium chloride 20 mEq orally twice daily — NEW; monitor levels
6. Metformin 1000 mg orally twice daily — unchanged
7. Atorvastatin 40 mg orally nightly — unchanged
8. Allopurinol 300 mg orally daily — unchanged
9. Aspirin 81 mg orally daily — unchanged

DISCHARGE INSTRUCTIONS
Your heart failure flare was caused by high blood pressure that has been difficult to control, leading to fluid buildup in your lungs and legs. Weigh yourself every morning before eating and after urinating. Write it down. If you gain 2 or more pounds in one day or 5 or more pounds in one week, call your cardiologist immediately. Limit sodium to 2 grams daily and fluids to 6 cups daily. Take all medications exactly as prescribed — especially the new blood pressure pill (carvedilol) and the higher dose water pill (furosemide). Use your CPAP every night — poor sleep worsens your heart condition. If you develop severe shortness of breath, call 911.

FOLLOW-UP
1. Cardiology (Dr. Singh): 1 week — weight, BP, labs (BMP, BNP), echocardiogram review
2. Primary Care: 2 weeks — diabetes, CKD monitoring
3. Sleep Medicine: 4 weeks — CPAP adherence review
4. Dietary counseling: Arranged, within 2 weeks""",
    },
    {
        "title": "Atherosclerotic Heart Disease — Elective Percutaneous Coronary Intervention",
        "category": "Interventional Cardiology",
        "expected_codes": ["I2510"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Thomas Gallagher, 66M | MRN: 3920481
Admission: 09/22/2025 | Discharge: 09/25/2025 | LOS: 3 days
Attending: Dr. C. Reyes, MD | Service: Interventional Cardiology

CHIEF COMPLAINT
Elective admission for cardiac catheterization and percutaneous coronary intervention following positive nuclear stress test for stable angina workup.

HISTORY OF PRESENT ILLNESS
Mr. Gallagher is a 66-year-old man with a long-standing history of essential hypertension, hyperlipidemia, and type 2 diabetes mellitus who was referred to interventional cardiology for elective catheterization following a nuclear myocardial perfusion imaging study that demonstrated a moderate reversible perfusion defect in the inferior and inferolateral walls (inferior territory, approximately 15% of left ventricular myocardium), consistent with significant ischemia in the right coronary artery or left circumflex territory. He reports a three-month history of exertional chest pressure — described as a dull, substernal heaviness rated 4–5/10 in severity — that consistently occurs when climbing two flights of stairs or walking uphill at a brisk pace. The symptoms reliably resolve within three to five minutes of rest. He denies symptoms at rest, with emotional stress alone, or at low levels of exertion. He has not experienced chest pain at night or with meals. He has never had a myocardial infarction by history.

He was evaluated outpatient by cardiology two months ago after he mentioned his exertional chest discomfort to his primary care physician during an annual visit. A treadmill nuclear stress test using standard Bruce protocol was performed. He exercised for 7 minutes 40 seconds (achieving 9.4 METs) and stopped due to chest pressure and leg fatigue. ECG showed 1.5 mm horizontal ST depression in leads II, III, aVF during exercise, with normalization at 6 minutes of recovery. Nuclear perfusion imaging demonstrated the inferior/inferolateral reversible defect as noted above, with preserved LVEF of 62% on gated imaging. The findings were consistent with stress-induced ischemia in the inferior distribution, most likely right coronary artery. He was started on aspirin 81 mg and sublingual nitroglycerin as needed, and referred for elective catheterization.

He has no history of prior cardiac catheterization, angioplasty, stenting, or bypass surgery. He denies contrast allergy. Creatinine is 1.0 mg/dL baseline. He has been on dual antiplatelet therapy (aspirin) preoperatively and was started on clopidogrel 600 mg loading dose the morning prior to admission per the cath lab pre-procedure protocol.

PAST MEDICAL HISTORY
1. Essential hypertension, 15-year history
2. Hyperlipidemia, previously on pravastatin, upgraded to rosuvastatin 6 months ago
3. Type 2 diabetes mellitus on metformin and empagliflozin
4. Atherosclerotic cardiovascular disease risk — ASCVD 10-year risk 28% by pooled cohort equation
5. Obesity, BMI 30
6. Peripheral arterial disease, mild — ABI 0.82 right lower extremity, bilateral claudication symptoms on long distance walking
7. Former tobacco use

PAST SURGICAL HISTORY
Appendectomy age 32. Knee arthroscopy age 55. No prior cardiac procedures.

MEDICATIONS ON ADMISSION
1. Rosuvastatin 40 mg orally nightly — high-intensity statin
2. Metformin 1000 mg orally twice daily — held morning of procedure for contrast
3. Empagliflozin 10 mg orally daily — held 48 hours prior per pre-procedure protocol
4. Lisinopril 20 mg orally daily
5. Metoprolol succinate 50 mg orally daily
6. Aspirin 81 mg orally daily — continued
7. Clopidogrel 600 mg loading dose given morning of admission (pre-load for PCI)
8. Sublingual nitroglycerin 0.4 mg as needed — prescribed at outpatient visit, used twice prior to admission

ALLERGIES
No known drug allergies. No contrast allergy. Iodine contrast safe; pre-medication not required.

SOCIAL HISTORY
Retired fire captain. Married, lives with wife. Two adult children. Former smoker — 25 pack-year history, quit 14 years ago. Moderate alcohol — three to four drinks per week, wine primarily. No illicit drug use. Moderate aerobic activity until symptoms began. Medicare and supplemental insurance.

FAMILY HISTORY
Father had coronary artery disease, first MI at age 61, died of second MI at age 67. Mother had hypertension and peripheral vascular disease. One sibling with CAD requiring stenting at age 60.

REVIEW OF SYSTEMS
Positive: exertional chest pressure with two flights of stairs or brisk uphill walking (3-month history); relieved by rest within 3–5 minutes; claudication bilateral calves on long-distance walking.
Negative: chest pain at rest, nocturnal chest pain, radiation to arm or jaw, diaphoresis, palpitations, syncope, dyspnea at rest or with mild exertion, lower extremity edema, orthopnea.

PHYSICAL EXAMINATION (PRE-PROCEDURE, DAY 1)
Vital Signs: Temp 36.8°C, BP 138/82 mmHg, HR 64 bpm regular, RR 14 breaths/min, SpO2 98% RA, Wt 91 kg
General: Well-nourished man in no acute distress. Alert and oriented x3.
HEENT: No carotid bruits bilaterally (auscultated). No JVD. No lymphadenopathy.
Cardiovascular: Regular rate and rhythm. S1 and S2. No murmurs. No S3 or S4. PMI non-displaced. Peripheral pulses 2+ all extremities. Right femoral pulse 2+ — planned arterial access site.
Pulmonary: Clear to auscultation bilaterally. No adventitious sounds.
Abdomen: Soft, non-tender, non-distended. No aortic bruit. No organomegaly.
Extremities: Mild muscle wasting bilateral calves. No lower extremity edema. Bilateral dorsalis pedis and posterior tibial pulses present but diminished on the right (ABI-consistent). No skin ulceration.
Neurological: Alert and oriented x3. No focal deficits.

LABORATORY DATA
Pre-procedure BMP: Na 140, K 4.1, Cl 103, HCO3 25, BUN 16, Cr 1.0, Glucose 142 — normal renal function; metformin held
CBC: WBC 7.6, Hgb 14.2, Hct 42.4%, Plt 188 — normal
Coagulation: PT/INR 1.0, aPTT 27 s — normal
HbA1c: 7.2%
Lipid panel: LDL 68 (on rosuvastatin 40 mg — at LDL target <70 mg/dL for ASCVD), HDL 40, Total 152, TG 220
Troponin I (baseline, pre-procedure): <0.02 — negative
Post-procedure Troponin I (6h): 0.18 ng/mL — mild peri-procedural troponin elevation; Type 4a MI threshold considered; no clinical evidence of abrupt vessel closure; CK-MB ratio not meeting criteria for periprocedural infarction

Post-procedure BMP (Day 2): Cr 1.1 — mild contrast nephropathy not significant; hydration maintained

IMAGING AND DIAGNOSTICS
Nuclear Stress Test (Outpatient, 8 weeks prior): Moderate reversible perfusion defect inferior/inferolateral walls, approximately 15% LV myocardium at risk. LVEF 62% on gated imaging. Consistent with RCA or LCx territory ischemia.
Coronary Angiography (Hospital Day 1): Left main — no significant disease. LAD — 30% proximal stenosis, non-obstructive. LCx — dominant vessel, 40% mid-vessel irregularities, non-obstructive. RCA — non-dominant; 85% stenosis mid-RCA with TIMI 2 flow; 60% distal RCA stenosis. Conclusion: Culprit lesion mid-RCA 85% stenosis consistent with inferior nuclear perfusion defect.
PCI Procedure (Hospital Day 1): Femoral arterial access, right groin. Heparin anticoagulation per weight-based protocol (ACT target 250–300 s). Mid-RCA 85% lesion pre-dilated with 3.0 x 15 mm balloon. Drug-eluting stent (Xience everolimus-eluting, 3.5 x 28 mm) deployed at 14 atm — excellent angiographic result, 0% residual stenosis, TIMI 3 flow post-stent. No dissection. No perforation. No slow flow. Distal RCA 60% lesion — assessed with FFR (0.84), hemodynamically non-significant; medical management elected for distal lesion. Total contrast volume 124 mL. Access site closed with Angioseal closure device.
Echocardiogram (Hospital Day 2, post-PCI): LVEF 63%, preserved. No wall motion abnormality. No pericardial effusion. No significant valvular disease. Grade I diastolic dysfunction.

HOSPITAL COURSE
Mr. Gallagher underwent uncomplicated elective cardiac catheterization with PCI to the mid-RCA on hospital day 1. He tolerated the procedure well without hemodynamic instability. Post-procedure, he was maintained on a flat-bed rest protocol for four hours with right groin check every 30 minutes; no hematoma or vascular complication was noted. The femoral access site closed adequately with the Angioseal device. He was ambulatory by four hours post-procedure without groin symptoms.

Dual antiplatelet therapy was initiated with aspirin 81 mg daily (continued from pre-admission) plus clopidogrel 75 mg daily following the 600 mg loading dose — minimum 12 months of DAPT planned given DES placement. He was counseled explicitly not to stop either antiplatelet agent without first contacting cardiology, particularly in the first 12 months, due to the risk of in-stent thrombosis. The importance of this instruction was reinforced in written form.

Troponin elevation of 0.18 at six hours was noted — this was reviewed by the interventional cardiology team and determined to be a minor peri-procedural rise below the threshold for Type 4a periprocedural MI; no abrupt vessel closure was identified on post-procedure angiography, TIMI 3 flow was maintained throughout, and no clinical symptoms developed post-procedure. Troponin trended down at 12 hours (0.12) and at 24 hours (0.06).

Metformin was restarted on post-procedure day 2 after confirmation that creatinine had not risen significantly (peak 1.1 mg/dL). Empagliflozin was restarted on discharge. The high-intensity statin (rosuvastatin 40 mg) was maintained given LDL at 68 mg/dL meeting secondary prevention targets. Metoprolol succinate was continued for rate control and post-PCI benefit. Lisinopril was continued for blood pressure and diabetes renoprotection.

Cardiac rehabilitation referral was placed for 8–12 weeks post-discharge. He was instructed to avoid strenuous exertion for one week, avoid lifting over ten pounds for one week (femoral site healing), and resume graduated walking by week two. He may drive in 24 hours.

DISCHARGE DIAGNOSES
1. Atherosclerotic heart disease of native coronary artery without angina pectoris — stable exertional angina; RCA 85% stenosis, primary diagnosis
2. Successful PCI with drug-eluting stent to mid-RCA — complete revascularization of culprit lesion; distal RCA 60% managed medically (FFR-negative)
3. Minor peri-procedural troponin elevation — Type 4a MI not meeting criteria; clinically insignificant
4. Essential hypertension — active comorbidity
5. Hyperlipidemia, controlled on high-intensity statin — active comorbidity
6. Type 2 diabetes mellitus — active comorbidity
7. Peripheral arterial disease, mild — active comorbidity
8. Obesity — active comorbidity

DISCHARGE CONDITION
Stable. Access site intact without hematoma. No chest pain or groin symptoms. Hemodynamically stable on discharge. Tolerating dual antiplatelet therapy and all medications.

DISCHARGE MEDICATIONS
1. Aspirin 81 mg orally daily — CRITICAL: do not stop; lifelong therapy; minimum 12 months DAPT required
2. Clopidogrel 75 mg orally daily — CRITICAL: do not stop for 12 months without cardiology guidance; stent thrombosis risk
3. Rosuvastatin 40 mg orally nightly — high-intensity statin; continue long-term
4. Metoprolol succinate 50 mg orally daily — continued
5. Lisinopril 20 mg orally daily — continued
6. Metformin 1000 mg orally twice daily — RESUMED; hold if contrast procedure planned in future
7. Empagliflozin 10 mg orally daily — RESUMED (held 48h pre-procedure)
8. Sublingual nitroglycerin 0.4 mg as needed — may still carry; use if chest pressure returns; call 911 if no relief with 3 doses

DISCHARGE INSTRUCTIONS
You had a blocked artery in your heart (right coronary artery) that was causing your chest pressure on exertion. We placed a small metal mesh tube (stent) to open the blockage. The stent works well, but you MUST take BOTH blood thinners (aspirin and clopidogrel) every day for at least 12 months — stopping them early can cause the stent to clot, which is a heart attack. Do not have any non-emergency procedures or surgeries without first telling your cardiologist that you have a coronary stent. Return to the ER if you develop chest pain at rest, shortness of breath, or groin bleeding. Restart normal activities gradually over 1–2 weeks.

FOLLOW-UP
1. Interventional Cardiology (Dr. Reyes): 1 week post-discharge — wound check, DAPT review
2. Cardiology (outpatient): 4–6 weeks — stress test or imaging not routinely needed; symptoms review
3. Cardiac Rehabilitation: Referral placed; begins within 4–6 weeks
4. Primary Care: 2 weeks — diabetes, hypertension, cholesterol monitoring""",
    },
    {
        "title": "Paroxysmal Atrial Fibrillation — Symptomatic Episode with Cardioversion",
        "category": "Cardiology / Electrophysiology",
        "expected_codes": ["I480"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Ruth Chambers, 64F | MRN: 4510932
Admission: 10/15/2025 | Discharge: 10/17/2025 | LOS: 2 days
Attending: Dr. K. Chen, MD | Service: Cardiology / Electrophysiology

CHIEF COMPLAINT
Sudden onset palpitations, lightheadedness, and shortness of breath for five hours; confirmed paroxysmal atrial fibrillation with rapid ventricular response on arrival ECG.

HISTORY OF PRESENT ILLNESS
Ms. Chambers is a 64-year-old woman with a known three-year history of paroxysmal atrial fibrillation currently managed with flecainide and apixaban who presents with a five-hour episode of palpitations, lightheadedness, and mild exertional dyspnea. She describes the onset as sudden, occurring while she was gardening. She did not take an additional dose of her pill-in-pocket flecainide because she ran out of the extra supply two weeks ago and had not yet refilled it. She denies chest pain, presyncope, or syncope. She has no history of structural heart disease. Her last documented AFib episode was approximately 8 months ago, which self-terminated within 6 hours on pill-in-pocket flecainide 200 mg.

She has been on chronic apixaban anticoagulation for 18 months, with consistent adherence. Her CHA₂DS₂-VASc score is 3 (age 64: 0, female sex: 1, hypertension: 1, prior stroke/TIA: 0, diabetes: 1, HF: 0, vascular disease: 0). Her last echocardiogram 14 months ago demonstrated preserved LVEF of 64% with normal chamber dimensions. No prior cardioversion on record; all prior episodes terminated spontaneously or with pill-in-pocket therapy.

On arrival ECG, she was in atrial fibrillation with rapid ventricular response at 134 bpm. Blood pressure was 132/78 mmHg. She was hemodynamically stable. She was given IV metoprolol 5 mg x2 with rate reduction to 92 bpm over 30 minutes. Given persistent symptomatic AFib, her anticoagulation was confirmed as therapeutic (she took her last apixaban dose 8 hours ago, within dosing interval), and electrical cardioversion was offered after informed consent with goal of rhythm restoration. She elected to proceed with cardioversion.

PAST MEDICAL HISTORY
1. Paroxysmal atrial fibrillation, known 3-year history; 3 documented episodes including this admission
2. Essential hypertension on amlodipine
3. Type 2 diabetes mellitus on metformin
4. Hyperlipidemia on atorvastatin
5. Hypothyroidism on levothyroxine, stable
6. No structural heart disease; LVEF normal on most recent echo

PAST SURGICAL HISTORY
Hysterectomy for fibroids, age 51. Bilateral cataract surgery. No cardiac procedures.

MEDICATIONS ON ADMISSION
1. Flecainide 100 mg orally twice daily — scheduled maintenance dose; pill-in-pocket 200 mg supply depleted
2. Apixaban 5 mg orally twice daily — adherent; last dose 8 hours prior to admission
3. Amlodipine 10 mg orally daily
4. Metoprolol succinate 25 mg orally daily — for rate control; home
5. Metformin 500 mg orally twice daily
6. Atorvastatin 20 mg orally nightly
7. Levothyroxine 88 mcg orally daily on empty stomach

ALLERGIES
Amiodarone (hepatotoxicity — documented on prior admission). Penicillin (rash, childhood).

SOCIAL HISTORY
Retired schoolteacher. Lives alone in a condo. Two adult daughters who live nearby and are closely involved. Nonsmoker. Rare alcohol — one to two glasses of wine per month. No illicit drug use. Active lifestyle; gardening, yoga, walking 3–4 miles per day. Commercial insurance through retirement benefit. Compliant with follow-up historically.

FAMILY HISTORY
Mother had atrial fibrillation in her late 60s. Father had hypertension and died of heart failure. No family history of sudden cardiac death or channelopathy.

REVIEW OF SYSTEMS
Positive: palpitations (sudden onset, 5 hours duration), mild lightheadedness, exertional dyspnea with activity (resolved with sitting).
Negative: chest pain, chest pressure, radiation to arm or jaw, syncope, near-syncope, fever, chills, cough, lower extremity edema, orthopnea, neurological symptoms.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 36.8°C, BP 132/78 mmHg, HR 134 bpm irregularly irregular, RR 16 breaths/min, SpO2 98% RA, Wt 68 kg
General: Well-appearing woman in mild distress due to palpitations. Alert and oriented x3.
HEENT: No JVD. No thyromegaly or nodule. No lymphadenopathy.
Cardiovascular: Irregularly irregular rhythm, rate 134. No murmurs, rubs, or gallops. PMI non-displaced. Peripheral pulses present and irregular.
Pulmonary: Clear bilaterally. No crackles, wheeze, or rhonchi.
Abdomen: Soft, non-tender, non-distended. No organomegaly.
Extremities: No lower extremity edema. Peripheral pulses 2+.
Neurological: Alert and oriented x3. No focal neurological deficits. Speech fluent. Cranial nerves intact. Motor 5/5 all extremities.

LABORATORY DATA
BMP: Na 140, K 4.2, Cl 104, HCO3 25, BUN 14, Cr 0.8, Glucose 118 — normal
CBC: WBC 7.2, Hgb 13.6, Hct 40.8%, Plt 234 — normal
Troponin I x2 (baseline and 4h): <0.02 — negative
TSH: 1.6 mIU/L — normal; hyperthyroidism excluded as precipitant
Magnesium: 2.0 mg/dL — normal
Coagulation: INR 1.0 (apixaban does not affect INR reliably; used for baseline)
Urine toxicology: Negative
HbA1c: 7.0%

IMAGING AND DIAGNOSTICS
12-Lead ECG (Admission): Atrial fibrillation with rapid ventricular response 134 bpm. No P waves. Irregularly irregular rhythm. No delta waves. QTc 420 ms. No ST-T wave changes.
Post-Cardioversion ECG (Hospital Day 1): Normal sinus rhythm at 68 bpm. PR interval 164 ms. Normal axis. No ST-T changes. QTc 432 ms.
Chest X-Ray: No acute cardiopulmonary process. Normal heart size. No pulmonary edema. No pleural effusions.
Transthoracic Echocardiogram (Hospital Day 2): LVEF 64%, preserved. Normal LV size and wall thickness. LA diameter 3.8 cm — mildly enlarged. No intracardiac thrombus on transthoracic view. No significant valvular disease. Grade I diastolic dysfunction. No pericardial effusion.

HOSPITAL COURSE
Ms. Chambers was admitted to the cardiology telemetry unit. Rate control was achieved with IV metoprolol as described, with rate reducing to 92 bpm. Given her adherence to apixaban (confirmed last dose within therapeutic window and no missed doses by pill log review), the electrophysiology team agreed to proceed with electrical cardioversion on hospital day 1 without transesophageal echocardiogram to rule out left atrial appendage thrombus — consistent with current guidelines for AFib duration less than 48 hours on adequate anticoagulation.

Informed consent was obtained. She was administered propofol 80 mg IV for brief conscious sedation by the cardiology proceduralist. External biphasic cardioversion was performed at 200J, achieving immediate restoration of normal sinus rhythm. Post-shock ECG confirmed NSR at 68 bpm. She recovered from sedation without complication. Blood pressure post-cardioversion was 128/74 mmHg.

She was monitored on telemetry for 18 hours post-cardioversion without AFib recurrence. She was maintained on her scheduled flecainide 100 mg twice daily throughout. Her pill-in-pocket flecainide 200 mg supply was replenished (new prescription provided). Metoprolol succinate was continued. Apixaban was continued at 5 mg twice daily — anticoagulation should be maintained for at least four weeks post-cardioversion regardless of apparent sinus rhythm maintenance (standard post-cardioversion anticoagulation), and indefinitely thereafter given her CHA₂DS₂-VASc score of 3.

The electrophysiology team discussed the possibility of catheter ablation as a long-term rhythm control strategy given her relatively young age, active lifestyle, and preference to remain in sinus rhythm. She was receptive and agreed to an outpatient consultation for ablation planning. The risks and benefits, including recurrence rates with flecainide alone vs. ablation, were reviewed.

She was discharged in sinus rhythm on hospital day 2 with close electrophysiology follow-up in two weeks.

DISCHARGE DIAGNOSES
1. Paroxysmal atrial fibrillation — symptomatic episode with rapid ventricular response; successfully cardioverted to sinus rhythm; primary admission diagnosis
2. Essential hypertension — active comorbidity, contributing AF substrate
3. Type 2 diabetes mellitus — active comorbidity
4. Hypothyroidism, stable on levothyroxine — active comorbidity
5. Hyperlipidemia — active comorbidity
6. Pill-in-pocket flecainide supply depleted — contributing factor to failure of outpatient management

DISCHARGE CONDITION
Stable. Normal sinus rhythm on telemetry. HR 68 bpm. No palpitations. No symptoms. Tolerating all medications.

DISCHARGE MEDICATIONS
1. Apixaban 5 mg orally twice daily — CRITICAL: do not stop; continue indefinitely; take at same times each day
2. Flecainide 100 mg orally twice daily — maintenance dose; ALSO: pill-in-pocket supply of 200 mg x4 tablets provided
3. Metoprolol succinate 25 mg orally daily — continued
4. Amlodipine 10 mg orally daily — continued
5. Metformin 500 mg orally twice daily — continued
6. Atorvastatin 20 mg orally nightly — continued
7. Levothyroxine 88 mcg orally daily on empty stomach — continued

DISCHARGE INSTRUCTIONS
You had an episode of your known irregular heart rhythm (atrial fibrillation) that was successfully converted back to a normal rhythm with a brief electrical shock procedure. Your blood thinner (apixaban) must be continued every day for at least 4 weeks after the cardioversion, and long-term due to your stroke risk. Never stop apixaban without calling your electrophysiologist. You have a pill-in-pocket supply of flecainide 200 mg — if you feel your heart racing irregularly, take two tablets immediately, rest, and call the clinic; if symptoms do not improve in 2–3 hours or you feel lightheaded, go to the ER. Keep all pill supplies refilled. Avoid excess caffeine, alcohol, and sleep deprivation, which can trigger AFib. Consider catheter ablation at your next cardiology visit.

FOLLOW-UP
1. Electrophysiology (Dr. Chen): 2 weeks — rhythm review, ablation consultation
2. Primary Care: 3 weeks — hypertension, diabetes, lipids
3. Cardiology echo: 3 months — left atrial size monitoring""",
    },
    {
        "title": "Non-ST-Elevation Myocardial Infarction — Prior Coronary Artery Disease",
        "category": "Cardiology / Interventional Cardiology",
        "expected_codes": ["I252"],
        "text": """DISCHARGE SUMMARY
==================
Patient: James Okonkwo, 69M | MRN: 5083921
Admission: 11/01/2025 | Discharge: 11/05/2025 | LOS: 4 days
Attending: Dr. A. Walsh, MD | Service: Cardiology / Interventional Cardiology

CHIEF COMPLAINT
Substernal chest pressure with radiation to the left arm, onset at rest, for two hours.

HISTORY OF PRESENT ILLNESS
Mr. Okonkwo is a 69-year-old man with a history of coronary artery disease and a prior myocardial infarction (anterior STEMI six years ago treated with primary PCI to the LAD with placement of a drug-eluting stent, now coded as old myocardial infarction) who presents with a two-hour history of chest pressure identical in character to his prior MI. He describes a substernal pressure rated 7/10 in severity, radiating to the left arm and jaw, associated with diaphoresis and mild nausea, that began while he was sitting watching television at rest. He took one sublingual nitroglycerin tablet at home with only minimal improvement (pressure reduced to 5/10). He activated 911 and was transported to the emergency department.

He reports no prior episodes of chest pain since his LAD stent placement six years ago. He has been maintained on dual antiplatelet therapy (aspirin and clopidogrel) for six years, though clopidogrel was discontinued two years ago by his cardiologist after the minimum post-DES period was reached, and he has been on aspirin monotherapy since then. He has been adherent to all medications including aspirin, atorvastatin, metoprolol, and lisinopril. His most recent stress echocardiogram fourteen months ago showed no inducible ischemia with preserved LVEF of 52% and a fixed anterior wall motion abnormality (known scar from prior MI).

In the emergency department, initial ECG showed NSR with 1.5 mm ST depression in leads V4–V6 and 1 mm ST depression in leads I and aVL, without ST elevation — consistent with NSTEMI or posterior extension injury. Troponin I on arrival was 2.4 ng/mL, markedly elevated. He was given aspirin 325 mg, IV heparin infusion, and IV nitroglycerin for ongoing chest pressure. He was admitted to the cardiac intensive care unit for urgent management of NSTEMI with plan for early invasive strategy.

PAST MEDICAL HISTORY
1. Coronary artery disease — prior LAD STEMI six years ago, treated with primary PCI (DES to proximal LAD); old myocardial infarction
2. Anterior wall motion abnormality, fixed — known scar from prior STEMI
3. Essential hypertension on lisinopril and metoprolol
4. Hyperlipidemia on atorvastatin 80 mg (high-intensity)
5. Type 2 diabetes mellitus on metformin
6. Heart failure with reduced ejection fraction — LVEF 52% (mildly reduced), attributed to prior LAD infarction
7. Peripheral arterial disease — bilateral claudication, ABI 0.78
8. Chronic kidney disease Stage 2 (eGFR 72)

PAST SURGICAL HISTORY
Primary PCI with DES to proximal LAD six years ago (STEMI). No CABG. No non-cardiac major surgeries.

MEDICATIONS ON ADMISSION
1. Aspirin 81 mg orally daily — adherent
2. Atorvastatin 80 mg orally nightly — adherent (high-intensity)
3. Metoprolol succinate 100 mg orally daily
4. Lisinopril 40 mg orally daily
5. Metformin 1000 mg orally twice daily — held on admission for potential procedure
6. Sublingual nitroglycerin 0.4 mg as needed
7. Furosemide 20 mg orally daily (for mild HFrEF)

ALLERGIES
No known drug allergies. Prior clopidogrel — discontinued intentionally after DAPT period; no adverse reaction history.

SOCIAL HISTORY
Retired mechanical engineer. Married, lives with wife. Three adult children. Former smoker — 40 pack-year history, quit 6 years ago at time of prior MI. No alcohol since prior MI per cardiologist recommendation. No illicit drug use. Limited exercise due to PAD claudication; otherwise mostly sedentary. Medicare coverage.

FAMILY HISTORY
Father had MI at age 55, died of cardiac arrest at 58. Mother had hypertension and diabetes. One sibling had CABG at age 64.

REVIEW OF SYSTEMS
Positive: substernal chest pressure radiating to left arm and jaw (2 hours), diaphoresis, nausea.
Negative: vomiting, shortness of breath at rest, syncope, palpitations, fever, chills, cough, hemoptysis, abdominal pain, hematuria, leg swelling beyond baseline claudication.

PHYSICAL EXAMINATION ON ADMISSION (CARDIAC ICU)
Vital Signs: Temp 36.9°C, BP 148/90 mmHg, HR 82 bpm regular, RR 18 breaths/min, SpO2 97% RA, Wt 88 kg
General: Middle-aged man in moderate distress from chest pressure. Diaphoretic. Alert and oriented x3.
HEENT: No JVD at 45 degrees on admission. No carotid bruits. No lymphadenopathy.
Cardiovascular: Regular rate and rhythm. S1 and S2. S4 gallop appreciated at apex. No S3. No murmurs. No pericardial friction rub.
Pulmonary: Clear to auscultation bilaterally. No crackles. No wheeze.
Abdomen: Soft, non-tender, non-distended. No organomegaly. No aortic bruit.
Extremities: Trace bilateral ankle edema (chronic). Peripheral pulses diminished at dorsalis pedis bilaterally (PAD). No calf tenderness.
Neurological: Alert and oriented x3. No focal deficits.

LABORATORY DATA
Troponin I (Arrival): 2.4 ng/mL — markedly elevated
Troponin I (3h): 5.8 ng/mL — rising pattern; peak
Troponin I (12h): 4.2 ng/mL — trending down post-intervention
Troponin I (24h): 1.6 ng/mL — continuing to fall
Peak CK-MB: 28 ng/mL (normal <5); CK total: 420 U/L — consistent with moderate myocardial injury
BMP: Na 138, K 4.0, Cl 102, HCO3 24, BUN 22, Cr 1.2 (baseline), Glucose 186 mg/dL
CBC: WBC 12.4 K/uL (stress leukocytosis), Hgb 13.8, Hct 41.4%, Plt 192
INR: 1.0 (not on warfarin)
aPTT: 28 s baseline; 68 s on heparin infusion (therapeutic range 60–100 s)
HbA1c: 7.8%
BNP: 320 pg/mL — mildly elevated, consistent with mildly reduced LVEF and acute event
LDL on high-intensity statin: 62 mg/dL — at target

IMAGING AND DIAGNOSTICS
12-Lead ECG (Admission): NSR at 82 bpm. Old Q-waves in leads V1–V3 (known prior anterior MI). New 1.5 mm horizontal ST depression V4–V6, 1 mm ST depression I and aVL. No ST elevation. T-wave flattening laterally. QTc 446 ms. Findings consistent with NSTEMI; lateral ischemia superimposed on known anterior scar.
Chest X-Ray: Mild cardiomegaly. No pulmonary edema. No pleural effusions. No pneumothorax.
Coronary Angiography (Hospital Day 1, Urgent Invasive Strategy): LAD — prior DES in proximal LAD patent, no in-stent restenosis, 40% stenosis mid-LAD (non-flow-limiting), TIMI 3 flow. LCx — 90% stenosis at the second obtuse marginal branch (OM2) — culprit lesion, consistent with lateral ischemia on ECG. RCA — 50% mid-vessel stenosis, TIMI 3 flow. LM — no significant disease. Conclusion: Culprit OM2 90% stenosis.
PCI (Hospital Day 1): OM2 lesion crossed with 0.014 guidewire. Pre-dilated with 2.5 x 12 mm balloon. Drug-eluting stent (2.75 x 20 mm Onyx zotarolimus-eluting) deployed at 16 atm. Excellent result — 0% residual stenosis, TIMI 3 flow. No dissection. No slow flow.
Echocardiogram (Hospital Day 2, post-PCI): LVEF 50% — mildly reduced, unchanged from prior. Fixed anterior hypokinesis (known scar). No new wall motion abnormality in lateral territory suggesting successful reperfusion. Mild mitral regurgitation. Grade II diastolic dysfunction.

HOSPITAL COURSE
Mr. Okonkwo was admitted to the cardiac ICU for management of NSTEMI with early invasive strategy. He was loaded with ticagrelor 180 mg in the ED (preferred over clopidogrel given NSTEMI per current ACS guidelines, prior tolerance confirmed) and maintained on heparin infusion. Chest pressure resolved following IV nitroglycerin and within 30 minutes of ticagrelor administration.

He underwent coronary angiography on hospital day 1 (within 24 hours of admission, consistent with high-risk NSTEMI criteria — troponin elevation, ST changes, prior CAD) with identification of the OM2 culprit lesion and successful PCI with DES as described above. Post-procedure course was uncomplicated.

He was transferred from the cardiac ICU to the step-down telemetry unit on day 2. Troponin trended appropriately downward post-intervention. Echocardiogram showed stable LVEF with no new wall motion abnormality — confirming successful revascularization without new ischemic territory injury. Heparin was discontinued after PCI.

DAPT was reinitiated: aspirin 81 mg daily (continued from admission loading dose) plus ticagrelor 90 mg twice daily — minimum 12 months required given ACS indication; indefinite aspirin. He was extensively counseled on the importance of not stopping ticagrelor early. Proton pump inhibitor (pantoprazole 40 mg daily) was added for GI protection with DAPT.

Metformin was restarted on day 3 after creatinine confirmed stable. Atorvastatin was maintained at 80 mg — LDL already at 62 mg/dL. Lisinopril and metoprolol continued. Furosemide was held given no signs of decompensated heart failure on this admission; to be restarted outpatient as needed.

He was ambulated by physical therapy on days 2 and 3 without symptoms. He was discharged on day 4 in stable condition with cardiac rehabilitation referral.

DISCHARGE DIAGNOSES
1. Non-ST-elevation myocardial infarction — lateral territory; OM2 culprit; old myocardial infarction (prior LAD STEMI) — primary admission diagnosis
2. Successful emergent PCI with DES to OM2 branch
3. Coronary artery disease — multivessel; LAD stent patent; mid-LAD and mid-RCA non-flow-limiting disease managed medically
4. Heart failure with mildly reduced ejection fraction (LVEF 50%) — stable
5. Essential hypertension — active comorbidity
6. Type 2 diabetes mellitus — active comorbidity
7. Hyperlipidemia, controlled — active comorbidity
8. Peripheral arterial disease — active comorbidity
9. Chronic kidney disease Stage 2 — active comorbidity

DISCHARGE CONDITION
Stable. Chest pain-free since PCI. No recurrent ischemia on telemetry. LVEF stable at 50%. Hemodynamically stable. Tolerating dual antiplatelet therapy and all medications.

DISCHARGE MEDICATIONS
1. Aspirin 81 mg orally daily — CRITICAL: do not stop; lifelong
2. Ticagrelor 90 mg orally twice daily — CRITICAL: do not stop for minimum 12 months; ACS/DES indication; take at same times daily
3. Pantoprazole 40 mg orally daily — NEW; GI protection with dual antiplatelet
4. Atorvastatin 80 mg orally nightly — high-intensity; continue lifelong
5. Metoprolol succinate 100 mg orally daily — continued
6. Lisinopril 40 mg orally daily — continued
7. Metformin 1000 mg orally twice daily — RESUMED; hold if contrast planned
8. Sublingual nitroglycerin 0.4 mg as needed — keep on person at all times

DISCHARGE INSTRUCTIONS
You had a second heart attack caused by a new blockage in a different artery. We opened the blockage with a stent. You MUST take both blood thinners (aspirin and ticagrelor) every day without fail for at least 12 months — stopping early can cause the stent to clot and cause another heart attack. Do not have any elective procedures or dental work without telling your cardiologist first. If you develop chest pressure again, take one nitroglycerin tablet, wait 5 minutes, repeat up to 3 times, and call 911 if not fully relieved. Do not drive for 48 hours. Begin cardiac rehabilitation as scheduled.

FOLLOW-UP
1. Interventional Cardiology (Dr. Walsh): 1 week — DAPT review, wound check, labs
2. Heart Failure Clinic: 2 weeks — LVEF monitoring, medication optimization
3. Cardiac Rehabilitation: Starts within 4 weeks — 36-session program
4. Primary Care: 2 weeks — diabetes, blood pressure, renal function""",
    },
    {
        "title": "Acute Kidney Failure — Contrast-Induced and NSAID-Related AKI",
        "category": "Nephrology / Internal Medicine",
        "expected_codes": ["N179"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Sandra Kim, 62F | MRN: 6204831
Admission: 10/28/2025 | Discharge: 11/02/2025 | LOS: 5 days
Attending: Dr. T. Morris, MD | Service: Nephrology / Internal Medicine

CHIEF COMPLAINT
Decreased urine output, nausea, and rising creatinine (3.4 mg/dL from baseline 1.0) found on outpatient lab check three days after CT with contrast for abdominal pain workup.

HISTORY OF PRESENT ILLNESS
Ms. Kim is a 62-year-old woman with type 2 diabetes mellitus, hypertension, and no prior history of chronic kidney disease who underwent outpatient CT abdomen and pelvis with intravenous iodinated contrast three days before admission for evaluation of right lower quadrant abdominal pain (ultimately attributed to a resolving right ovarian cyst on imaging). She was not adequately pre-hydrated prior to the CT scan and was not instructed to hold nephrotoxic medications. She had been using ibuprofen 600 mg three times daily for the prior two weeks for low back pain. She did not discontinue ibuprofen before or after the contrast study as she was not told to do so.

Two days after the CT scan she developed markedly decreased urine output — she estimates she urinated only two to three times in 24 hours in small amounts. She also reports progressive nausea, mild ankle swelling, and fatigue. She went to her primary care physician the following morning and labs showed creatinine 3.4 mg/dL (documented baseline creatinine 1.0 mg/dL at annual labs six months prior). She was referred urgently to the emergency department. She denies gross hematuria, rash, joint pain, fever, or purpuric lesions. She has not had any new medications started other than ibuprofen. No streptococcal illness or URI recently. She denies recent diarrhea, vomiting, or significant fluid loss.

PAST MEDICAL HISTORY
1. Type 2 diabetes mellitus on metformin and glipizide
2. Essential hypertension on lisinopril and hydrochlorothiazide
3. Hyperlipidemia on simvastatin
4. Obesity, BMI 34
5. No prior history of kidney disease; baseline creatinine 1.0 mg/dL
6. Chronic low back pain managed with NSAIDs (ibuprofen — against medical advice given diabetes and now AKI)
7. Right ovarian cyst (incidental, resolving on imaging)

PAST SURGICAL HISTORY
Laparoscopic appendectomy age 38. No other surgeries.

MEDICATIONS ON ADMISSION
1. Metformin 1000 mg orally twice daily — held on admission (contraindicated with AKI)
2. Glipizide 5 mg orally daily
3. Lisinopril 20 mg orally daily — held on admission given AKI
4. Hydrochlorothiazide 25 mg orally daily — held on admission
5. Simvastatin 20 mg orally nightly
6. Ibuprofen 600 mg orally three times daily — STOPPED on admission; identified as major precipitant

ALLERGIES
Sulfonamides (rash). No other known drug allergies.

SOCIAL HISTORY
Administrative director at a university. Married, lives with husband. Two adult children. Nonsmoker. Moderate alcohol — three to four drinks per week. No illicit drug use. Active lifestyle — walks 30 minutes daily. Commercial insurance. Adequate health literacy and engaged in care.

FAMILY HISTORY
Mother had type 2 diabetes and hypertension, died of heart disease at age 71. No family history of kidney disease or autoimmune conditions.

REVIEW OF SYSTEMS
Positive: markedly decreased urine output (oliguria) x48 hours, nausea, mild bilateral ankle edema (new), fatigue, malaise.
Negative: gross hematuria, tea-colored urine, rash, joint pain, fever, chills, flank pain, chest pain, dyspnea, diarrhea, vomiting, confusion, focal neurological deficits.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 36.9°C, BP 158/96 mmHg, HR 88 bpm, RR 16 breaths/min, SpO2 97% RA, Wt 92 kg
General: Obese woman in mild distress due to nausea and fatigue. Alert and oriented x3. Mildly anxious.
HEENT: Oral mucosa moist. No JVD. No lymphadenopathy. No periorbital edema.
Cardiovascular: Regular rate and rhythm. S1 and S2. No murmurs.
Pulmonary: Clear to auscultation bilaterally. No crackles.
Abdomen: Mild diffuse tenderness, right greater than left, without guarding or rebound. No organomegaly. Normoactive bowel sounds. No CVA tenderness bilaterally.
Extremities: 1+ bilateral ankle edema. Peripheral pulses 2+. No rash or purpura.
Neurological: Alert and oriented x3. No focal deficits. No asterixis (hepatic/uremic encephalopathy screen negative).

LABORATORY DATA
BMP (Admission): Na 138, K 5.6 mEq/L (hyperkalemia), Cl 106, HCO3 18 mEq/L (metabolic acidosis), BUN 68, Cr 3.4 mg/dL (baseline 1.0), Glucose 202 mg/dL
eGFR: 15 mL/min/1.73m² — severely decreased, AKI Stage 3 (KDIGO)
CBC: WBC 10.2, Hgb 12.8, Hct 38.4%, Plt 248 — normal
Urinalysis: SG 1.018, 2+ protein, 1+ blood, 5–10 RBC/hpf (non-dysmorphic), no casts, no nitrites, no leukocyte esterase
Urine sodium: 28 mEq/L — intermediate; FeNa 1.4% — mixed prerenal and intrinsic
Urine microscopy: Muddy brown granular casts — consistent with acute tubular necrosis
Urine osmolality: 380 mOsm/kg
C3, C4: Normal — complement-mediated GN excluded
ANA, ANCA, anti-GBM: Negative — vasculitis and Goodpasture excluded
Serum protein electrophoresis: No M-spike — myeloma excluded
Uric acid: 8.4 mg/dL — mildly elevated
BNP: 96 pg/mL — mildly elevated; mild volume overload
ECG: Normal sinus rhythm; peaked T-waves V2-V4 — hyperkalemia pattern; no sine wave morphology

Day 3 BMP: Na 139, K 4.8, HCO3 20, BUN 48, Cr 2.2 — improving
Day 5 (Discharge): Na 140, K 4.4, HCO3 22, BUN 28, Cr 1.4 — continuing to improve toward baseline

IMAGING AND DIAGNOSTICS
Renal Ultrasound (Hospital Day 1): Right kidney 10.4 cm, left kidney 10.6 cm — normal size bilaterally. No hydronephrosis. No renal calculi. No obstructive lesion. Slightly increased cortical echogenicity bilaterally consistent with acute parenchymal injury. No cysts of concern.
CT Abdomen/Pelvis (Prior Outpatient, 3 days pre-admission): Right ovarian cyst 2.8 cm — simple, benign morphology. No free air. No abscess. No appendicitis. Kidneys appeared normal in size on imaging (no prior kidney pathology identified, supporting acute onset).

HOSPITAL COURSE
Ms. Kim was admitted for management of AKI Stage 3, attributed to a combination of contrast nephropathy (iodinated contrast in a diabetic patient with no pre-hydration protocol) and concurrent NSAID nephrotoxicity (ibuprofen 600 mg three times daily for two weeks causing afferent arteriolar vasoconstriction and interstitial nephritis). Urine microscopy demonstrating muddy brown granular casts confirmed acute tubular necrosis as the dominant pathophysiology.

Ibuprofen was immediately discontinued. Lisinopril and hydrochlorothiazide were held given AKI — ACE inhibitor reduces GFR in the setting of acute tubular injury, and thiazide provides no diuretic benefit in severe AKI. Metformin was held given creatinine above 1.5 mg/dL. All nephrotoxic medications were reviewed and none added.

IV isotonic saline was infused at 125 mL/hour for the first 24 hours to correct mild volume depletion and promote tubular flow. Urine output improved from approximately 400 mL on the day of admission to 900 mL by day 2 and 1,600 mL by day 3. Hyperkalemia (K 5.6) was managed with patiromer 8.4g orally daily plus dietary potassium restriction. ECG changes (peaked T-waves) prompted one-time IV calcium gluconate 1g for membrane stabilization on admission night; subsequent ECG showed resolution of peaked T-wave morphology after 48 hours of potassium management. No need for dialysis.

Metabolic acidosis (HCO3 18 on admission) was managed with oral sodium bicarbonate 650 mg three times daily, with improvement to 22 mEq/L by discharge. Hyperglycemia was managed with a conservative sliding scale given the metformin hold; glipizide was continued at reduced dose.

Nephrology was closely involved throughout. The team counseled her extensively and clearly: (1) NSAIDs are permanently contraindicated; acetaminophen is the preferred analgesic; (2) future contrast CT scans require pre-procedure hydration, creatinine check, and metformin hold per protocol; (3) ACE inhibitor will be restarted outpatient once creatinine returns to baseline. Outpatient nephrology follow-up was arranged to monitor for full renal recovery and evaluate for any superimposed chronic kidney disease from the acute injury.

DISCHARGE DIAGNOSES
1. Acute kidney failure, unspecified — AKI Stage 3 (creatinine peak 3.4 from baseline 1.0); multifactorial: contrast nephropathy plus NSAID nephrotoxicity (acute tubular necrosis); primary admission diagnosis
2. Hyperkalemia — resolved with patiromer and dietary restriction
3. Metabolic acidosis — partially corrected
4. Type 2 diabetes mellitus — active comorbidity; metformin held
5. Essential hypertension — active comorbidity; ACE inhibitor and thiazide held during AKI
6. NSAID use (ibuprofen) against medical advice — primary precipitating factor
7. Obesity — active comorbidity

DISCHARGE CONDITION
Improved. Urine output normalized. Creatinine declining (1.4 at discharge, improving toward baseline 1.0). Edema resolved. Nausea resolved. Potassium 4.4 mEq/L. Tolerating oral diet and medications.

DISCHARGE MEDICATIONS
1. Acetaminophen 500 mg orally every 6 hours as needed (max 2g/day) — ONLY safe analgesic; NEVER take ibuprofen, naproxen, or any NSAID again
2. Glipizide 5 mg orally daily — continued; monitor glucose
3. Simvastatin 20 mg orally nightly — continued
4. Sodium bicarbonate 650 mg orally twice daily — 2-week course; recheck at nephrology
5. Patiromer 8.4g orally daily with food — continue until nephrology clears
6. Lisinopril and Hydrochlorothiazide — HELD; restart only when nephrologist confirms creatinine at baseline
7. Metformin — HELD; do NOT restart until creatinine returns to ≤1.0 and nephrology approves

DISCHARGE INSTRUCTIONS
Your kidneys were seriously injured by a combination of the IV dye from your CT scan and the ibuprofen you were taking. Your kidney function is improving but is not yet back to normal. You must NEVER take ibuprofen, naproxen (Aleve), or any anti-inflammatory pain medication ever again — these medications can cause permanent kidney failure. For pain, use only Tylenol (acetaminophen) up to 2 grams daily. Do not restart lisinopril or your water pill until your kidney doctor tells you to. If your urine output decreases significantly, you feel very swollen, or you feel confused or extremely fatigued, go to the ER immediately.

FOLLOW-UP
1. Nephrology (Dr. Morris): 1 week — creatinine, electrolytes, decision to restart held medications
2. Primary Care: 2 weeks — blood pressure, diabetes management
3. Nephrology (follow-up): 4 weeks — confirm full renal recovery, evaluate for residual CKD""",
    },
    {
        "title": "Urosepsis — Complicated Urinary Tract Infection with Bacteremia",
        "category": "Internal Medicine / Infectious Disease",
        "expected_codes": ["N390"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Helen Watkins, 77F | MRN: 7391024
Admission: 11/03/2025 | Discharge: 11/07/2025 | LOS: 4 days
Attending: Dr. J. Rivera, MD | Service: Internal Medicine / Infectious Disease

CHIEF COMPLAINT
Confusion, fever, and flank pain in an elderly woman; found to have urinalysis consistent with infection and blood pressure 88/54 mmHg on arrival.

HISTORY OF PRESENT ILLNESS
Ms. Watkins is a 77-year-old woman with a history of recurrent urinary tract infections, type 2 diabetes mellitus, and hypertension who was brought to the emergency department by her daughter after two days of confusion (described as not recognizing her home, forgetting her daughter's name), fever to 38.9°C at home, right flank pain rated 5/10, chills, and decreased oral intake. She denies dysuria, urinary frequency, or gross hematuria, though her daughter notes she has been voiding less frequently than usual over the past two days. She also reports one episode of nausea and vomiting this morning.

She has a history of three UTIs in the past eighteen months, with two requiring antibiotic treatment. The last episode was eight months ago and was treated with nitrofurantoin for five days. She has no prior history of urosepsis or bacteremia. She has a known history of urinary retention related to pelvic floor dysfunction — she has been wearing absorbent pads and recently was fitted for an indwelling Foley catheter six days ago by her urologist for incomplete bladder emptying (post-void residual 280 mL confirmed by ultrasound). The Foley catheter is still in place.

In the emergency department, initial vital signs were notable for temperature 39.2°C, blood pressure 88/54 mmHg, heart rate 118 bpm, and oxygen saturation 94% on room air. She appeared confused and was unable to state the date or where she was. Urinalysis showed pyuria (>100 WBC/hpf), bacteriuria (large), positive nitrites, and positive leukocyte esterase. She was recognized as meeting SIRS criteria with signs of end-organ dysfunction (altered mental status, hypotension) — consistent with urosepsis/septic shock. She received 2 liters IV normal saline and blood pressure improved to 104/62 mmHg, avoiding vasopressor initiation. Blood cultures (two sets) were drawn, and IV piperacillin-tazobactam was initiated empirically within 45 minutes of triage.

PAST MEDICAL HISTORY
1. Recurrent urinary tract infections, history of three episodes in 18 months
2. Urinary retention — pelvic floor dysfunction; post-void residual 280 mL; Foley catheter placed 6 days prior to admission by urology
3. Type 2 diabetes mellitus on metformin
4. Essential hypertension on amlodipine and lisinopril
5. Mild cognitive impairment at baseline — independent in most ADLs, lives with daughter
6. Osteoporosis on alendronate and calcium supplementation
7. Chronic lower extremity edema managed with compression stockings

PAST SURGICAL HISTORY
Total abdominal hysterectomy age 52. Left total knee arthroplasty age 68. No urological surgeries.

MEDICATIONS ON ADMISSION
1. Metformin 500 mg orally twice daily — held on admission
2. Amlodipine 10 mg orally daily — held initially given hypotension; resumed day 2
3. Lisinopril 10 mg orally daily — held initially; resumed day 3
4. Alendronate 70 mg orally weekly — continued on appropriate day
5. Calcium carbonate 500 mg orally twice daily — continued
6. Vitamin D 1000 IU orally daily — continued
7. Docusate sodium 100 mg orally daily — continued

ALLERGIES
Nitrofurantoin (GI intolerance — nausea and vomiting with full course; documented at urology). Trimethoprim-sulfamethoxazole (sulfonamide allergy — rash). Note: these allergies significantly limit oral UTI treatment options.

SOCIAL HISTORY
Retired librarian. Widowed, lives with adult daughter in a one-story home. Two additional adult children nearby. Nonsmoker. No alcohol in the past five years (prior social drinker). No illicit drug use. Mild cognitive impairment per prior neuropsychological testing — manages daily activities with family support. Medicare and Medicaid dual coverage. English-speaking.

FAMILY HISTORY
Mother had hypertension and dementia. Father died of prostate cancer. One sibling with type 2 diabetes.

REVIEW OF SYSTEMS
Positive: confusion (2 days), fever (38.9°C at home), chills, right flank pain, nausea, vomiting (x1), decreased oral intake, decreased urine output, general malaise, weakness.
Negative: cough, chest pain, shortness of breath, diarrhea, abdominal pain beyond flank, headache, focal neurological deficits, rash, gross hematuria, dysuria (denied; may be limited historian due to cognitive state).

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 39.2°C, BP 88/54 mmHg → 104/62 after 2L IVF, HR 118 bpm, RR 22 breaths/min, SpO2 94% RA → 97% on 2L NC, Wt 68 kg
General: Elderly woman in moderate distress. Appears ill and fatigued. Confused — disoriented to date, place, situation. Responds to voice. Not agitated.
HEENT: Dry mucous membranes. No JVD. No lymphadenopathy.
Cardiovascular: Tachycardic and regular. No murmurs. Weak peripheral pulses on arrival.
Pulmonary: Coarse rhonchi bilaterally, likely secretions. No focal consolidation. No wheeze.
Abdomen: Mild right-sided and suprapubic tenderness. No rebound or guarding. Normoactive bowel sounds. Right costovertebral angle tenderness — moderate, consistent with pyelonephritis.
Genitourinary: Foley catheter in place; draining cloudy, dark yellow urine with sediment.
Extremities: 1+ bilateral lower extremity edema (chronic). No calf tenderness. Peripheral pulses weak on arrival, improving with fluids.
Neurological: Confused, disoriented x2-3. Follows simple commands inconsistently. No focal motor deficits. No Babinski. Fluctuating attention — consistent with delirium.

LABORATORY DATA
CBC: WBC 18.6 K/uL (markedly elevated, 88% PMNs, 7% bands), Hgb 11.2, Hct 33.6%, Plt 142 K/uL (thrombocytopenia, early sepsis-associated)
BMP: Na 132 mEq/L (hyponatremia), K 3.4, Cl 98, HCO3 20 (metabolic acidosis), BUN 46, Cr 1.8 mg/dL (baseline unknown; estimated ~1.0 for age), Glucose 268 mg/dL (hyperglycemia)
Lactate: 3.1 mmol/L — elevated, consistent with sepsis/early shock
Procalcitonin: 18.6 ng/mL — markedly elevated; severe bacterial infection
Urinalysis: Appearance cloudy, SG 1.025, pH 6.0, protein 2+, 3+ blood, >100 WBC/hpf, large bacteria, 3+ nitrite, 3+ leukocyte esterase — frank pyuria and bacteriuria
Urine culture (catheter specimen): Escherichia coli, >100,000 CFU/mL — susceptible to ceftriaxone, piperacillin-tazobactam, gentamicin; resistant to ampicillin, trimethoprim-sulfamethoxazole, ciprofloxacin (ESBL-negative by final sensitivity)
Blood cultures (2 sets): Escherichia coli in 3 of 4 bottles — bacteremia confirmed; same organism and sensitivity as urine culture
HbA1c: 9.2% — poorly controlled diabetes

Day 2 BMP: Na 136, K 4.0, BUN 32, Cr 1.3, Glucose 182 — improving
Discharge BMP: Na 139, K 4.2, BUN 18, Cr 1.0, Glucose 148 — at estimated baseline

IMAGING AND DIAGNOSTICS
CT Abdomen/Pelvis without contrast (Hospital Day 1): Thickening of the right renal collecting system and perinephric fat stranding — consistent with acute pyelonephritis. No renal abscess. No perirenal abscess. No obstructing calculus. No gas in the collecting system (excludes emphysematous pyelonephritis). Foley catheter tip in bladder, appropriate position. Bilateral mild hydronephrosis — likely related to incomplete drainage prior to catheter, not obstruction. Normal appendix.
Chest X-Ray: No focal consolidation. No pulmonary edema. No pleural effusions. Coarse basilar markings, likely secretions. No pneumothorax.

HOSPITAL COURSE
Ms. Watkins was admitted to the internal medicine unit on telemetry for management of urosepsis with bacteremia secondary to a complicated catheter-associated urinary tract infection (CAUTI) with Escherichia coli. The Foley catheter, placed six days prior and identified as the likely source and reservoir of infection, was replaced immediately on admission with a new sterile catheter using aseptic technique.

Sepsis resuscitation per protocol: 30 mL/kg IV crystalloid over the first three hours (approximately 2 liters given her weight). Blood pressure responded adequately to fluid resuscitation; vasopressor therapy was not required. She was maintained on continuous telemetry with hourly blood pressure monitoring for the first 24 hours. Oxygen was weaned from 2L nasal cannula to room air by hospital day 2.

Empirical antibiotic therapy with IV piperacillin-tazobactam 3.375g every 6 hours was initiated in the ED. When blood culture sensitivities resulted on day 2 — showing E. coli susceptible to ceftriaxone (MIC ≤1 mg/L) and resistant to ciprofloxacin — therapy was de-escalated to ceftriaxone 2g IV daily for definitive treatment of bacteremic E. coli pyelonephritis. Duration of therapy: 14 days total from first negative blood culture (the bacteremia cleared confirmed on day 2 repeat cultures), transitioning to oral amoxicillin-clavulanate on day 4 (sensitivity confirmed) to complete the course at home.

Delirium management: she was placed in a single room with her daughter at bedside throughout. Reorientation, environmental light/dark cycling, and early ambulation with physical therapy were prioritized. Antipsychotic medications were avoided given her age and limited benefit evidence in delirium. By day 3, mental status improved substantially — she was oriented x2 (person and place) and engaged in meaningful conversation. By discharge she had returned to near-baseline cognitive function per her daughter.

Hyperglycemia was managed with a corrective insulin scale; glucose improved from 268 on admission to a range of 130–160 by day 3. Metformin was held for AKI; outpatient diabetes management to be reconsidered given HbA1c of 9.2% — endocrinology referral placed.

Urology was consulted on day 2 regarding the Foley catheter. Given the bacteremia and CAUTI, they recommended a trial of suprapubic catheter placement versus re-evaluation for intermittent self-catheterization once the acute infection resolved. She was discharged with the replacement Foley in place and urology follow-up in one week to reassess.

DISCHARGE DIAGNOSES
1. Urinary tract infection, complicated — catheter-associated; bacteremic Escherichia coli urosepsis; primary admission diagnosis
2. Septic shock, resolved — hypotension responsive to fluid resuscitation; no vasopressor required
3. Acute kidney injury, resolved — peak Cr 1.8, at baseline 1.0 at discharge
4. Delirium — resolved; near-baseline mental status at discharge
5. Catheter-associated urinary tract infection — Foley catheter replaced
6. Type 2 diabetes mellitus with hyperglycemia — poorly controlled; HbA1c 9.2%
7. Hyponatremia — resolved
8. Essential hypertension — active comorbidity
9. Mild cognitive impairment at baseline — active comorbidity

DISCHARGE CONDITION
Improved. Alert, oriented x2, near-baseline per family. Afebrile >48 hours. Hemodynamically stable. Urine output adequate via Foley. Creatinine at estimated baseline. Tolerating oral diet and antibiotics.

DISCHARGE MEDICATIONS
1. Amoxicillin-clavulanate 875/125 mg orally twice daily — complete 14-day antibiotic course; approximately 10 days remaining at discharge; take with food
2. Amlodipine 10 mg orally daily — resumed
3. Lisinopril 10 mg orally daily — resumed
4. Alendronate 70 mg orally weekly — continued (on appropriate day of week)
5. Calcium carbonate 500 mg orally twice daily — continued
6. Vitamin D 1000 IU orally daily — continued
7. Docusate sodium 100 mg orally daily — continued
8. Metformin — HELD; restart only after urology/PCP confirms kidney function stable and catheter plan in place

DISCHARGE INSTRUCTIONS
You had a serious blood infection that started from a urinary tract infection related to your bladder catheter. The infection has improved significantly with IV antibiotics. You must complete the full antibiotic course at home (amoxicillin-clavulanate). Keep your catheter clean and watch for signs that the infection has returned: fever above 38°C, renewed confusion, chills, or cloudy foul-smelling urine. Go to the emergency room immediately if these develop. Your daughter should check your temperature daily for the next week. Attend all follow-up appointments — especially urology — to discuss a better long-term solution for your bladder emptying problem.

FOLLOW-UP
1. Urology: 1 week — catheter management, suprapubic vs. intermittent catheterization discussion
2. Internal Medicine (Dr. Rivera): 1 week — antibiotic completion check, blood cultures finalized
3. Primary Care: 2 weeks — metformin restart, blood pressure, renal function
4. Endocrinology: 4 weeks — diabetes management optimization (HbA1c 9.2%)""",
    },
    {
        "title": "Community-Acquired Pneumonia — PSI Class IV, Requiring IV Antibiotics",
        "category": "General Medicine / Pulmonary",
        "expected_codes": ["J189"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Arthur Patel, 73M | MRN: 8041293
Admission: 10/12/2025 | Discharge: 10/17/2025 | LOS: 5 days
Attending: Dr. L. Yamamoto, MD | Service: General Medicine

CHIEF COMPLAINT
Productive cough with rust-colored sputum, fever, and right-sided pleuritic chest pain for four days.

HISTORY OF PRESENT ILLNESS
Mr. Patel is a 73-year-old man with a history of type 2 diabetes mellitus, hypertension, and mild chronic kidney disease who presents with a four-day history of productive cough with rust-colored and then yellow-green sputum, fever peaking at 39.4°C at home, right-sided pleuritic chest pain that worsens with deep inspiration and coughing, and progressive exertional dyspnea. He reports the symptoms began suddenly with shaking chills and rigors approximately four days before admission. He initially managed at home with over-the-counter acetaminophen and increased oral fluids, but his condition worsened with increasing shortness of breath and an inability to complete activities of daily living without fatigue. His daughter noted he appeared dusky and brought him to the emergency department.

He has no prior history of pneumonia. He received his annual influenza vaccine one month prior but has never received pneumococcal vaccination. He denies recent sick contacts, recent travel, aspiration events, or healthcare exposure in the past 90 days. He lives at home with his wife and is independent in his daily activities at baseline. He denies hemoptysis, significant weight loss, night sweats, or chronic respiratory symptoms. He has no known structural lung disease, immunosuppression, or history of recurrent infections.

In the emergency department, oxygen saturation was 88% on room air, improving to 94% on 4L nasal cannula. Temperature was 39.6°C. Blood pressure was 112/68 mmHg (mild hypotension). Right lower lobe consolidation was confirmed on chest radiograph. PSI score was calculated at 128 points (Class IV) based on age, comorbidities, laboratory values, and radiographic findings — warranting inpatient admission. IV antibiotics were initiated within one hour of triage.

PAST MEDICAL HISTORY
1. Type 2 diabetes mellitus, 8-year history on metformin
2. Essential hypertension on amlodipine
3. Chronic kidney disease Stage 2 (eGFR 68), likely hypertensive nephrosclerosis
4. Benign prostatic hyperplasia on tamsulosin
5. Hyperlipidemia on pravastatin
6. Remote tobacco use history

PAST SURGICAL HISTORY
Transurethral resection of the prostate (TURP) age 67. Cataract surgery bilateral, remote.

MEDICATIONS ON ADMISSION
1. Metformin 1000 mg orally twice daily — held on admission for acute illness
2. Amlodipine 5 mg orally daily
3. Tamsulosin 0.4 mg orally nightly
4. Pravastatin 40 mg orally nightly
5. Aspirin 81 mg orally daily

ALLERGIES
Penicillin (rash — documented childhood allergy; no formal challenge; skin testing not performed). No other known drug allergies.

SOCIAL HISTORY
Retired accountant. Married, lives with wife in a two-story home. Three adult children locally. Former smoker — 15 pack-year history, quit 22 years ago. Occasional alcohol — one beer per weekend. No illicit drug use. Moderately active — gardens and takes short walks. Medicare with supplemental coverage. English and Gujarati-speaking; English proficient.

FAMILY HISTORY
Father had pulmonary tuberculosis — treated decades ago in India. Mother had hypertension and diabetes. No family history of malignancy or immunodeficiency.

REVIEW OF SYSTEMS
Positive: productive cough (rust-colored then yellow-green sputum), fever (39.4°C at home), shaking chills and rigors, right pleuritic chest pain, progressive dyspnea, fatigue, anorexia, decreased oral intake x3 days, nausea (no vomiting).
Negative: hemoptysis, significant weight loss, night sweats, diarrhea, abdominal pain, dysuria, lower extremity swelling, palpitations, syncope, rash, joint pain.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 39.6°C, BP 112/68 mmHg, HR 104 bpm, RR 24 breaths/min, SpO2 88% RA → 94% on 4L NC, Wt 74 kg
General: Thin elderly man in moderate respiratory distress. Appears acutely ill. Mildly diaphoretic. Speaking in short sentences. Alert and oriented x3.
HEENT: Oral mucosa dry. No JVD. No lymphadenopathy. No sinus tenderness.
Cardiovascular: Tachycardic and regular. No murmurs. No pericardial rub.
Pulmonary: Dullness to percussion right lower lung zone. Decreased breath sounds right lower lobe with bronchial breath sounds and egophony (E to A change). Coarse crackles right middle and lower lobes. Whispered pectoriloquy present at right base. Left lung clear.
Abdomen: Soft, non-tender. No organomegaly. Normoactive bowel sounds.
Extremities: No lower extremity edema. Peripheral pulses 2+. No calf tenderness.
Neurological: Alert and oriented x3. No focal deficits. Mild tremor — likely fever-related.

LABORATORY DATA
CBC: WBC 19.4 K/uL (markedly elevated, 86% PMNs, 10% bands — left shift), Hgb 12.4 g/dL, Hct 37.2%, Plt 182 K/uL
BMP: Na 132 mEq/L (hyponatremia), K 3.6, Cl 97, HCO3 22, BUN 32, Cr 1.6 mg/dL (baseline approximately 1.1), Glucose 278 mg/dL
Procalcitonin: 12.4 ng/mL — markedly elevated; severe bacterial infection
LDH: 340 U/L — elevated, consistent with significant parenchymal injury
Albumin: 3.0 g/dL — low, nutritional compromise
Troponin I: <0.02 — negative
BNP: 148 pg/mL — mildly elevated
Blood cultures (x2 sets drawn prior to antibiotics): Streptococcus pneumoniae, penicillin-intermediate (MIC 4 mg/L), susceptible to ceftriaxone — bacteremia in 1 of 4 bottles; treated as significant given clinical picture
Sputum culture: Streptococcus pneumoniae, same susceptibility pattern
Urine Legionella antigen: Negative
Urine Pneumococcal antigen: Positive — consistent with pneumococcal pneumonia
Respiratory viral panel: Negative (influenza A/B, COVID-19, RSV)
HbA1c: 9.0% — poorly controlled diabetes
HIV: Negative (ordered given severity and age)

Day 3 Labs: WBC 12.4, BMP: Na 136, Cr 1.3, Glucose 190 — improving
Discharge: WBC 9.8, Cr 1.2, Glucose 162 — approaching baseline

IMAGING AND DIAGNOSTICS
Chest X-Ray (Admission): Right lower lobe lobar consolidation — dense homogeneous opacity occupying the entire right lower lobe with air bronchograms. Small right pleural effusion. No pneumothorax. Left lung clear. Mild cardiomegaly.
Chest X-Ray (Day 3): Interval improvement in right lower lobe consolidation — consolidation less dense, improving. Pleural effusion resolved. No new infiltrate.
Chest X-Ray (Day 5, Pre-Discharge): Significant improvement in right lower lobe opacity. Residual haziness at right base. Cardiomegaly unchanged. No new process.
CT Chest without contrast (Day 1, penicillin allergy evaluation for treatment planning; also to assess for empyema): Right lower lobe lobar consolidation with air bronchograms and small right parapneumonic effusion — free-flowing, non-loculated, no septations, no pleural thickening. No empyema. No cavitation. Mild bronchial wall thickening. No mediastinal adenopathy. No evidence of malignancy behind the consolidation.
12-Lead ECG: Sinus tachycardia at 104 bpm. No acute ischemic changes. No Q-waves. QTc 436 ms.

HOSPITAL COURSE
Mr. Patel was admitted to the general medicine floor with telemetry for management of PSI Class IV community-acquired pneumonia with bacteremic Streptococcus pneumoniae. Given his penicillin allergy (rash — low-risk phenotype), the infectious disease pharmacist was consulted. Given the low-risk nature of the rash history and the susceptibility of the organism to ceftriaxone, empirical treatment with ceftriaxone 1g IV every 24 hours was initiated without skin testing — consistent with current guidelines for low-risk penicillin allergy and cephalosporin use. Azithromycin 500 mg IV daily was added for atypical organism coverage per CAP guidelines (dual therapy for bacteremic CAP). The patient was monitored closely for 30 minutes after the first dose of ceftriaxone without allergic reaction.

Azithromycin was discontinued on day 2 when blood cultures confirmed penicillin-intermediate S. pneumoniae susceptible to ceftriaxone. Ceftriaxone was continued as monotherapy. Given one positive blood culture bottle, the team treated this as true bacteremia and planned a minimum 7–10 day antibiotic course from the date of positive culture. He was transitioned to oral amoxicillin-clavulanate 875/125 mg twice daily on day 4 for outpatient completion — confirmed susceptibility on sensitivity panel.

Fever defervesced by day 3. Oxygen requirements decreased from 4L on admission to 2L by day 2 and 1L by day 4. He was maintained on room air at rest by day 5 with SpO₂ 93–94% — acceptable given his comorbidities. He required 2L with ambulation at discharge; a brief home oxygen assessment was arranged.

Hyponatremia (Na 132) was attributed to SIADH in the context of CAP — this is well-recognized. Free water restriction was implemented; sodium normalized to 136 by day 3 and 139 by day 5 with resolution of pneumonia.

Hyperglycemia was managed with a basal-bolus insulin regimen during admission with glucose levels stabilizing by day 3. Metformin was held for the acute illness; restarted on day 4 when creatinine was improving. Diabetes educator visited on day 4 regarding the elevated HbA1c of 9.0%.

He was ambulated by physical therapy beginning on day 2 and tolerated ambulation on room air by day 4. He was assessed as safe for home by occupational therapy.

Infectious disease strongly recommended pneumococcal vaccination prior to discharge (PCV20) and confirmed influenza vaccine receipt. PCV20 was administered on day 4.

DISCHARGE DIAGNOSES
1. Community-acquired pneumonia, unspecified organism — Streptococcus pneumoniae confirmed, right lower lobe lobar pneumonia with bacteremia; PSI Class IV; primary admission diagnosis
2. Bacteremic pneumococcal pneumonia — one positive blood culture, treated with 7–10 day course
3. Hyponatremia — SIADH-related; resolved with pneumonia treatment
4. Hyperglycemia — steroid-unrelated; HbA1c 9.0%, poorly controlled diabetes
5. Acute kidney injury — mild, peak Cr 1.6, improving to 1.2 at discharge
6. Type 2 diabetes mellitus — active comorbidity; poorly controlled
7. Hypertension — active comorbidity
8. Chronic kidney disease Stage 2 — active comorbidity
9. Benign prostatic hyperplasia — active comorbidity
10. Penicillin allergy (low-risk, rash) — documented; ceftriaxone tolerated

DISCHARGE CONDITION
Improved. Afebrile >72 hours. SpO₂ 93–94% on room air at rest, 90% with ambulation (home oxygen assessment arranged). Respiratory rate 16. WBC 9.8. Tolerating oral antibiotics and diet. Near-baseline mental status.

DISCHARGE MEDICATIONS
1. Amoxicillin-clavulanate 875/125 mg orally twice daily — complete antibiotic course; approximately 4 days remaining at discharge; take with food
2. Metformin 1000 mg orally twice daily — RESUMED on day 4; continue
3. Amlodipine 5 mg orally daily — continued
4. Tamsulosin 0.4 mg orally nightly — continued
5. Pravastatin 40 mg orally nightly — continued
6. Aspirin 81 mg orally daily — continued
7. Home oxygen (2L NC) — prescribed for ambulation only; home health oxygen assessment visit arranged within 48 hours; to be weaned as tolerated

DISCHARGE INSTRUCTIONS
You were very ill with bacterial pneumonia caused by a common germ called Streptococcus pneumoniae, which also got into your bloodstream. You have improved significantly. Complete the full antibiotic course. Use supplemental oxygen as directed during activity until home health tells you otherwise. You received a pneumonia vaccine today — this vaccine helps prevent this type of pneumonia in the future. If you develop return of fever above 38.5°C, worsening shortness of breath, coughing up blood, or confusion, go to the emergency department immediately. Check your blood sugar daily and write it down.

FOLLOW-UP
1. General Medicine (Dr. Yamamoto): 1 week — repeat chest X-ray in 6–8 weeks to confirm resolution (exclude underlying malignancy behind consolidation)
2. Primary Care: 2 weeks — diabetes management, blood pressure, renal function
3. Infectious Disease: 2 weeks — culture follow-up, antibiotic completion confirmation
4. Home Health: Oxygen assessment within 48 hours of discharge""",
    },
    {
        "title": "Acute Asthma Exacerbation — Moderate to Severe",
        "category": "Pulmonary Medicine",
        "expected_codes": ["J45909"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Jasmine Torres, 34F | MRN: 9183042
Admission: 11/20/2025 | Discharge: 11/22/2025 | LOS: 2 days
Attending: Dr. M. Osei, MD | Service: Pulmonary Medicine

CHIEF COMPLAINT
Severe shortness of breath, wheezing, and inability to complete a sentence, unresponsive to home nebulizer treatments for four hours.

HISTORY OF PRESENT ILLNESS
Ms. Torres is a 34-year-old woman with a known history of unspecified asthma (not on a formal step-therapy regimen; using intermittent SABA only) who presents with a four-hour progressive asthma exacerbation precipitated by a recent upper respiratory infection in her household. She reports she has been sick with nasal congestion, mild sore throat, and low-grade fever for three days, and noticed worsening wheezing and shortness of breath beginning this morning. She used her albuterol MDI 8 times over a four-hour period without meaningful relief and called 911 when she could no longer speak in full sentences.

She denies any personal history of intubation, mechanical ventilation, or ICU admission for asthma. She reports one prior emergency department visit for asthma approximately two years ago that was treated with IV methylprednisolone and nebulizers and did not require hospitalization. She has been using albuterol as her only asthma medication for the past three years — she was previously prescribed an inhaled corticosteroid (fluticasone) but discontinued it one year ago when she ran out and was not seen by a physician for a refill. She uses albuterol on average three to four times per week at baseline, which represents persistent asthma requiring a step-up in controller therapy. She has not had formal pulmonary function testing in three years. Identified triggers include respiratory viral infections, cold air, and pet dander (she recently adopted a cat).

On arrival to the emergency department, she was in severe respiratory distress with an oxygen saturation of 89% on room air, respiratory rate 32 breaths/min, audible diffuse expiratory wheezing, use of accessory muscles (sternocleidomastoid and intercostals), and inability to speak more than two to three words between breaths. She was immediately administered continuous albuterol nebulization and ipratropium, IV methylprednisolone 125 mg, and supplemental oxygen via non-rebreather mask with saturation improving to 96%. Peak expiratory flow rate was measured at 32% of personal best. She was admitted for observation and continued therapy.

PAST MEDICAL HISTORY
1. Asthma, unspecified — diagnosed age 14; never formally classified; baseline likely moderate persistent given SABA use frequency
2. Allergic rhinitis on loratadine as needed
3. Obesity, BMI 30
4. Anxiety disorder, managed with escitalopram
5. Vitamin D deficiency — on supplementation
6. No history of eczema or food allergy
7. No prior intubation or ICU admission for asthma

PAST SURGICAL HISTORY
No surgical history.

MEDICATIONS ON ADMISSION
1. Albuterol 90 mcg MDI — used 8 times in past 4 hours; baseline 3–4 times per week
2. Loratadine 10 mg orally daily as needed (seasonal)
3. Escitalopram 10 mg orally daily
4. Vitamin D 2000 IU orally daily
5. Oral contraceptive pill (ethinyl estradiol-norethindrone 35/1 mg) — daily

ALLERGIES
Codeine (nausea and vomiting). Aspirin (exacerbates asthma — aspirin-exacerbated respiratory disease suspected but not formally confirmed; avoids aspirin).

SOCIAL HISTORY
Works as a preschool teacher. Single, lives alone in an apartment. Two young nieces and nephews whom she sees frequently. Nonsmoker; never smoked. No alcohol. No illicit drug use. Recently adopted a cat (three weeks ago) — new potential allergen trigger. No cockroaches or dust mite mitigation in apartment noted. No mold exposure history. Medicaid coverage.

FAMILY HISTORY
Mother has asthma and seasonal allergies. Father has hypertension. One sibling with eczema and allergic rhinitis. Strong atopic family history.

REVIEW OF SYSTEMS
Positive: severe dyspnea, diffuse audible wheezing, chest tightness, use of accessory muscles, inability to complete sentences, respiratory viral URI symptoms x3 days (nasal congestion, sore throat, low-grade fever), productive cough with clear sputum.
Negative: fever at time of exam (afebrile in ED), hemoptysis, chest pain, palpitations, syncope, lower extremity edema, recent aspirin or NSAID use, new pet exposures other than the cat.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 37.4°C (resolved from prior low-grade fever), BP 138/88 mmHg (relative hypertension from respiratory distress and beta-agonist), HR 128 bpm, RR 32 breaths/min, SpO2 89% RA → 96% on 10L NRB, Wt 82 kg
General: Young woman in severe respiratory distress. Speaks 2–3 words between breaths. Visibly using accessory muscles. Diaphoretic. Alert and oriented.
HEENT: Oral mucosa moist. Nasal congestion present. No sinus tenderness. No JVD. No lymphadenopathy.
Cardiovascular: Tachycardic and regular. No murmurs. Pulsus paradoxus estimated at 18 mmHg (>10 mmHg consistent with severe obstruction).
Pulmonary: Diffuse expiratory and early inspiratory polyphonic wheeze throughout all lung fields. Markedly prolonged expiratory phase. Hyperresonant to percussion. No crackles. Use of sternocleidomastoid, intercostal, and scalene muscles. Decreased air entry bilaterally.
Abdomen: Soft, non-tender, non-distended.
Extremities: No edema. Peripheral pulses 2+ bilaterally.
Neurological: Alert and anxious. No focal deficits.

LABORATORY DATA
ABG on NRB mask (early): pH 7.42, PaCO2 38 mmHg, PaO2 78 mmHg — initially normocarbia; note: if PaCO2 rises in severe asthma despite tachypnea, this signals impending respiratory failure
CBC: WBC 14.8 K/uL (elevated, likely stress response and steroid effect; no bands), Hgb 13.4, Hct 40.2%, Plt 308 — normal differential (eosinophilia absent acutely due to steroid)
BMP: Na 140, K 3.4 (mild hypokalemia — expected with beta-agonist therapy), Cl 104, HCO3 24, BUN 10, Cr 0.7, Glucose 188 (steroid-induced hyperglycemia)
Peak expiratory flow (Admission): 32% of personal best (<40% = severe exacerbation)
Peak expiratory flow (2h post-treatment): 54% of personal best — improving
Peak expiratory flow (Discharge): 78% of personal best — approaching target (>80%)
Procalcitonin: 0.12 ng/mL — low; viral rather than bacterial trigger supported
Respiratory viral panel: Rhinovirus/Enterovirus detected — confirmed viral trigger

IMAGING AND DIAGNOSTICS
Chest X-Ray (Admission): Bilateral hyperinflation with flattened diaphragms and increased AP diameter consistent with air trapping. No focal consolidation (excludes pneumonia as trigger). No pneumothorax. No pleural effusion. No mediastinal shift. Heart size normal.
12-Lead ECG: Sinus tachycardia at 128 bpm. Rightward P-wave axis. No ST changes. No Q-waves. QTc 428 ms. No arrhythmia.

HOSPITAL COURSE
Ms. Torres was admitted to the pulmonary medicine unit for management of moderate-to-severe acute asthma exacerbation precipitated by rhinovirus upper respiratory infection. She was maintained on continuous supplemental oxygen, continuous cardiac and SpO₂ monitoring, and hourly peak flow monitoring.

Bronchodilator therapy was intensified from continuous nebulization in the ED to scheduled albuterol 2.5 mg nebulized every 2 hours for the first 12 hours, transitioned to every 4 hours on day 2 as she improved. Ipratropium bromide 0.5 mg nebulized every 6 hours was given for the first 24 hours. IV methylprednisolone 80 mg every 12 hours was continued for 24 hours and transitioned to oral prednisone 60 mg daily on day 2 with plan for a 5-day total steroid course (to be completed outpatient). Potassium was repleted with oral KCl 20 mEq twice daily for hypokalemia induced by beta-agonist therapy.

The patient was not intubated — her ABG remained normocarbia without hypercapnia throughout, indicating she was maintaining adequate ventilation despite severe obstruction. BiPAP was considered but not required. By hospital day 2, peak expiratory flow had improved to 78% of personal best, oxygen requirements had decreased to room air, respiratory rate was 16, and she was speaking in full sentences without accessory muscle use.

Respiratory therapy provided comprehensive inhaled corticosteroid education. A step-up in controller therapy was initiated: budesonide-formoterol 160/4.5 mcg MDI (ICS-LABA) 2 puffs twice daily was prescribed as the new maintenance controller, replacing SABA monotherapy. The critical importance of daily controller therapy was reinforced — asthma attacks requiring hospitalization are preventable with proper maintenance therapy. The concept of step therapy (controller + rescue) was reviewed.

An asthma action plan was written and given to the patient in paper form, color-coded by peak flow zone (green, yellow, red). Allergen counseling: the new cat was identified as a likely contributor to baseline inflammation that made this viral exacerbation more severe. She was referred to allergy/immunology for allergen testing and immunotherapy discussion. Aspirin avoidance confirmed and documented given possible AERD.

Pulmonary function testing (spirometry) was ordered outpatient in 4–6 weeks once the acute exacerbation has fully resolved, to formally classify asthma severity.

DISCHARGE DIAGNOSES
1. Acute asthma exacerbation, moderate to severe — unspecified asthma; rhinovirus precipitant; primary admission diagnosis
2. Rhinovirus upper respiratory infection — trigger for exacerbation
3. Poorly controlled asthma — baseline SABA overuse (3–4x/week); no controller therapy x1 year; step-up initiated
4. New cat allergen exposure — contributing to baseline airway inflammation
5. Hypokalemia — beta-agonist-induced; repleted
6. Obesity — active comorbidity
7. Anxiety disorder — stable on escitalopram

DISCHARGE CONDITION
Stable. Peak flow 78% of personal best on room air. Speaks in full sentences. No accessory muscle use. SpO2 96% on room air. Wheezing significantly reduced. Ready for discharge with close pulmonary follow-up.

DISCHARGE MEDICATIONS
1. Budesonide-formoterol 160/4.5 mcg MDI — NEW controller therapy; 2 puffs TWICE daily every day (morning and night); this is your primary asthma preventer — do not stop even when you feel well
2. Albuterol 90 mcg MDI — rescue inhaler; use only for breakthrough symptoms; if using more than 2 days per week, call your doctor
3. Prednisone 60 mg orally daily — complete 5-day course; approximately 3 days remaining at discharge; take in the morning with food
4. Loratadine 10 mg orally daily — continue for rhinitis; consider daily (not as-needed) given allergen exposure
5. Escitalopram 10 mg orally daily — continued
6. Vitamin D 2000 IU orally daily — continued
7. Oral contraceptive — continued

DISCHARGE INSTRUCTIONS
Your asthma attack was triggered by a cold virus but made worse by the fact that your asthma was poorly controlled without a daily preventer medication. You now have a controller inhaler (budesonide-formoterol) that you must take EVERY DAY — morning and evening — even when you feel well. This is the most important change from this hospitalization. Your rescue inhaler (albuterol) is for sudden symptoms only. Follow your asthma action plan (attached). If your peak flow drops below 50% of personal best, use your rescue inhaler and go to the ER. Consider rehoming your cat or at minimum keeping it out of your bedroom and using a HEPA air purifier — pet dander is likely making your asthma worse daily.

FOLLOW-UP
1. Pulmonary Medicine (Dr. Osei): 1 week — peak flow check, steroid taper completion, inhaler technique
2. Allergy/Immunology: 4 weeks — allergen testing, immunotherapy evaluation
3. Spirometry (outpatient): 4–6 weeks — formal asthma classification
4. Primary Care: 2 weeks — prednisone complications monitoring, mental health follow-up""",
    },
    {
        "title": "Severe Hypothyroidism — Myxedema Features with Decompensation",
        "category": "Endocrinology / Internal Medicine",
        "expected_codes": ["E039"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Carolyn Steele, 55F | MRN: 1092847
Admission: 10/05/2025 | Discharge: 10/09/2025 | LOS: 4 days
Attending: Dr. N. Gupta, MD | Service: Endocrinology / Internal Medicine

CHIEF COMPLAINT
Progressive fatigue, cold intolerance, significant weight gain, constipation, and cognitive slowing over four months; TSH found to be markedly elevated at 148 mIU/L on outpatient labs prompting urgent admission.

HISTORY OF PRESENT ILLNESS
Ms. Steele is a 55-year-old woman with a known history of Hashimoto's thyroiditis and primary hypothyroidism on levothyroxine who presents following a call from her endocrinologist after outpatient thyroid function tests showed TSH 148 mIU/L and free T4 0.22 ng/dL (severely suppressed). She reports a four-month history of progressive and debilitating fatigue — she is sleeping 12–14 hours per day and still feels unrefreshed. She has gained 24 pounds over four months without dietary change. She reports extreme cold intolerance (wears a coat indoors in warm weather), dry and thickened skin, coarsened hair with diffuse hair loss, constipation requiring manual disimpaction twice over the past month, hoarse voice developing over several weeks, and cognitive slowing described as difficulty concentrating, slow thought processing, and word-finding difficulties that her husband describes as "she's not herself."

She has been on levothyroxine 100 mcg daily for six years with previously stable TSH values in the 1.5–2.5 mIU/L range. On detailed questioning, she discloses that she began taking her levothyroxine with her morning calcium supplement and coffee approximately five months ago — both significantly reduce levothyroxine absorption. Additionally, she started taking omeprazole four months ago for reflux symptoms — proton pump inhibitors reduce levothyroxine absorption by raising gastric pH. She was not counseled on the importance of proper levothyroxine administration when omeprazole was prescribed.

She denies fever, altered consciousness, seizure, or chest pain. She denies pericardial effusion symptoms. She denies thyroidectomy, radioactive iodine therapy, or neck irradiation. She denies recent iodine contrast exposure or amiodarone use.

On examination in clinic she was noted to have periorbital puffiness, coarse dry skin, non-pitting edema of the face and hands (myxedema), delayed relaxation phase of deep tendon reflexes, bradycardia (HR 52 bpm), and a mildly elevated blood pressure. She was admitted for IV levothyroxine therapy, monitoring for potential myxedema coma progression, and medication optimization.

PAST MEDICAL HISTORY
1. Primary hypothyroidism secondary to Hashimoto's thyroiditis — diagnosed 8 years ago; previously well-controlled on levothyroxine
2. Gastroesophageal reflux disease — omeprazole started 4 months ago (absorption interaction with levothyroxine)
3. Essential hypertension on lisinopril
4. Obesity, BMI 36
5. Mild depression on sertraline
6. Hyperlipidemia on rosuvastatin
7. Osteopenia by DEXA scan — calcium and vitamin D supplementation (now identified as levothyroxine absorption blocker)

PAST SURGICAL HISTORY
Laparoscopic cholecystectomy age 46. No thyroid surgery.

MEDICATIONS ON ADMISSION
1. Levothyroxine 100 mcg orally daily — taking with calcium supplement and coffee (absorption significantly reduced; must be taken on empty stomach 30–60 min before food/other meds)
2. Lisinopril 10 mg orally daily
3. Omeprazole 20 mg orally daily (4 months — reduces levothyroxine absorption)
4. Sertraline 50 mg orally daily
5. Rosuvastatin 20 mg orally nightly
6. Calcium carbonate 600 mg orally with morning medications (taken simultaneously with levothyroxine)
7. Vitamin D 1000 IU orally daily
8. Aspirin 81 mg orally daily

ALLERGIES
Iodine topical (contact dermatitis). No systemic iodine allergy. No other known drug allergies.

SOCIAL HISTORY
Insurance case manager. Married, lives with husband. One adult child. Nonsmoker. Rare alcohol — one to two drinks per month. No illicit drug use. Was previously active (yoga, walking) but has become largely sedentary over the past four months due to fatigue. Excellent health insurance (commercial). High health literacy — reports feeling "something was really wrong" for months.

FAMILY HISTORY
Mother has Hashimoto's thyroiditis. Sister has Graves' disease. Father had hypertension. Strong family history of autoimmune thyroid disease.

REVIEW OF SYSTEMS
Positive: extreme fatigue (sleeping 12–14 hours daily), 24-lb weight gain over 4 months, cold intolerance (wears coat indoors), dry thickened skin, coarse hair with diffuse loss, constipation (requiring manual disimpaction x2), hoarse voice (worsening over weeks), cognitive slowing (word-finding difficulty, slow processing), periorbital puffiness, facial and hand edema, myalgias, bradycardia noted on home pulse monitor (HR 48–55 bpm).
Negative: fever, chest pain, dyspnea at rest, altered consciousness, seizure, syncope, dysuria, abdominal pain, diarrhea.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 35.6°C (mild hypothermia), BP 148/92 mmHg, HR 52 bpm, RR 14 breaths/min, SpO2 96% RA, Wt 98 kg (from 74 kg 12 months ago — 24 kg weight gain)
General: Obese middle-aged woman with striking myxedematous appearance — facial puffiness, periorbital edema, expressionless facies. Alert but cognitively slowed. Speaks slowly and deliberately. Monotone voice, hoarse.
HEENT: Periorbital myxedema (non-pitting puffiness). Dry, dull, coarse skin texture. Sparse, coarse scalp hair — diffuse hair thinning. Macroglossia present — tongue mildly enlarged. Thyroid not enlarged on palpation (atrophic Hashimoto's). No goiter. No lymphadenopathy.
Cardiovascular: Bradycardic and regular. Heart sounds distant — possible pericardial effusion. No murmurs.
Pulmonary: Decreased breath sounds bilateral bases — possible pleural effusions. No wheeze.
Abdomen: Soft, mild diffuse tenderness, non-distended. Bowel sounds hypoactive. No organomegaly.
Extremities: Non-pitting edema of hands and dorsal feet (myxedema — not fluid overload). Skin dry, rough, yellowish-orange tint (carotenemia from reduced hepatic conversion of carotene).
Neurological: Alert, oriented x3 but slowed. Slow processing speed. DTRs 1+ with markedly delayed relaxation phase (characteristic hypothyroid finding — "hung-up reflexes"). No focal motor deficit. Cerebellar function intact.

LABORATORY DATA
TSH: 148 mIU/L (normal 0.4–4.0) — severely elevated; consistent with profound hypothyroidism
Free T4: 0.22 ng/dL (normal 0.8–1.8) — severely suppressed
Free T3: 1.2 pg/mL (normal 2.3–4.2) — very low
Anti-TPO antibody: 2,840 IU/mL — markedly elevated; confirms Hashimoto's thyroiditis
Anti-thyroglobulin antibody: 640 IU/mL — elevated
BMP: Na 128 mEq/L (hyponatremia — hypothyroid-related SIADH pattern), K 4.2, Cl 98, HCO3 23, BUN 16, Cr 0.9, Glucose 88 mg/dL
CBC: WBC 7.2, Hgb 10.8 g/dL (mild normocytic anemia of hypothyroidism), Hct 32.4%, MCV 88, Plt 188
Total cholesterol: 298 mg/dL, LDL 212, HDL 38, TG 264 — markedly elevated lipids from hypothyroidism (secondary hyperlipidemia — will normalize with treatment)
CK: 388 U/L — elevated; myopathy from hypothyroidism
Prolactin: 38 ng/mL — mildly elevated; hypothyroidism-induced hyperprolactinemia
Cortisol (AM): 18 mcg/dL — adequate adrenal reserve; no concomitant adrenal insufficiency
Troponin I: <0.02 — negative; no myocardial injury from bradycardia
BNP: 156 pg/mL — mildly elevated

Day 2: TSH 148 (unchanged — IV T4 requires days to shift TSH); Free T4 0.44 (improving)
Day 4 (Discharge): Free T4 0.61 (continuing upward trend); TSH will lag for weeks

IMAGING AND DIAGNOSTICS
ECG (Admission): Sinus bradycardia at 52 bpm. Low-voltage QRS throughout all leads — consistent with pericardial effusion and hypothyroid cardiomyopathy. Prolonged QT interval (QTc 486 ms). Flattened T-waves globally. No ST changes. No acute ischemia.
Echocardiogram (Hospital Day 1): LVEF 55%, preserved. Mild-to-moderate pericardial effusion (estimated 250 mL) — circumferential but without evidence of tamponade physiology (no respiratory variation in mitral inflow, no IVC plethora). Left ventricular wall thickness mildly increased (pseudohypertrophy from myxedema). No regional wall motion abnormality. Small bilateral pleural effusions.
Chest X-Ray: Mildly enlarged cardiac silhouette — consistent with pericardial effusion. Small bilateral pleural effusions. No pneumothorax. No consolidation.
Thyroid Ultrasound (Hospital Day 2): Atrophic, heterogeneous thyroid gland — right lobe 2.1 cm, left lobe 1.8 cm. Increased echogenicity and coarse echotexture consistent with Hashimoto's thyroiditis. No discrete nodule greater than 1 cm. No dominant nodule.

HOSPITAL COURSE
Ms. Steele was admitted for management of severe hypothyroidism with myxedema features, pericardial effusion, and hyponatremia. She did not meet criteria for myxedema coma (she was alert, not in shock, not in respiratory failure, temperature was mildly low but not profound) but required IV therapy given the severity of TSH elevation and clinical syndrome.

IV levothyroxine (T4) was initiated at a dose of 200 mcg on hospital day 1 (calculated as approximately 1.6 mcg/kg IV given her degree of depletion), followed by IV levothyroxine 75 mcg daily on days 2–3. In severe hypothyroidism, concurrent liothyronine (T3) was considered; given her preserved consciousness and hemodynamic stability, IV T4 alone was used with cardiac monitoring. Cardiac telemetry was maintained throughout given the prolonged QTc (486 ms) and bradycardia.

Hyponatremia (Na 128) was attributed to SIADH from hypothyroidism; free water restriction to 1 liter daily was implemented. Sodium improved to 134 by day 3 and 137 by day 4 with thyroid hormone supplementation. No hypertonic saline was required.

Bradycardia was monitored; rate ranged 48–56 bpm throughout admission without hemodynamic instability. No pacing was required. The pericardial effusion did not demonstrate tamponade physiology on serial echocardiography and echo was repeated on day 3 showing stable effusion — expected to resolve over weeks with thyroid hormone restoration.

Levothyroxine was transitioned to oral on day 3 at a dose of 150 mcg daily (increased from her prior 100 mcg, dosed correctly on an empty stomach). The most critical intervention was patient and family education: levothyroxine must be taken 30–60 minutes before any food, coffee, or other medications. Calcium supplements, antacids, PPIs, iron, and high-fiber foods should be taken at least 4 hours apart from levothyroxine.

Omeprazole was switched to famotidine (H2 blocker) — lower impact on levothyroxine absorption — given her GERD. She was instructed to take calcium supplement at bedtime (separated from morning levothyroxine by the entire day). The elevated cholesterol panel will be reassessed at 6–8 weeks after levothyroxine stabilization — secondary hyperlipidemia from hypothyroidism is expected to substantially improve. Rosuvastatin will be continued pending reassessment.

DISCHARGE DIAGNOSES
1. Hypothyroidism, unspecified — severe decompensated; TSH 148 mIU/L; myxedema features without coma; primary admission diagnosis
2. Pericardial effusion — hypothyroid-related; mild-to-moderate; no tamponade; monitoring required
3. Hyponatremia — hypothyroid-associated SIADH; resolved
4. Drug-absorption interaction — levothyroxine malabsorption from concurrent calcium supplement, coffee, and omeprazole intake; corrected by medication timing education
5. Secondary hyperlipidemia — hypothyroid-related; to be reassessed after euthyroid state established
6. Hypothyroid myopathy — elevated CK; expected to normalize
7. Mild normocytic anemia — hypothyroid-related; monitoring required
8. Essential hypertension — active comorbidity
9. Obesity — active comorbidity

DISCHARGE CONDITION
Improved. More alert and interactive by discharge. HR 56–62 bpm. BP 138/84 mmHg. Temperature normalized to 36.4°C. Free T4 trending up. Hyponatremia resolved. Tolerating oral levothyroxine at correct timing. Pericardial effusion stable, no tamponade.

DISCHARGE MEDICATIONS
1. Levothyroxine 150 mcg orally every morning on EMPTY STOMACH — 30–60 minutes BEFORE eating, coffee, or any other medication; INCREASED from 100 mcg; TIMING IS CRITICAL for absorption
2. Calcium carbonate 600 mg orally at BEDTIME — moved from morning to bedtime to separate from levothyroxine; take with small amount of food
3. Famotidine 20 mg orally twice daily — SUBSTITUTED for omeprazole (less absorption interference)
4. Lisinopril 10 mg orally daily — continued (in afternoon, separated from levothyroxine)
5. Sertraline 50 mg orally daily — continued (take in afternoon, separated from levothyroxine)
6. Rosuvastatin 20 mg orally nightly — continued; cholesterol panel to be repeated at 8 weeks
7. Vitamin D 1000 IU orally daily — take at bedtime with calcium
8. Aspirin 81 mg orally daily — continue; take in afternoon separated from levothyroxine

DISCHARGE INSTRUCTIONS
Your thyroid gland was severely underactive because your thyroid medication was not being absorbed properly. This happened because you were taking it at the same time as calcium, coffee, and a stomach acid medication — all of which block absorption. You now have a higher dose of levothyroxine and clear instructions: take it FIRST THING in the morning, on an empty stomach, 30–60 minutes before eating or taking any other medication or coffee. This single change is critical to your recovery. You will feel better gradually over the next 4–8 weeks. Do not expect overnight improvement. You have a fluid collection around your heart that should shrink as your thyroid levels improve. Report any new chest pain, shortness of breath, or leg swelling immediately. Keep all follow-up appointments.

FOLLOW-UP
1. Endocrinology (Dr. Gupta): 4 weeks — TSH, free T4 recheck; levothyroxine dose adjustment anticipated
2. Cardiology: 6 weeks — repeat echocardiogram to confirm pericardial effusion resolution
3. Primary Care: 2 weeks — sodium recheck, blood pressure, anemia follow-up
4. Lipid panel recheck: 8 weeks — after thyroid state normalizes""",
    },
    {
        "title": "Hyponatremia — Syndrome of Inappropriate Antidiuretic Hormone (SIADH)",
        "category": "Nephrology / Internal Medicine",
        "expected_codes": ["E871"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Frank Deluca, 70M | MRN: 2038471
Admission: 09/30/2025 | Discharge: 10/04/2025 | LOS: 4 days
Attending: Dr. S. Kim, MD | Service: Internal Medicine / Nephrology

CHIEF COMPLAINT
Confusion, nausea, and unsteady gait for two days; found to have sodium 118 mEq/L in the emergency department.

HISTORY OF PRESENT ILLNESS
Mr. Deluca is a 70-year-old man with a history of small cell lung cancer (SCLC) diagnosed three months ago, currently receiving chemotherapy (carboplatin and etoposide, cycle 3 completed two weeks ago), hypertension, and type 2 diabetes mellitus who presents with a two-day history of progressive confusion noted by his wife — she describes him as disoriented, unable to recall what he had eaten that day, slow to respond to questions, and unsteady on his feet when walking. He denies frank loss of consciousness, seizure activity, or focal weakness. He reports mild nausea and one episode of non-bloody vomiting this morning. He has had headache for three days, which he initially attributed to chemotherapy-related side effects.

His sodium was checked by his oncologist's office two weeks ago and was 128 mEq/L, at which time the team recommended fluid restriction to 1 liter daily and he was thought to have early SIADH from SCLC (ectopic ADH production is a classic paraneoplastic syndrome of SCLC). He discloses that he was not strictly adhering to the 1-liter fluid restriction, as he felt thirsty and believed drinking water was beneficial during chemotherapy. He has not started any new medications. He has no history of adrenal insufficiency, hypothyroidism, heart failure, liver disease, or nephrotic syndrome. He denies new neurological symptoms prior to this admission beyond what is described.

On arrival to the emergency department, he was disoriented to date and location. Serum sodium was 118 mEq/L — severely symptomatic hyponatremia. Serum osmolality was 247 mOsm/kg (hypotonic). Urine osmolality was 620 mOsm/kg (inappropriately concentrated). Urine sodium was 68 mEq/L (elevated). Volume status was euvolemic by examination. These findings are consistent with SIADH from ectopic ADH production by the SCLC. He was admitted for careful sodium correction and inpatient fluid restriction.

PAST MEDICAL HISTORY
1. Small cell lung cancer (SCLC), limited stage — diagnosed 3 months ago; currently on carboplatin/etoposide chemotherapy, cycle 3 completed 2 weeks prior
2. SIADH — paraneoplastic syndrome from SCLC; sodium 128 noted 2 weeks prior; outpatient fluid restriction non-adherent
3. Essential hypertension on lisinopril
4. Type 2 diabetes mellitus on metformin
5. Chronic obstructive pulmonary disease — GOLD Stage II; former smoker; on tiotropium
6. Peripheral neuropathy — bilateral lower extremities, attributed to chemotherapy (carboplatin)
7. Depression — on sertraline (SSRIs can also contribute to SIADH)

PAST SURGICAL HISTORY
Appendectomy age 32. No thoracic surgeries. Bronchoscopy with biopsy (SCLC diagnosis), outpatient.

MEDICATIONS ON ADMISSION
1. Lisinopril 10 mg orally daily
2. Metformin 500 mg orally twice daily
3. Tiotropium 18 mcg inhaled once daily
4. Sertraline 50 mg orally daily — possible minor SIADH contributor; reviewed with oncology
5. Ondansetron 4 mg orally every 8 hours as needed (post-chemotherapy antiemetic)
6. Dexamethasone 4 mg orally twice daily — prescribed for chemotherapy-related nausea; last 5-day course completed 10 days ago
7. Gabapentin 300 mg orally three times daily (peripheral neuropathy)

ALLERGIES
No known drug allergies.

SOCIAL HISTORY
Retired truck driver. Married, lives with wife in a single-story home. Two adult children. Former heavy smoker — 50 pack-year history, quit 3 years ago at lung cancer diagnosis. Social alcohol — stopped at cancer diagnosis. No illicit drug use. Limited mobility due to peripheral neuropathy and fatigue from chemotherapy. Medicare with supplemental insurance.

FAMILY HISTORY
Father had lung cancer (smoker). Mother had hypertension and diabetes. One sibling with COPD.

REVIEW OF SYSTEMS
Positive: confusion (progressive over 2 days), disorientation, nausea, vomiting (x1), headache (3 days), unsteady gait, fatigue.
Negative: seizure, focal weakness, facial droop, visual changes, chest pain, fever, cough worsening from baseline, hemoptysis, dyspnea at rest, dysuria, gross hematuria, abdominal pain, diarrhea.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 36.8°C, BP 132/80 mmHg, HR 78 bpm, RR 16 breaths/min, SpO2 95% RA, Wt 72 kg
General: Thin elderly man in mild distress, confused. Oriented to person only. Responds to voice. Not combative.
HEENT: Mucous membranes moist. No JVD. No lymphadenopathy. No papilledema on fundoscopic exam.
Cardiovascular: Regular rate and rhythm. S1 and S2. No murmurs.
Pulmonary: Diminished breath sounds left lower lobe (known primary tumor). Mild scattered expiratory wheeze. No crackles.
Abdomen: Soft, non-tender, non-distended. No organomegaly. Normoactive bowel sounds.
Extremities: No lower extremity edema. Peripheral pulses 2+. Diminished sensation bilateral feet and ankles (peripheral neuropathy).
Neurological: Disoriented to date and place. Responds to name. Follows simple commands. No focal motor deficit. Mild ataxia on finger-nose testing. Gait unsteady — assisted. No Babinski.

LABORATORY DATA
Serum sodium: 118 mEq/L — severely low (symptomatic hyponatremia <125)
Serum osmolality: 247 mOsm/kg — hypotonic (confirms true hyponatremia, not pseudohyponatremia)
Urine osmolality: 620 mOsm/kg — inappropriately concentrated despite hypoosmolality; confirms ADH excess
Urine sodium: 68 mEq/L — elevated; confirms renal sodium excretion (euvolemic SIADH vs. cerebral salt wasting)
BMP: Na 118, K 3.8, Cl 84, HCO3 24, BUN 10, Cr 0.8, Glucose 142 — hyponatremia confirmed; BUN:Cr ratio 12.5 (low-normal; consistent with euvolemia, not dehydration)
CBC: WBC 4.2 K/uL (mild leukopenia from chemotherapy), Hgb 10.4 g/dL (chemotherapy-related anemia), Hct 31.2%, Plt 128 K/uL — mild thrombocytopenia
TSH: 1.9 mIU/L — normal; hypothyroidism excluded as cause of hyponatremia
AM Cortisol: 22 mcg/dL — normal; adrenal insufficiency excluded
HbA1c: 7.1%
Troponin: <0.02

Correction monitoring:
Hour 0: Na 118
Hour 6: Na 121 (rate 0.5 mEq/L/h — appropriate, within target <0.5 mEq/L/h acute phase)
Hour 12: Na 123
Day 2 (24h): Na 126 — total correction 8 mEq/L in 24 hours (target <10–12 mEq/L to prevent osmotic demyelination)
Day 3: Na 131
Day 4 (Discharge): Na 134

IMAGING AND DIAGNOSTICS
CT Head without contrast (Hospital Day 1, due to confusion and fall risk): No acute intracranial hemorrhage. No ischemic changes. No brain metastases identified. Mild cortical atrophy appropriate for age. No hydrocephalus. No midline shift. (Note: MRI brain with gadolinium preferred for metastasis screening in SCLC; outpatient MRI brain ordered.)
MRI Brain with gadolinium (Ordered for outpatient, not performed during this admission due to acute Na management priority): Will be performed within 2 weeks post-discharge.
Chest X-Ray: Known left hilar mass and left lower lobe atelectasis related to SCLC — unchanged from prior imaging. No new infiltrate. No pneumothorax.

HOSPITAL COURSE
Mr. Deluca was admitted to a monitored internal medicine bed for management of severe symptomatic hyponatremia (Na 118 mEq/L) attributed to SIADH from ectopic ADH production by his SCLC, compounded by SSRI use (sertraline) and non-adherence to fluid restriction.

The primary treatment was strict fluid restriction to 500 mL total daily fluid intake. Hypertonic saline (3% NaCl) was not initiated given the absence of seizure, coma, or acute respiratory failure — current guidelines support fluid restriction as the primary treatment for chronic SIADH when the patient has symptomatic but not life-threatening hyponatremia. IV normal saline was avoided as this can worsen SIADH if urine osmolality exceeds plasma osmolality (urine 620 vs. plasma 247 mOsm/kg — a state where isotonic saline would exacerbate hyponatremia).

Sodium correction rate was monitored every 6 hours to ensure the rate did not exceed 10–12 mEq/L per 24 hours to prevent osmotic demyelination syndrome. Total correction over 24 hours was 8 mEq/L (appropriate). Fluid restriction was maintained throughout. Salt tablets (sodium chloride 1g three times daily) were added on day 2 to accelerate correction while maintaining fluid restriction.

Oral tolvaptan (a V2 receptor antagonist) was considered for treatment-refractory SIADH; however, given improvement with fluid restriction by day 2, tolvaptan was deferred and reserved for outpatient use if sodium fails to maintain correction after discharge. Oncology was involved throughout and endorsed tolvaptan as an option for outpatient management if SIADH persists despite optimal fluid restriction.

Sertraline was maintained at the same dose (benefit for depression during cancer treatment outweighs the marginal SIADH contribution). Oncology was informed.

Mental status improved substantially by day 2 (sodium 126 mEq/L) — he was oriented x2 by day 2 and x3 by day 3. Gait improved with physical therapy evaluation; no fall occurred during admission. He was cleared by occupational therapy for home discharge with family supervision and fall precautions.

Comprehensive patient and wife education on strict fluid restriction (1,000 mL daily maximum — including soups, ice cream, juice, coffee) was provided. Written instructions were given. A fluid tally chart was provided to the family. Follow-up sodium check was arranged for 48 hours post-discharge.

DISCHARGE DIAGNOSES
1. Hypo-osmolality and hyponatremia — severe symptomatic hyponatremia, Na 118 mEq/L; SIADH from paraneoplastic ectopic ADH production by SCLC; primary admission diagnosis
2. Syndrome of inappropriate antidiuretic hormone secretion (SIADH) — paraneoplastic from small cell lung cancer; non-adherence to fluid restriction as precipitant of acute decompensation
3. Small cell lung cancer, limited stage — active treatment, paraneoplastic syndrome
4. Confusion and gait instability — resolved with sodium correction
5. SSRI-related SIADH contribution — sertraline continued; minor contributor
6. Type 2 diabetes mellitus — active comorbidity
7. Essential hypertension — active comorbidity
8. Chemotherapy-induced peripheral neuropathy — active comorbidity
9. COPD, GOLD Stage II — active comorbidity

DISCHARGE CONDITION
Improved. Sodium 134 mEq/L at discharge. Alert and oriented x3. Gait improved; requires supervision. Tolerating strict fluid restriction. Tolerating oral medications.

DISCHARGE MEDICATIONS
1. Sodium chloride 1g orally three times daily — NEW; continue until oncology/nephrology stops
2. Sertraline 50 mg orally daily — continued; take in morning
3. Lisinopril 10 mg orally daily — continued; take in afternoon
4. Metformin 500 mg orally twice daily — continued
5. Tiotropium 18 mcg inhaled once daily — continued
6. Gabapentin 300 mg orally three times daily — continued
7. Ondansetron 4 mg orally as needed for nausea — continued

DISCHARGE INSTRUCTIONS
Your salt level (sodium) was critically low because your lung cancer was producing a hormone that caused your kidneys to retain too much water. The treatment is strict fluid restriction. You may drink NO MORE THAN 4 cups (1,000 mL) of any fluid total per day — this includes water, coffee, juice, milk, soup, ice cream, and anything liquid. This is extremely important. Too much fluid will cause your sodium to fall again. Have your sodium checked in two days. If you develop confusion, seizures, or are unable to walk, go to the emergency department immediately. Take the salt tablets as prescribed.

FOLLOW-UP
1. Nephrology (Dr. Kim): 48 hours post-discharge — sodium recheck; tolvaptan discussion if level drops
2. Oncology: 1 week — sodium management within cancer treatment plan; next chemo cycle planning
3. Neurology: 2 weeks — MRI brain with gadolinium (metastasis screening)
4. Primary Care: 2 weeks — blood pressure, diabetes""",
    },
    {
        "title": "Metabolic Acidosis — Non-Anion Gap, CKD-Related",
        "category": "Nephrology / Internal Medicine",
        "expected_codes": ["E872"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Donna Barrett, 63F | MRN: 3081924
Admission: 11/10/2025 | Discharge: 11/14/2025 | LOS: 4 days
Attending: Dr. R. Larsen, MD | Service: Nephrology / Internal Medicine

CHIEF COMPLAINT
Fatigue, weakness, shortness of breath on exertion, and rapid shallow breathing found on outpatient visit; labs showing bicarbonate 11 mEq/L and pH 7.22 on ABG.

HISTORY OF PRESENT ILLNESS
Ms. Barrett is a 63-year-old woman with stage 4 chronic kidney disease (eGFR 22 mL/min/1.73m², baseline eGFR 25–28 over the past year), type 2 diabetes mellitus, and hypertension who was evaluated by her nephrologist for a routine quarterly visit and found to have severe metabolic acidosis on venous blood gas and BMP. She reports a three-week history of progressive fatigue, generalized weakness, exertional dyspnea with minimal activity, and rapid breathing. She initially attributed these symptoms to her known CKD and did not contact her nephrologist earlier. Over the past week she has had markedly decreased appetite, mild nausea, and difficulty performing her usual household activities.

She was already on sodium bicarbonate supplementation (sodium bicarbonate 650 mg three times daily) as per her CKD-associated metabolic acidosis management protocol. On further questioning, she had been reducing her sodium bicarbonate intake because the pills were causing her bloating and gas — she was taking one tablet daily instead of three. She has also been under significant stress related to a family illness, and her dietary intake has become less balanced with higher protein intake (protein catabolism worsens acid load).

Her nephrologist obtained a venous blood gas in office showing pH 7.22, HCO3 11 mEq/L, and a complete metabolic panel showing Na 136, HCO3 10, Cr 4.2 (acute worsening from baseline 3.8). She was sent directly to the emergency department for IV bicarbonate therapy and admission for workup of acute-on-chronic metabolic acidosis and CKD exacerbation.

She denies diarrhea, vomiting, or other gastrointestinal losses. She denies aspirin overdose, methanol or ethylene glycol ingestion, and new medications. She denies chest pain or palpitations. She has not had a contrast study recently. She is not on metformin (held three months ago when eGFR dropped below 30).

PAST MEDICAL HISTORY
1. Chronic kidney disease Stage 4 (eGFR 22–28), presumed diabetic nephropathy
2. Type 2 diabetes mellitus — insulin-requiring; HbA1c 8.4% at last check
3. Essential hypertension on amlodipine and losartan
4. Metabolic acidosis — CKD-related; on sodium bicarbonate supplementation (non-adherent x3 weeks)
5. Anemia of chronic kidney disease — on darbepoetin alfa subcutaneous monthly
6. Secondary hyperparathyroidism — on calcitriol and sevelamer
7. Peripheral diabetic neuropathy — on gabapentin
8. Hyperlipidemia on rosuvastatin
9. Obesity, BMI 32

PAST SURGICAL HISTORY
Bilateral knee arthroplasty (left age 56, right age 59). Hysterectomy age 48.

MEDICATIONS ON ADMISSION
1. Insulin glargine 30 units subcutaneously at bedtime
2. Insulin lispro 6 units subcutaneously with meals (and correction scale)
3. Amlodipine 10 mg orally daily
4. Losartan 100 mg orally daily — held on admission given acute CKD worsening
5. Sodium bicarbonate 650 mg orally THREE times daily — taking once daily only (non-adherent)
6. Sevelamer 800 mg orally three times daily with meals
7. Calcitriol 0.25 mcg orally daily
8. Darbepoetin alfa 40 mcg subcutaneously monthly
9. Rosuvastatin 20 mg orally nightly
10. Gabapentin 200 mg orally three times daily (dose-reduced for CKD)
11. Aspirin 81 mg orally daily

ALLERGIES
Sulfonamides (rash). Penicillin (angioedema — documented; use cephalosporins with caution).

SOCIAL HISTORY
Retired elementary school teacher. Lives with her husband. Two adult children. Nonsmoker. No alcohol — stopped when CKD diagnosed. No illicit drug use. Diet includes moderate dietary sodium restriction with moderate protein; recent higher protein intake. Medicare and Medicaid dual coverage.

FAMILY HISTORY
Mother had end-stage renal disease on hemodialysis — died age 72. Father had type 2 diabetes. One sibling on hemodialysis (diabetic nephropathy). Strong family history of CKD.

REVIEW OF SYSTEMS
Positive: progressive fatigue (3 weeks), generalized weakness, dyspnea on exertion (even minimal activity), rapid breathing, decreased appetite, nausea, difficulty with household activities, bloating (from bicarbonate tablets, causing non-adherence).
Negative: vomiting, diarrhea, fever, chest pain, palpitations, syncope, edema (stable chronic), focal neurological deficits, diarrhea, decreased urine output (she is still making urine — non-oliguric CKD).

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 36.7°C, BP 162/98 mmHg, HR 98 bpm (mild compensatory tachycardia), RR 22 breaths/min (Kussmaul breathing pattern — deep, rapid breathing as respiratory compensation for metabolic acidosis), SpO2 95% RA, Wt 88 kg
General: Obese middle-aged woman in moderate distress — notably tachypneic and fatigued. Alert and oriented x3. Using intercostal muscles to breathe but no accessory muscle recruitment at neck.
HEENT: Pale conjunctiva. Dry mucous membranes. No JVD. No lymphadenopathy.
Cardiovascular: Tachycardic and regular. S1 and S2. No murmurs. No S3.
Pulmonary: Clear to auscultation bilaterally. Deep, regular, rapid breathing pattern — Kussmaul respirations. No wheeze or crackles.
Abdomen: Soft, mildly distended. Normoactive bowel sounds. Mild diffuse tenderness without guarding or rebound. No organomegaly.
Extremities: 1+ bilateral lower extremity edema (chronic stable). Peripheral pulses 2+. Diminished monofilament sensation bilateral feet (known neuropathy).
Neurological: Alert and oriented x3. No focal deficits. No asterixis. DTRs 1+ symmetric.

LABORATORY DATA
Venous Blood Gas (Outpatient, Nephrology Office): pH 7.22, pCO2 26 mmHg (appropriate respiratory compensation: expected pCO2 = 1.5 × HCO3 + 8 ± 2 = 1.5 × 11 + 8 = 24.5 — observed 26, appropriate compensation), HCO3 11 mEq/L — severe pure metabolic acidosis with appropriate respiratory compensation
BMP (Admission): Na 136, K 5.4 mEq/L (hyperkalemia — CKD-related), Cl 110, HCO3 10 mEq/L, BUN 88, Cr 4.2 mg/dL (worsened from baseline 3.8), Glucose 218 mg/dL
Anion gap: Na − (Cl + HCO3) = 136 − (110 + 10) = 16 mEq/L — mildly elevated anion gap (borderline; accounting for albumin correction: albumin 2.9, corrected AG = 16 + 2.5 × (4 − 2.9) = 18.75 — mildly elevated; mixed gap/non-gap)
Delta ratio: (AG − 12) / (24 − HCO3) = 4/14 = 0.29 — consistent with predominantly non-anion gap metabolic acidosis (type IV RTA pattern from advanced CKD, hyperkalemia)
Urine anion gap: (Urine Na + K) − Urine Cl = (42 + 38) − 22 = +58 — positive; consistent with distal tubular ammonium excretion impairment (type IV renal tubular acidosis from aldosterone effect reduction by advanced CKD)
CBC: WBC 8.4, Hgb 9.2 g/dL (anemia of CKD), Hct 27.6%, MCV 84, Plt 188
Phosphorus: 6.8 mg/dL — hyperphosphatemia (sevelamer non-optimal timing)
Calcium: 8.2 mg/dL — borderline low
iPTH: 248 pg/mL — elevated, secondary hyperparathyroidism
HbA1c: 8.4%
Urine toxicology: Negative — ingestion excluded

Day 2 BMP: Na 138, K 5.0, HCO3 14, BUN 76, Cr 4.0
Discharge BMP: Na 140, K 4.8, HCO3 19, BUN 68, Cr 3.9 (approaching baseline)

IMAGING AND DIAGNOSTICS
ECG (Admission): Sinus tachycardia at 98 bpm. Peaked T-waves V2–V5 — hyperkalemia pattern. Mildly prolonged PR (208 ms). No sine wave morphology. No acute ischemic changes.
ECG (Day 2): Sinus rhythm 80 bpm. T-wave peaking improved. PR 190 ms. No acute changes.
Renal Ultrasound (Hospital Day 1): Bilateral kidneys small and echogenic — right 8.2 cm, left 8.6 cm; consistent with advanced chronic kidney disease and loss of cortical mass. No hydronephrosis. No renal calculi. No acute obstruction.
Chest X-Ray: Mild cardiomegaly. No pulmonary edema. No pleural effusions. No consolidation.

HOSPITAL COURSE
Ms. Barrett was admitted to the nephrology service for management of severe metabolic acidosis (pH 7.22, HCO3 10) in the setting of advanced CKD Stage 4, attributable to bicarbonate depletion from non-adherence to sodium bicarbonate supplementation compounded by high protein dietary intake and mild CKD progression (Cr 4.2 from baseline 3.8 — likely mild prerenal component and disease progression).

IV sodium bicarbonate was initiated: isotonic sodium bicarbonate (150 mEq in 1L D5W) was infused at 150 mL/hour for the first 6 hours, providing 22.5 mEq bicarbonate per hour, then transitioned to oral therapy when the patient was tolerating fluids. The volume of bicarbonate was calculated based on estimated bicarbonate space deficit: 0.5 × weight × (target HCO3 − current HCO3) = 0.5 × 88 × (18 − 10) = 352 mEq total deficit; partial correction to target HCO3 18–20 mEq/L (not fully normalized, to avoid overshoot in a CKD patient).

Hyperkalemia (K 5.4) with ECG changes was managed with calcium gluconate 1g IV for membrane stabilization, then patiromer 8.4g orally once for acute reduction. Potassium declined from 5.4 to 5.0 by day 2 with bicarbonate therapy (acidosis correction shifts potassium intracellularly) and to 4.8 by discharge.

Losartan was held for the first two days during the acute acidosis management and renal stress, then resumed on day 3 when creatinine improved to 3.9. IV fluids were infused to gently address mild prerenal component; goal was euvolemia without volume overload.

Oral sodium bicarbonate dose was optimized: the patient had been experiencing GI side effects (bloating and gas) from her current formulation. The team switched to sodium bicarbonate 1300 mg (two 650mg tablets) twice daily instead of 650 mg three times daily — same total daily dose with different dosing frequency to reduce the peak gas production. Simethicone was added for GI comfort.

The patient was counseled extensively on the life-threatening consequences of metabolic acidosis in CKD: it accelerates CKD progression, worsens bone disease, contributes to muscle catabolism, and impairs insulin sensitivity. The mandatory nature of bicarbonate supplementation was emphasized. Dietary consultation was placed for lower protein and potassium diet education.

Nephrology documented that hemodialysis planning is recommended to begin within the next 6–12 months given eGFR 22 and the trend of progression. The patient was referred to the CKD Stage 4–5 transition education program, which includes AV fistula consultation and renal transplant evaluation.

DISCHARGE DIAGNOSES
1. Metabolic acidosis — severe; pH 7.22, HCO3 10 mEq/L; non-anion gap (type IV RTA pattern) predominantly; CKD-related with bicarbonate supplementation non-adherence as precipitant; primary admission diagnosis
2. Chronic kidney disease Stage 4 — eGFR 22, acute-on-chronic worsening (Cr 4.2 from 3.8 baseline)
3. Hyperkalemia — resolved with bicarbonate therapy and patiromer
4. Secondary hyperparathyroidism — ongoing management
5. Anemia of chronic kidney disease — stable on darbepoetin
6. Type 2 diabetes mellitus — active comorbidity
7. Essential hypertension — active comorbidity
8. Hyperphosphatemia — managed with sevelamer
9. Medication non-adherence (sodium bicarbonate) — primary precipitant

DISCHARGE CONDITION
Improved. pH 7.38 on repeat VBG at discharge. HCO3 19 mEq/L. Respiratory rate 16 (resolved Kussmaul pattern). Potassium 4.8. Alert, oriented, fatigue significantly improved. Tolerating all oral medications with improved GI comfort.

DISCHARGE MEDICATIONS
1. Sodium bicarbonate 1300 mg (two 650 mg tablets) orally TWICE daily — dose restructured; total daily dose same; MUST take as prescribed; this medication keeps your blood from becoming too acidic
2. Simethicone 125 mg orally after each sodium bicarbonate dose — NEW; for GI comfort with bicarbonate
3. Patiromer 8.4g orally daily with food — continue for potassium management
4. Insulin glargine 30 units subcutaneously at bedtime — continued
5. Insulin lispro 6 units with meals — continued
6. Losartan 100 mg orally daily — RESUMED; do not stop without nephrologist guidance
7. Amlodipine 10 mg orally daily — continued
8. Sevelamer 800 mg orally three times daily with meals — continued
9. Calcitriol 0.25 mcg orally daily — continued
10. Darbepoetin alfa 40 mcg subcutaneously monthly — continued (injection due next Monday)
11. Rosuvastatin 20 mg orally nightly — continued
12. Gabapentin 200 mg orally three times daily — continued

DISCHARGE INSTRUCTIONS
You were admitted because your blood became too acidic (metabolic acidosis) — this happened because you stopped taking your baking soda tablets regularly. Those tablets are not optional — they are as important as any of your other kidney medications. Without them, your blood becomes dangerously acidic, which is what caused your fatigue, weakness, and fast breathing. We changed the dosing to twice a day instead of three times a day (same total amount) and added a gas-reducing tablet to make them more comfortable. Your kidneys are significantly advanced in their disease. It is time to begin planning for dialysis — please attend the kidney education session your nephrologist has arranged. Do not skip any nephrology appointments.

FOLLOW-UP
1. Nephrology (Dr. Larsen): 1 week — BMP, VBG, creatinine, potassium; medication adjustment
2. CKD Transition Education Program: 2 weeks — AV fistula consultation, RRT planning, transplant evaluation
3. Dietary counseling: 2 weeks — low-protein, low-potassium, low-phosphorus diet reinforcement
4. Primary Care: 2 weeks — insulin management, blood pressure""",
    },
    {
        "title": "Acute Posthemorrhagic Anemia — Upper GI Bleed from Peptic Ulcer Disease",
        "category": "Gastroenterology / Internal Medicine",
        "expected_codes": ["D62"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Raymond Schultz, 67M | MRN: 4192038
Admission: 10/18/2025 | Discharge: 10/22/2025 | LOS: 4 days
Attending: Dr. F. Huang, MD | Service: Gastroenterology / Internal Medicine

CHIEF COMPLAINT
Hematemesis (vomiting blood) and lightheadedness; hemoglobin 7.2 g/dL on arrival to the emergency department.

HISTORY OF PRESENT ILLNESS
Mr. Schultz is a 67-year-old man with a history of hypertension, atrial fibrillation on apixaban, and osteoarthritis who presents with a four-hour history of two episodes of hematemesis — the first consisting of bright red blood mixed with clots, the second largely coffee-ground material. He reports accompanying lightheadedness and dizziness on standing, mild diaphoresis, and weakness. He denies frank melena or bright red blood per rectum, though his wife notes his last bowel movement the day prior appeared dark and malodorous — consistent with melena in retrospect. He denies abdominal pain, which he finds reassuring but is atypical and may reflect an inactive or recently healed ulcer base.

He reports taking ibuprofen 800 mg three times daily for the past four weeks for severe right knee osteoarthritis pain — his orthopedist had discussed the scheduled knee replacement surgery but he was trying to manage pain in the meantime. He was not on a proton pump inhibitor. He is on apixaban 5 mg twice daily for atrial fibrillation. He denies taking aspirin or other antiplatelet agents. He denies excessive alcohol use. He denies prior peptic ulcer disease, prior upper GI bleed, or H. pylori infection history. He denies recent weight loss, early satiety, dysphagia, or odynophagia.

In the emergency department, he was pale, diaphoretic, and orthostatic — blood pressure 108/68 supine and 84/52 upright, heart rate 118 bpm. Hemoglobin was 7.2 g/dL (baseline unknown; estimated 13–14 based on recent outpatient CBC 8 months prior: 13.8). Apixaban was last taken 7 hours prior. Two large-bore peripheral IVs were placed, IV fluid resuscitation initiated with normal saline, and a GI consult was placed urgently. He was admitted to a monitored bed for emergent endoscopy.

PAST MEDICAL HISTORY
1. Atrial fibrillation on apixaban anticoagulation
2. Essential hypertension on metoprolol and lisinopril
3. Osteoarthritis — bilateral knees; right knee scheduled for arthroplasty
4. Hyperlipidemia on atorvastatin
5. No prior peptic ulcer disease
6. No prior GI bleeding
7. Obesity, BMI 31

PAST SURGICAL HISTORY
Appendectomy age 28. Left knee arthroplasty age 62 — uncomplicated. Cataract surgery bilateral, remote.

MEDICATIONS ON ADMISSION
1. Apixaban 5 mg orally twice daily — held on admission for GI bleed; reversal agent considered
2. Metoprolol succinate 50 mg orally daily
3. Lisinopril 20 mg orally daily — held initially given hypotension
4. Atorvastatin 40 mg orally nightly
5. Ibuprofen 800 mg orally three times daily — STOPPED; identified as precipitant; never to be used again
6. Acetaminophen 500 mg orally as needed — he was using this in addition to ibuprofen, not as a replacement

ALLERGIES
No known drug allergies.

SOCIAL HISTORY
Retired construction foreman. Married, lives with wife. Three adult children. Former smoker — 20 pack-year history, quit 12 years ago. Moderate alcohol — two to three drinks per week. No illicit drug use. Diet is unrestricted. Commercial insurance (through retiree benefit).

FAMILY HISTORY
Father had peptic ulcer disease. Mother had hypertension. One sibling with colon cancer — colonoscopy screening up to date (last 3 years ago, one tubular adenoma, next due in 1 year).

REVIEW OF SYSTEMS
Positive: hematemesis (x2 episodes — bright red and coffee-ground), lightheadedness, orthostasis, diaphoresis, weakness, dark malodorous stool prior day (melena in retrospect).
Negative: abdominal pain, dysphagia, odynophagia, hematochezia (bright red blood per rectum), significant weight loss, early satiety, prior ulcer or GI bleed history, fever.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 36.8°C, BP 108/68 mmHg supine (84/52 orthostatic), HR 118 bpm, RR 18 breaths/min, SpO2 97% RA, Wt 92 kg
General: Pale, diaphoretic man in mild-to-moderate distress. Alert and oriented x3. Appears volume-depleted.
HEENT: Pale conjunctiva. Dry mucous membranes. No JVD. No lymphadenopathy.
Cardiovascular: Tachycardic and regular. No murmurs.
Pulmonary: Clear bilaterally.
Abdomen: Soft, mild epigastric tenderness to deep palpation. No guarding or rebound. No organomegaly. Normoactive bowel sounds. No signs of peritonitis.
Rectal examination: Dark brown, guaiac-positive stool — melena confirmed.
Extremities: No lower extremity edema. Peripheral pulses weak but present bilaterally. Capillary refill 3 seconds.
Neurological: Alert and oriented x3. No focal deficits. No asterixis.

LABORATORY DATA
CBC (Admission): WBC 12.4 K/uL (stress leukocytosis), Hgb 7.2 g/dL (estimated acute posthemorrhagic from baseline ~13.8 — approximately 6.6 g/dL drop, significant blood loss), Hct 21.6%, MCV 82, Plt 228 K/uL
BMP: Na 138, K 3.4 (mild hypokalemia), Cl 104, HCO3 22, BUN 52 mg/dL (elevated — upper GI bleed; BUN rises from protein absorption of blood), Cr 1.1, Glucose 162 mg/dL; BUN:Cr ratio 47 — consistent with upper GI bleeding
Coagulation: PT/INR 1.0 (apixaban does not significantly prolong INR at standard doses); aPTT 34 s; anti-Xa level: 78 ng/mL (within apixaban therapeutic range — confirms active drug on board)
Anti-Xa reversal agent: Andexanet alfa discussed by GI/hematology; given hemodynamic response to fluids and ability to proceed with endoscopy, andexanet alfa was not required — the apixaban was simply held and endoscopic hemostasis was achieved
Troponin I: <0.02
Helicobacter pylori serology: Positive (IgG antibody) — H. pylori eradication therapy planned
H. pylori stool antigen (confirmatory): Positive
Urea breath test (pre-endoscopy): Not performed (active bleed); stool antigen used for diagnosis
Type and Screen: Blood type O positive; 2 units pRBC crossmatched

Post-transfusion Day 2 CBC: Hgb 9.4, Hct 28.2% (after 2 units pRBC)
Discharge CBC: Hgb 10.2, Hct 30.6%

IMAGING AND DIAGNOSTICS
Esophagogastroduodenoscopy (Hospital Day 1, Emergent): Stomach: Grade C erosive gastritis (Lanza score) in the antrum and body, multiple erosions — NSAID-related gastropathy. Duodenum: 1.2 cm ulcer on the posterior wall of the duodenal bulb with a visible vessel (Forrest Class IIa — non-bleeding visible vessel, high risk of rebleed). Endoscopic therapy: epinephrine injection (1:10,000, total 10 mL) around the visible vessel base followed by hemostatic clip placement (2 clips applied). Adequate hemostasis achieved. Retroflexion of scope in stomach showed Grade C gastritis but no active bleeding site in the stomach. No varices. No malignant-appearing lesion. Duodenal ulcer biopsied.
Second-look Endoscopy (Hospital Day 2, planned): Duodenal ulcer — clips in place, no active bleeding, no visible vessel, Forrest Class III. No rebleeding. Gastritis improved with IV PPI.
Chest X-Ray: No free air under the diaphragm (excludes perforation). No pneumonia. No pulmonary edema.
CT Abdomen/Pelvis (Not required; reserved if rebleeding or perforation suspected): Not performed.

HOSPITAL COURSE
Mr. Schultz was admitted for management of acute upper GI bleed secondary to NSAID-induced peptic ulcer disease with H. pylori co-infection. Resuscitation was initiated in the ED with 2 liters normal saline IV over 2 hours, with blood pressure improving to 128/82 mmHg and heart rate decreasing to 98 bpm by the time of transfer to the floor. Two units of packed red blood cells were transfused — transfusion was initiated given hemoglobin 7.2 g/dL with active bleeding, orthostasis, and tachycardia. Post-transfusion hemoglobin was 9.4 g/dL.

IV pantoprazole 80 mg bolus was given in the ED followed by continuous infusion at 8 mg/hour for 72 hours — high-dose PPI infusion reduces rebleeding rates in peptic ulcer hemorrhage. After 72 hours, transitioned to oral pantoprazole 40 mg twice daily.

Emergent endoscopy was performed on hospital day 1. The duodenal posterior wall ulcer with visible vessel (Forrest IIa) was treated with epinephrine injection and hemostatic clips, as described above. Second-look endoscopy on day 2 confirmed adequate hemostasis. No surgical intervention was required.

Apixaban was held throughout the admission. Cardiology was consulted regarding the safety and timing of anticoagulation restart given the history of AFib. Risk-benefit discussion was conducted with the patient and wife: the rebleed risk vs. stroke risk. Given the successful endoscopic hemostasis and high-risk AFib (CHA₂DS₂-VASc 4: age, sex, hypertension, and vascular disease from atherosclerotic risk), anticoagulation was restarted on hospital day 3 (48 hours post-hemostasis). Apixaban 5 mg twice daily was restarted. Long-term PPI was prescribed for GI protection with anticoagulation.

Ibuprofen was permanently discontinued with a clear directive — never to use NSAIDs again. Celecoxib (COX-2 selective inhibitor with lower GI risk) plus PPI was considered for future knee pain management; discussed with the patient; decision deferred to outpatient orthopedic and gastroenterology review prior to prescribing.

H. pylori eradication therapy was prescribed on discharge: clarithromycin-based triple therapy (amoxicillin 1g, clarithromycin 500 mg, pantoprazole 40 mg — each twice daily for 14 days). Test-of-cure with urea breath test or stool antigen at 4 weeks post-completion of H. pylori treatment.

DISCHARGE DIAGNOSES
1. Acute posthemorrhagic anemia — significant acute blood loss anemia; hemoglobin nadir 7.2 g/dL; 2 units pRBC transfused; source: upper GI bleed; primary admission diagnosis
2. Upper gastrointestinal hemorrhage — duodenal ulcer Forrest IIa; treated with endoscopic epinephrine and clips; successful hemostasis
3. Peptic ulcer disease — duodenal posterior wall ulcer; NSAID-induced plus H. pylori co-infection
4. NSAID-induced gastropathy — Grade C erosive gastritis; ibuprofen permanently discontinued
5. Helicobacter pylori infection — confirmed by serology and stool antigen; eradication therapy started
6. Atrial fibrillation on anticoagulation (apixaban) — held during acute bleed; restarted day 3
7. Hypertension — active comorbidity
8. Osteoarthritis — active comorbidity; right knee arthroplasty planning affected
9. Hyperlipidemia — active comorbidity

DISCHARGE CONDITION
Stable. No recurrent hematemesis or melena during admission. Hemoglobin 10.2 g/dL. Hemodynamically stable. Tolerating oral diet and medications. Apixaban restarted day 3 without recurrent bleeding.

DISCHARGE MEDICATIONS
1. Pantoprazole 40 mg orally twice daily — NEW; take 30 minutes before meals; continue long-term (on anticoagulation)
2. Amoxicillin 1g orally twice daily — H. pylori eradication (14-day course)
3. Clarithromycin 500 mg orally twice daily — H. pylori eradication (14-day course, with meals)
4. Apixaban 5 mg orally twice daily — RESUMED; do not stop without cardiology guidance; take with food
5. Metoprolol succinate 50 mg orally daily — continued
6. Lisinopril 20 mg orally daily — RESUMED; held during hypotension, now stable
7. Atorvastatin 40 mg orally nightly — continued
8. Acetaminophen 500 mg orally every 6 hours as needed (max 2g/day) — ONLY pain reliever you may use; NEVER take ibuprofen, naproxen, aspirin for pain, or any NSAID

DISCHARGE INSTRUCTIONS
You were admitted because your stomach was bleeding from a stomach ulcer caused by anti-inflammatory pain medications (ibuprofen) plus a bacterial infection (H. pylori). You must NEVER take ibuprofen, naproxen (Aleve), aspirin for pain, or any similar anti-inflammatory medication again — they cause stomach bleeding. For pain, use only Tylenol (acetaminophen). Complete the full 14-day antibiotic course for H. pylori — all three medications, twice daily with food. You will have a breath test or stool test in 4–6 weeks to confirm the infection is cured. Continue the pantoprazole twice daily long-term to protect your stomach. Watch for any recurrence of vomiting blood, coffee-ground vomit, or black tarry stools — go to the ER immediately.

FOLLOW-UP
1. Gastroenterology (Dr. Huang): 4–6 weeks — H. pylori test-of-cure; repeat endoscopy to confirm ulcer healing
2. Cardiology: 2 weeks — anticoagulation review; apixaban restart confirmation
3. Orthopedics: 4–6 weeks — reassess right knee arthroplasty candidacy; safer analgesic plan (no NSAIDs)
4. Primary Care: 1 week — hemoglobin recheck, medication reconciliation""",
    },
    {
        "title": "Acute Gout Flare — Polyarticular with Septic Joint Excluded",
        "category": "Internal Medicine / Rheumatology",
        "expected_codes": ["M109"],
        "text": """DISCHARGE SUMMARY
==================
Patient: William Huang, 57M | MRN: 5038271
Admission: 11/05/2025 | Discharge: 11/07/2025 | LOS: 2 days
Attending: Dr. C. Weber, MD | Service: Internal Medicine / Rheumatology

CHIEF COMPLAINT
Severe pain, swelling, and erythema of the right knee and left first metatarsophalangeal joint for two days; unable to bear weight.

HISTORY OF PRESENT ILLNESS
Mr. Huang is a 57-year-old man with a known history of gout with multiple prior acute flares (this is his fifth documented attack), hypertension, and chronic kidney disease Stage 2 who presents with a two-day history of severe, acutely worsening pain and swelling of the right knee and left first MTP joint (classic podagra recurrence). He rates the pain 10/10, describes it as a constant burning, throbbing, and exquisitely tender sensation — even the bedsheet touching the joints is unbearable. The right knee is markedly swollen, warm, and erythematous. The left first MTP joint is similarly affected. He is unable to bear weight on either limb. Onset was sudden — he awoke at 2 AM two nights ago with severe joint pain, a presentation classic for gout.

Precipitating factors: he underwent a CT abdomen with IV contrast for abdominal pain evaluation three days prior to this admission — contrast administration and the associated osmotic diuresis likely precipitated an acute gout attack by acutely changing serum urate concentration. He also reports a celebratory meal with shellfish (shrimp and scallops, high purine) and two glasses of beer three nights ago. He is not on urate-lowering therapy — allopurinol was prescribed after his fourth flare eight months ago but he discontinued it after two months due to rash (mild, maculopapular). He has not had any gout prophylaxis since stopping allopurinol.

He denies fever above 37.8°C. He reports two prior episodes of podagra, one prior knee flare, and one wrist flare. He has no history of joint prosthesis. He denies recent skin breakdown over the joints or penetrating injury. He has no known immunosuppression.

In the emergency department, right knee aspiration was performed — 28 mL of cloudy, yellow synovial fluid was obtained. Synovial fluid analysis showed WBC 28,000 cells/uL (predominantly PMNs), weakly negative birefringent needle-shaped crystals under polarized light — monosodium urate crystals confirming gout. Gram stain was negative. Culture was sent and resulted with no growth (negative at 48 hours). Septic arthritis was effectively excluded by negative Gram stain, negative culture, and crystal identification.

PAST MEDICAL HISTORY
1. Gout — recurrent, fifth documented attack; prior flares of bilateral feet, right knee, right wrist
2. Essential hypertension on hydrochlorothiazide and lisinopril
3. Chronic kidney disease Stage 2 (eGFR 72)
4. Hyperlipidemia on rosuvastatin
5. Obesity, BMI 33
6. Non-alcoholic fatty liver disease (NAFLD) — elevated transaminases on prior labs; liver ultrasound confirmed fatty liver
7. Former allopurinol use — discontinued due to maculopapular rash 6 months ago; febuxostat not yet started

PAST SURGICAL HISTORY
Right knee arthroscopy age 48 for meniscal tear. No prior joint replacements.

MEDICATIONS ON ADMISSION
1. Hydrochlorothiazide 25 mg orally daily — thiazide diuretic identified as gout-exacerbating; to be reviewed
2. Lisinopril 20 mg orally daily
3. Rosuvastatin 20 mg orally nightly
4. Aspirin 81 mg orally daily — low-dose aspirin can impair urate excretion; reviewed with rheumatology

ALLERGIES
Allopurinol (maculopapular rash — mild; no Stevens-Johnson syndrome; no systemic involvement). No other known drug allergies.

SOCIAL HISTORY
Restaurant owner. Married, lives with wife. Two adult children. Social smoker — two to three cigarettes per week. Moderate alcohol — two to three drinks per week (beer); instructed to stop alcohol. Diet high in purine-rich foods (seafood, red meat) related to his restaurant business. Medicare and commercial insurance (dual). Limited physical activity due to progressive joint pain with recurrent flares.

FAMILY HISTORY
Father had gout and died of coronary artery disease. Mother had hypertension and diabetes. One sibling with gout.

REVIEW OF SYSTEMS
Positive: severe joint pain (right knee and left first MTP — 10/10 intensity), warmth and erythema of affected joints, joint swelling, inability to bear weight, awakened from sleep by pain (classic gout presentation), mild low-grade fever (37.6°C at home x1 day, now resolved).
Negative: rigors, high fever (>38°C), joint drainage, skin breakdown over joints, rash, urticaria, throat tightness, diarrhea, abdominal pain beyond the prior CT evaluation.

PHYSICAL EXAMINATION ON ADMISSION
Vital Signs: Temp 37.3°C, BP 152/94 mmHg, HR 92 bpm, RR 16 breaths/min, SpO2 98% RA, Wt 97 kg
General: Obese middle-aged man in significant pain. Unable to ambulate without severe discomfort. Alert and oriented x3.
HEENT: No JVD. No lymphadenopathy. Examination of ear pinnae — small tophus identified in left helix (previously unnoticed). No corneal calcifications.
Cardiovascular: Regular rate and rhythm. No murmurs.
Pulmonary: Clear bilaterally.
Abdomen: Soft, non-tender. Mild hepatomegaly — liver edge 2 cm below right costal margin. No ascites.
Musculoskeletal: Right knee — marked swelling (moderate-to-large effusion), warmth, erythema involving the knee and extending 3 cm distal to the patella. Exquisitely tender to even light touch. ROM limited to 15–80 degrees (normal 0–135) due to pain and effusion. Left first MTP joint — swollen, erythematous, warm, severely tender, classic podagra appearance. No tophi visible at fingers, elbows, or Achilles tendons; one small tophus left auricle as noted. No skin ulceration. No draining sinus.
Neurological: Alert and oriented. No focal deficits.

LABORATORY DATA
Serum uric acid: 11.4 mg/dL (markedly elevated; normal <6.8 mg/dL in men)
Synovial fluid (right knee aspiration): WBC 28,000/uL (predominantly PMNs 84%), RBC 800/uL, Glucose 78 mg/dL (normal; in septic arthritis, glucose typically low), Protein 5.4 g/dL; Crystals: weakly negative birefringent needle-shaped crystals abundant under polarized light — monosodium urate (MSU) crystals; Gram stain: negative; Culture: no growth at 48 hours
BMP: Na 140, K 3.8, Cl 103, HCO3 24, BUN 18, Cr 1.1, Glucose 112 — normal
CBC: WBC 11.8 K/uL (leukocytosis — inflammatory; no left shift), Hgb 14.2, Hct 42.6%, Plt 248
CRP: 94 mg/L (markedly elevated — acute phase response from gout)
ESR: 88 mm/hour — elevated
LFTs: AST 48, ALT 62, Alk Phos 98, Total bili 0.9 — mildly elevated transaminases (known NAFLD; colchicine-safe at these levels)
Creatinine clearance (Cockcroft-Gault): 82 mL/min — adequate for colchicine dosing; note CKD Stage 2
24-hour urine uric acid (collected outpatient after discharge — arranged): To determine uric acid overproducer vs. underexcretor status for future ULT selection

IMAGING AND DIAGNOSTICS
Right Knee X-Ray: Joint space preserved. No chondrocalcinosis. Moderate effusion. No erosive changes. No fracture. No loose bodies.
Left Foot X-Ray: Periarticular soft tissue swelling at first MTP joint. No erosion. No joint space narrowing. No tophi calcification on plain film.
Musculoskeletal Ultrasound (right knee, hospital day 1): Double contour sign at the femoral condyle articular cartilage — highly specific for urate crystal deposition (sensitivity 44%, specificity 98%). Large joint effusion with echogenic material (urate deposits). No evidence of tophus within the joint. Findings confirmatory of gout.

HOSPITAL COURSE
Mr. Huang was admitted for management of acute polyarticular gout flare involving the right knee and left first MTP joint, with septic arthritis excluded by synovial fluid analysis (negative cultures, crystal identification). He received IV ketorolac 30 mg every 6 hours for the first 24 hours given severe pain — NSAIDs are first-line for acute gout when renal function and GI safety permit (eGFR adequate; no prior GI bleed; PPI prescribed with NSAID use). He was transitioned to oral indomethacin 50 mg three times daily on day 2.

IV methylprednisolone 80 mg was given once on hospital day 1 given the polyarticular involvement and severity of pain — systemic corticosteroids are an effective alternative when NSAIDs alone are insufficient. Oral prednisone 40 mg daily was prescribed for a 5-day outpatient taper.

Colchicine 1.2 mg orally followed by 0.6 mg one hour later (acute gout dosing protocol) was given on hospital day 1. Low-dose colchicine 0.6 mg twice daily was continued for prophylaxis and as adjunct to anti-inflammatory therapy.

The right knee was aspirated — the joint aspiration itself provided significant pain relief by decompressing the effusion. After aspiration, 40 mg triamcinolone acetonide was injected intra-articularly into the right knee, providing rapid local anti-inflammatory effect.

Pain improved substantially by day 2 — he rated pain 4/10 at rest and 6/10 with movement. He was ambulating with a cane by discharge with significant improvement in range of motion (now 20–100 degrees).

Urate-lowering therapy (ULT) planning was a critical part of the discharge plan. Given his allopurinol allergy (mild rash), febuxostat 40 mg daily was selected as the xanthine oxidase inhibitor for ongoing therapy — febuxostat does not cross-react with allopurinol. Hydrochlorothiazide (uricosuric inhibitor — thiazides block renal urate excretion, worsening hyperuricemia) was discontinued and replaced with amlodipine 5 mg for blood pressure management (amlodipine has a neutral effect on uric acid). Losartan was considered as an add-on given its mild uricosuric effect. Dietary counseling was provided: eliminate organ meats, limit red meat, avoid beer and liquor (wine in moderation may be acceptable), eliminate high-fructose corn syrup, limit shellfish and oily fish, increase low-fat dairy and cherries (reduce uric acid).

Rheumatology outpatient follow-up was arranged in 6 weeks to ensure ULT target achieved (serum uric acid <6 mg/dL; <5 mg/dL for patients with tophi — tophus noted in left auricle).

DISCHARGE DIAGNOSES
1. Gout, unspecified — acute polyarticular flare; right knee and left first MTP joint; MSU crystals confirmed; primary admission diagnosis
2. Septic arthritis excluded — synovial WBC 28,000 but crystal-confirmed; negative Gram stain and culture
3. Hyperuricemia — serum uric acid 11.4 mg/dL; urate-lowering therapy initiated
4. Essential hypertension — hydrochlorothiazide discontinued (contributed to hyperuricemia); amlodipine added
5. Chronic kidney disease Stage 2 — active comorbidity; febuxostat preferred over allopurinol given allergy
6. NAFLD — active comorbidity
7. Hyperlipidemia — active comorbidity

DISCHARGE CONDITION
Improved. Pain 4/10 at rest. Ambulating with cane. Right knee effusion reduced. First MTP swelling reduced. Tolerating oral anti-inflammatory medications. Afebrile.

DISCHARGE MEDICATIONS
1. Indomethacin 50 mg orally three times daily with food — complete 7-day anti-inflammatory course (5 days remaining at discharge); take with food; do not take without food
2. Pantoprazole 40 mg orally daily — NEW; GI protection while on indomethacin
3. Prednisone 40 mg orally daily x3 days, then 20 mg x3 days, then stop — tapering steroid course
4. Colchicine 0.6 mg orally twice daily — prophylactic; continue for minimum 6 months while starting urate-lowering therapy; reduces flare risk
5. Febuxostat 40 mg orally daily — NEW urate-lowering therapy; start today; continue indefinitely; do not start during an acute flare — already 48h into flare, now appropriate
6. Amlodipine 5 mg orally daily — NEW; replaces hydrochlorothiazide for blood pressure
7. Lisinopril 20 mg orally daily — continued
8. Rosuvastatin 20 mg orally nightly — continued
9. Aspirin 81 mg orally daily — continued (cardiovascular benefit; very low dose has minimal uricosuric impact; continue per cardiology risk assessment)

DISCHARGE INSTRUCTIONS
You had a severe gout attack in your right knee and left big toe joint. The attack is caused by uric acid crystals that deposit in your joints when uric acid in your blood is too high (yours is 11.4 — the goal is below 6.0). We have started a new medication (febuxostat) to lower your uric acid long-term. Take it every day even when you feel well — stopping and starting it can trigger more attacks. Take colchicine twice daily for the next 6 months to prevent attacks while your uric acid comes down. Dietary changes are critical: eliminate organ meats, beer, and hard liquor; limit red meat and shellfish; drink plenty of water. You will have a blood test to check your uric acid level in 6 weeks at rheumatology.

FOLLOW-UP
1. Rheumatology (Outpatient): 6 weeks — serum uric acid recheck; febuxostat dose adjustment (may need 80 mg); tophus assessment; ULT target <5 mg/dL given tophi
2. Internal Medicine (Dr. Weber): 2 weeks — blood pressure on new amlodipine; renal function
3. Gastroenterology: 6 weeks — NAFLD assessment; liver enzymes on febuxostat
4. Dietary counseling: Arranged within 2 weeks — low-purine diet education""",
    },
    {
        "title": "Major Depressive Disorder — Severe Episode with Suicidal Ideation",
        "category": "Psychiatry / Internal Medicine",
        "expected_codes": ["F329"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Miriam Cohen, 48F | MRN: 6094821
Admission: 10/25/2025 | Discharge: 10/31/2025 | LOS: 6 days
Attending: Dr. A. Mehta, MD | Service: Inpatient Psychiatry

CHIEF COMPLAINT
Worsening depression, passive suicidal ideation with a plan, and inability to care for self brought in by husband after she disclosed she had been researching methods.

HISTORY OF PRESENT ILLNESS
Ms. Cohen is a 48-year-old woman with a history of recurrent major depressive disorder (prior episodes at ages 28 and 36, both requiring medication adjustment; no prior inpatient psychiatric admissions), type 2 diabetes mellitus, hypertension, and hypothyroidism who was brought to the emergency department by her husband after he discovered she had been researching medication overdose methods online and she disclosed having a plan to take her entire medication supply. She reports a 12-week history of progressive and severe depressive symptoms including persistent depressed mood throughout most of every day, complete anhedonia (unable to derive pleasure from anything including activities she previously loved such as painting and cooking), hypersomnia (sleeping 14–16 hours daily with difficulty getting out of bed), psychomotor retardation visible to family members, significant appetite decrease with 14-pound weight loss over 12 weeks, severe fatigue, feelings of worthlessness and excessive guilt (she repeatedly states she is a burden to her family), poor concentration (unable to read or follow conversations), and passive suicidal ideation that escalated in the past 72 hours to active ideation with a plan.

She identifies several precipitants: she was laid off from her position as a financial analyst 14 weeks ago after 12 years of employment (company downsizing), which she describes as devastating to her identity and sense of purpose. Concurrently, her mother was diagnosed with Alzheimer's disease and she has been serving as the primary caregiver. Her husband reports she has been increasingly withdrawn, not answering phone calls, and not leaving the house for three weeks. She denies alcohol or substance use.

She was last seen by her outpatient psychiatrist four months ago — her usual appointment frequency had been once every three months. She has been on sertraline 100 mg daily for maintenance but discloses she ran out of the medication four weeks ago and did not refill it because she felt "too paralyzed to call the pharmacy." The abrupt SSRI discontinuation may have contributed to the rapid worsening of her depressive episode.

She has no prior history of mania, hypomania, psychotic features, or self-harm beyond suicidal ideation. She denies auditory or visual hallucinations. She denies homicidal ideation. She has no history of suicide attempts.

Collateral from husband: she has not eaten a full meal in two weeks, has been sleeping in a dark room for three weeks, and had not showered in six days prior to this presentation. He is extremely concerned.

PAST MEDICAL HISTORY
1. Major depressive disorder, recurrent — prior episodes age 28 (responded to sertraline 50 mg) and age 36 (responded to sertraline 100 mg); both achieved full remission; no prior hospitalizations; no history of psychosis
2. Type 2 diabetes mellitus on metformin
3. Essential hypertension on amlodipine
4. Hypothyroidism on levothyroxine — TSH stable at 1.8 mIU/L 6 months prior
5. Obesity, BMI 31
6. Fibromyalgia — managed with duloxetine (now discontinued; was replaced by sertraline 3 years ago at patient request)

PAST SURGICAL HISTORY
Appendectomy age 19. Cesarean section age 26.

MEDICATIONS ON ADMISSION
1. Sertraline 100 mg orally daily — NOT TAKING FOR 4 WEEKS (ran out; did not refill)
2. Metformin 1000 mg orally twice daily
3. Amlodipine 5 mg orally daily
4. Levothyroxine 88 mcg orally daily on empty stomach
5. Acetaminophen 500 mg orally as needed
6. Vitamin D 2000 IU orally daily

ALLERGIES
Fluoxetine (akathisia — discontinued at age 28 after severe restlessness; no other SSRI cross-intolerance confirmed). Codeine (nausea).

PSYCHIATRIC MEDICATIONS: All medications at home were collected by her husband and secured prior to discharge planning to reduce access to means for suicidality.

SOCIAL HISTORY
Former financial analyst, laid off 14 weeks ago. Married for 22 years; described as a supportive and involved husband who is distressed. Two adolescent children (ages 16 and 14) at home. Lives in a single-family home. No alcohol. No illicit drug use. No prior arrests or legal issues. Practicing Jewish faith — identifies religion as an important value but states she feels spiritually disconnected currently. Excellent insurance (commercial PPO). Had strong social network but has been socially isolating for 3 months.

FAMILY HISTORY
Mother — Alzheimer's disease (newly diagnosed). Father — major depressive disorder treated with ECT in the 1980s. Maternal aunt — completed suicide (age 55, medication overdose). Family history significantly positive for both depression and suicide — important risk factor.

REVIEW OF SYSTEMS (Psychiatric)
Positive: depressed mood (persistent, most of the day, every day for 12 weeks), anhedonia (complete), hypersomnia (14–16 hours/day), psychomotor retardation, 14-lb weight loss, decreased appetite, fatigue, worthlessness, excessive guilt, poor concentration, suicidal ideation with plan (researched medication overdose methods; access to medications at home).
Negative: auditory hallucinations, visual hallucinations, grandiosity, elevated mood, decreased need for sleep with high energy (no mania/hypomania), flight of ideas, homicidal ideation, current substance intoxication or withdrawal, disorientation.

PHYSICAL EXAMINATION ON ADMISSION (MEDICAL CLEARANCE)
Vital Signs: Temp 36.8°C, BP 138/88 mmHg, HR 82 bpm, RR 16 breaths/min, SpO2 98% RA, Wt 91 kg
General: Obese middle-aged woman, disheveled appearance (unwashed hair, no makeup, wrinkled clothing). Tearful throughout examination. Psychomotor retardation visible — slow movements and slow speech. Alert and oriented x3.
HEENT: Periorbital puffiness from crying. Mucous membranes moist. No lymphadenopathy.
Cardiovascular: Regular rate and rhythm. No murmurs.
Pulmonary: Clear bilaterally.
Abdomen: Soft, non-tender.
Extremities: No edema. No injection sites. No fresh self-harm lesions.
Neurological: Alert, oriented x3. Speech slow, monotone, low volume. Cranial nerves intact. Motor 5/5. No focal deficits.

Mental Status Examination
Appearance: Disheveled, older-appearing for stated age, tearful
Behavior: Cooperative but psychomotorically retarded; slowed movements; limited eye contact
Speech: Slow, low volume, monotone, reduced prosody
Mood: "Hopeless" — patient's own words; "I don't see any way out of this"
Affect: Dysphoric, constricted, tearful
Thought process: Linear, coherent, goal-directed
Thought content: Passive suicidal ideation escalated to active with plan (medication overdose); denies homicidal ideation; no thought insertion or broadcasting; no delusions
Perceptions: No auditory or visual hallucinations
Cognition: Oriented x3; concentration impaired; serial 7s — 3 of 5 correct
Insight: Limited — minimizes severity ("I'm just sad")
Judgment: Impaired — had concealed suicidal ideation from husband for three weeks

LABORATORY DATA (MEDICAL CLEARANCE)
BMP: Na 140, K 4.0, Cl 103, HCO3 25, BUN 12, Cr 0.8, Glucose 148 — normal
CBC: WBC 7.2, Hgb 13.4, Hct 40.2%, Plt 264 — normal
TSH: 1.4 mIU/L — normal; hypothyroidism as contributing factor to depression excluded
Free T4: 1.2 ng/dL — normal
Urine toxicology: Negative for all substances including opioids, benzodiazepines, cocaine, amphetamines, cannabis, PCP, barbiturates
Blood alcohol: 0.0 mg/dL — no alcohol ingestion
Serum acetaminophen: Negative — no overdose had occurred
Serum salicylates: Negative
Vitamin B12: 440 pg/mL — normal
Folate: 14 ng/mL — normal
HbA1c: 7.4% — reasonably controlled diabetes
Lipid panel: LDL 108, HDL 52, Total 182, TG 112 — acceptable

HOSPITAL COURSE
Ms. Cohen was admitted voluntarily to the inpatient psychiatric unit for management of severe major depressive disorder, single episode, with active suicidal ideation and plan. She was admitted to a locked psychiatric ward with constant line-of-sight observation for the first 24 hours, transitioning to every 15-minute safety checks after clinical improvement.

Means restriction was implemented immediately: her husband was instructed to secure all medications at home (which he had done prior to arrival), remove firearms if present (family confirmed no firearms in home), and lock up sharp objects. He was counseled on lethal means reduction as part of the safety planning process.

Sertraline was restarted at 100 mg daily — restarting the same previously effective SSRI at the same dose was appropriate given prior confirmed response. Given the severity of this episode and the abrupt discontinuation that may have contributed, adjunctive treatment was discussed. Mirtazapine 15 mg at bedtime was added on hospital day 2 for augmentation (targets insomnia, appetite, and depression through a different mechanism; appropriate for her hypersomnia and weight loss/appetite concerns). The mirtazapine was explained to her and she consented to the addition.

Daily individual therapy was conducted by the inpatient psychiatric team psychologist. Behavioral activation and safety planning were the primary foci of early treatment. Group therapy sessions were attended beginning day 2 — she participated minimally initially but showed increasing engagement by day 4.

Suicidal ideation diminished progressively: on day 1 she continued to endorse passive ideation without a current plan (plan had been "interrupted" by hospitalization); by day 3 she denied active suicidal ideation and plan; by day 5 she endorsed a future orientation and was making plans to contact a therapist she had previously seen. PHQ-9 score improved from 27 (severe) on admission to 16 (moderate) on day 5.

Medical comorbidities were co-managed throughout. Metformin, amlodipine, and levothyroxine were continued without interruption. Blood glucose was monitored daily given mirtazapine's potential metabolic effects; glucose remained in the 130–160 range. Blood pressure was well-controlled on amlodipine.

Discharge safety planning was conducted with the patient and her husband together on day 5 and reviewed again on day 6. The safety plan included: warning signs of worsening (isolation, stopping medications), coping strategies (calling her sister, painting), reasons for living (her children, her relationship with her husband), people she can contact (husband, sister, outpatient psychiatrist — after-hours line), crisis resources (988 Suicide and Crisis Lifeline), and emergency plan (call 911 or go to ER). Husband agreed to continue medication monitoring. A 7-day supply of sertraline and mirtazapine was provided at discharge (dispense-limited to reduce means access); psychiatry will provide 30-day supply at first outpatient visit.

She was discharged with a committed safety plan, an outpatient psychiatry appointment the following week, and clear instructions for her husband to call 911 if she expresses suicidal intent.

DISCHARGE DIAGNOSES
1. Major depressive disorder, single episode, unspecified — severe, with active suicidal ideation and plan; SSRI discontinuation as precipitant; primary admission diagnosis
2. Active suicidal ideation with plan (researched method) — resolved; safety plan in place
3. SSRI discontinuation syndrome — sertraline discontinued x4 weeks; contributing to episode severity
4. Type 2 diabetes mellitus — active comorbidity
5. Essential hypertension — active comorbidity
6. Hypothyroidism — active comorbidity; TSH normal; not contributing to depression
7. Obesity — active comorbidity

DISCHARGE CONDITION
Improved but not in remission. PHQ-9 score 16 (moderate) — improved from 27 (severe) on admission. No active suicidal ideation on day of discharge. Future-oriented statements. Safety plan in place. Husband engaged and supportive. Medications restarted. Ready for step-down to intensive outpatient program.

DISCHARGE MEDICATIONS
1. Sertraline 100 mg orally daily — RESUMED; take every morning; DO NOT stop without psychiatrist guidance; take even if you feel well
2. Mirtazapine 15 mg orally at bedtime — NEW; helps with sleep and appetite; may increase appetite and cause morning sedation (take at bedtime)
3. Metformin 1000 mg orally twice daily — continued
4. Amlodipine 5 mg orally daily — continued
5. Levothyroxine 88 mcg orally daily on empty stomach (before sertraline — separated by 30 min) — continued
6. Vitamin D 2000 IU orally daily — continued
NOTE: 7-day medication supply dispensed only; husband is administering and monitoring medications. Controlled dispensing until outpatient psychiatry follow-up.

DISCHARGE INSTRUCTIONS
You were admitted because you were having thoughts of ending your life. You are leaving in a better place than you arrived, but recovery from depression takes time. Take your medications every single day — the biggest risk factor for another crisis is stopping your antidepressants. Review your safety plan with your husband every day this week. If you have thoughts of hurting yourself, call your husband immediately, call the 988 Suicide and Crisis Lifeline, or go to the nearest emergency room. Your first therapy appointment is in 3 days. Attend it. Do not isolate — even small steps like sitting in the living room or texting your sister are important.

FOLLOW-UP
1. Outpatient Psychiatry (Dr. Mehta's group): 7 days — medication review, ongoing therapy plan, 30-day prescription provided at that visit
2. Intensive Outpatient Program (IOP): Referral placed; begins within 3–5 days of discharge (Monday following discharge)
3. Individual Therapy (weekly): Arranged with prior therapist starting next week
4. Primary Care: 2 weeks — diabetes, blood pressure, weight monitoring with mirtazapine
5. 988 Lifeline and Crisis Text Line: Printed on discharge paperwork; number saved in patient's phone""",
    },
    # NOTES_PLACEHOLDER
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

    # ── Wipe existing notes ───────────────────────────────────────────────────
    print("Wiping existing sample_notes...", end=" ", flush=True)
    with httpx.Client(timeout=60.0) as client:
        r = client.delete(
            f"{base}/rest/v1/sample_notes",
            params={"id": "not.is.null"},
            headers={**headers, "Prefer": "return=minimal"},
        )
    if r.status_code in (200, 204):
        print("OK")
    else:
        print(f"WARNING — wipe returned {r.status_code}: {r.text[:200]}")

    # ── Insert new notes ──────────────────────────────────────────────────────
    created, failed = 0, 0
    with httpx.Client(timeout=60.0) as client:
        for note in SAMPLE_NOTES:
            print(f"  Inserting: {note['title'][:60]}...", end=" ", flush=True)
            try:
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
                    print(f"FAILED — {r.status_code}: {r.text[:300]}")
                    failed += 1
                    continue
                print("OK")
                created += 1
            except Exception as e:
                print(f"FAILED — {e}")
                failed += 1

    print(f"\nDone: {created} inserted, {failed} failed")


if __name__ == "__main__":
    main()
