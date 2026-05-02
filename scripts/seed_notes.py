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
