"""Additional synthetic discharge summaries for the full-code model.

The original 21 templates in `seed_notes.py` were written for the top-50
DIAGNOSIS space, so they are almost entirely cardiology, pulmonary, endocrine
and renal medicine. The full-code model also predicts 2,138 ICD-10-PCS
procedure codes, 27% of its label space, and nothing in that original set is a
surgical, oncologic, obstetric, trauma or neuro-interventional admission.

These six fill that gap. Each is built around an operation so the procedure
pathway is exercised, and each carries the comorbidity load a real discharge
summary carries, so the note produces a realistic 10 to 20 codes rather than one.

ENTIRELY SYNTHETIC. No real patient data, no MIMIC text. Names, dates, medical
record numbers and every clinical detail are invented. This matters: the real
MIMIC notes in `sample_notes_seed.json` are credentialed-access under a data
use agreement and must never be loaded into a platform other people can log
into. They stay local, used only by the parity and smoke scripts.
"""

EXTRA_NOTES = [
    {
        "title": "Perforated Diverticulitis — Laparoscopic Sigmoid Colectomy",
        "category": "Colorectal Surgery",
        "expected_codes": ["K57.20", "0DTN4ZZ", "K65.1", "I10.", "E78.5", "Z79.899"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Raymond Alcott, 61M | MRN: 7719340
Admission: 03/04/2026 | Discharge: 03/11/2026 | LOS: 7 days
Attending: Dr. P. Ndiaye, MD | Service: Colorectal Surgery

CHIEF COMPLAINT
Severe left lower quadrant abdominal pain with fever for two days.

HISTORY OF PRESENT ILLNESS
Mr. Alcott is a 61-year-old man with a history of recurrent diverticulitis, essential hypertension, and hyperlipidemia who presented to the emergency department with two days of progressively severe left lower quadrant abdominal pain. The pain began as a dull ache and became sharp and constant, worsened by movement and coughing. He reported subjective fevers, chills, anorexia, and obstipation with no flatus for approximately eighteen hours. He denied hematochezia, melena, vomiting, dysuria, or hematuria.

He has had three prior episodes of uncomplicated diverticulitis over the preceding four years, each managed as an outpatient with oral ciprofloxacin and metronidazole. A colonoscopy eleven months ago demonstrated extensive sigmoid diverticulosis without malignancy or dysplasia. He had been counselled about elective resection but deferred.

In the emergency department he was febrile to 38.7 degrees Celsius, tachycardic at 112 beats per minute, with blood pressure 138/84 mmHg and oxygen saturation 97% on room air. Abdominal examination revealed focal peritonitis with guarding and rebound tenderness localized to the left lower quadrant. White blood cell count was 18.4 thousand per microliter with 88% neutrophils and a left shift. Lactate was 2.4 mmol per liter. CT of the abdomen and pelvis with intravenous contrast demonstrated sigmoid diverticulitis with wall thickening, pericolonic fat stranding, a contained 3.2 centimeter pericolic abscess, and extraluminal locules of free air consistent with contained perforation, Hinchey classification Ib.

PAST MEDICAL HISTORY
1. Recurrent acute diverticulitis, three prior episodes
2. Essential hypertension, eight years
3. Hyperlipidemia on statin therapy
4. Gastroesophageal reflux disease
5. Obesity, body mass index 31

PAST SURGICAL HISTORY
1. Laparoscopic cholecystectomy, 2014
2. Right inguinal hernia repair with mesh, 2009

MEDICATIONS ON ADMISSION
Lisinopril 20 mg daily, atorvastatin 40 mg nightly, omeprazole 20 mg daily, aspirin 81 mg daily.

ALLERGIES
Sulfa drugs, causing rash.

SOCIAL HISTORY
Former smoker, twenty pack-years, quit fourteen years ago. Social alcohol use, approximately four drinks weekly. Works as a logistics manager. Lives with his spouse.

HOSPITAL COURSE
Mr. Alcott was admitted to the colorectal surgical service and made nil per os. He was resuscitated with intravenous crystalloid and started on piperacillin-tazobactam. Interventional radiology performed CT-guided percutaneous drainage of the pericolic abscess on hospital day one, yielding 35 milliliters of purulent fluid. Culture subsequently grew Escherichia coli and Bacteroides fragilis, both sensitive to the empiric regimen.

He defervesced by hospital day two and his leukocytosis improved from 18.4 to 11.2 thousand per microliter. However, on hospital day three he developed recurrent left lower quadrant pain with worsening peritoneal signs, and repeat imaging showed persistent phlegmon with a new small locule of free air. After discussion with the patient and his spouse regarding the risks and benefits, including the possibility of an ostomy, he was taken to the operating room on hospital day three.

PROCEDURE
Laparoscopic sigmoid colectomy with primary colorectal anastomosis, performed 03/07/2026 by Dr. P. Ndiaye. Findings included an inflammatory phlegmon involving the sigmoid colon with dense adhesions to the pelvic sidewall, contained perforation, and purulent peritoneal contamination confined to the pelvis. The sigmoid colon was mobilized, the inferior mesenteric artery was divided, and the specimen was resected. A stapled end-to-end colorectal anastomosis was created and tested with a negative air leak test. A pelvic drain was placed. Estimated blood loss was 150 milliliters. A diverting ostomy was not required. The patient tolerated the procedure well.

Pathology demonstrated acute and chronic diverticulitis with perforation, abscess formation, and serosal fibrinopurulent exudate. No malignancy was identified. Twelve lymph nodes were examined, all reactive.

Postoperatively he was managed on an enhanced recovery pathway. He was extubated in the operating room and transferred to the surgical floor. Pain was controlled with scheduled acetaminophen, ketorolac for the first forty-eight hours, and oral oxycodone as needed. He ambulated on postoperative day zero. Diet was advanced from clear liquids on postoperative day one to a low-residue diet on postoperative day three after return of bowel function with passage of flatus and a bowel movement.

The pelvic drain output declined from 80 to 15 milliliters daily and was removed on postoperative day three. Antibiotics were narrowed to oral amoxicillin-clavulanate on postoperative day two and completed a total ten-day course. His postoperative hemoglobin drifted from 13.8 to 10.9 grams per deciliter, consistent with operative blood loss and hemodilution, and was stable on repeat testing without transfusion.

He had transient postoperative ileus on postoperative day two with abdominal distention and nausea, managed conservatively with nasogastric decompression for eighteen hours, which resolved. He was ambulating independently, tolerating a regular diet, and had adequate pain control on oral medication by postoperative day four.

DISCHARGE DIAGNOSES
1. Perforated sigmoid diverticulitis with pericolic abscess, Hinchey Ib
2. Localized peritonitis
3. Postoperative ileus, resolved
4. Essential hypertension
5. Hyperlipidemia
6. Acute blood loss anemia, not requiring transfusion

DISCHARGE MEDICATIONS
Amoxicillin-clavulanate 875-125 mg twice daily for four more days, acetaminophen 1000 mg every eight hours, oxycodone 5 mg every six hours as needed for breakthrough pain, docusate 100 mg twice daily, lisinopril 20 mg daily, atorvastatin 40 mg nightly, omeprazole 20 mg daily. Aspirin held for seven days postoperatively then resumed.

FOLLOW-UP
Colorectal surgery clinic in two weeks for wound check and pathology discussion. Primary care in four weeks. No heavy lifting over ten pounds for six weeks. Return precautions given for fever above 38.3 degrees Celsius, worsening abdominal pain, inability to tolerate oral intake, or wound drainage.
""",
    },
    {
        "title": "Invasive Ductal Carcinoma — Mastectomy with Sentinel Node Biopsy",
        "category": "Surgical Oncology",
        "expected_codes": ["C50.412", "0HTU0ZZ", "07B60ZX", "Z17.0", "D62.", "E03.9"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Denise Karolyi, 54F | MRN: 3308821
Admission: 01/21/2026 | Discharge: 01/23/2026 | LOS: 2 days
Attending: Dr. L. Okonkwo, MD | Service: Surgical Oncology

CHIEF COMPLAINT
Admission for planned left mastectomy for biopsy-proven breast carcinoma.

HISTORY OF PRESENT ILLNESS
Ms. Karolyi is a 54-year-old postmenopausal woman who presented for definitive surgical management of a left breast invasive ductal carcinoma. The lesion was detected on screening mammography four months prior as a 2.4 centimeter spiculated mass in the upper outer quadrant of the left breast with associated pleomorphic microcalcifications. Diagnostic ultrasound confirmed a hypoechoic irregular mass measuring 2.6 by 1.9 centimeters with posterior acoustic shadowing.

Ultrasound-guided core needle biopsy demonstrated invasive ductal carcinoma, grade 2, estrogen receptor positive at 95%, progesterone receptor positive at 80%, HER2 negative by immunohistochemistry with a score of 1 plus. Ki-67 proliferation index was 18%. Axillary ultrasound showed no morphologically abnormal nodes. Staging workup including CT of the chest, abdomen and pelvis and a bone scan showed no evidence of distant metastatic disease.

She was evaluated in the multidisciplinary breast conference. Given the tumor size relative to a modest breast volume, multifocality on breast MRI with a second 0.9 centimeter satellite lesion in the same quadrant, and the patient's stated preference to avoid adjuvant radiotherapy, the recommendation was total mastectomy with sentinel lymph node biopsy rather than breast-conserving surgery. She elected to defer immediate reconstruction and will consider delayed reconstruction after completing adjuvant therapy.

PAST MEDICAL HISTORY
1. Hypothyroidism, stable on levothyroxine for eleven years
2. Migraine without aura, infrequent
3. Vitamin D deficiency
4. Anxiety disorder, managed without medication

PAST SURGICAL HISTORY
1. Cesarean delivery, 2001
2. Diagnostic laparoscopy for endometriosis, 1998

FAMILY HISTORY
Mother diagnosed with breast cancer at age 68. Maternal aunt with ovarian cancer. Genetic testing performed and negative for BRCA1, BRCA2, PALB2, CHEK2 and ATM pathogenic variants.

MEDICATIONS ON ADMISSION
Levothyroxine 88 micrograms daily, cholecalciferol 2000 units daily, sumatriptan 50 mg as needed.

ALLERGIES
No known drug allergies.

SOCIAL HISTORY
Never smoker. Rare alcohol use. Works as a secondary school teacher. Married, two adult children. Independent in all activities of daily living.

HOSPITAL COURSE
Ms. Karolyi was admitted on the morning of surgery. Preoperatively she underwent lymphoscintigraphy with technetium-99m sulfur colloid injected in the periareolar region, which demonstrated drainage to two left axillary sentinel nodes.

PROCEDURE
Left total simple mastectomy with sentinel lymph node biopsy, performed 01/21/2026 by Dr. L. Okonkwo. Blue dye and radiotracer were used for sentinel node localization. Three sentinel nodes were identified as both blue and hot and were excised. Intraoperative frozen section of the sentinel nodes was negative for metastatic carcinoma. The mastectomy was completed with preservation of the pectoralis major fascia. Two closed suction drains were placed in the mastectomy bed and axilla. Estimated blood loss was 90 milliliters.

Final pathology confirmed invasive ductal carcinoma, grade 2, measuring 2.7 centimeters in greatest dimension, with an adjacent 1.0 centimeter satellite focus. An extensive intraductal component with intermediate-grade ductal carcinoma in situ was present. All margins were negative, with the closest deep margin at 4 millimeters. Lymphovascular invasion was not identified. Three sentinel lymph nodes were negative for metastatic carcinoma on permanent sections with immunohistochemistry, staged as pathologic N0. Final pathologic stage was pT2 pN0 cM0, stage IIA. Receptor status was confirmed on the resection specimen as estrogen and progesterone receptor positive and HER2 negative.

Postoperatively she was observed overnight for pain control and drain management. Pain was well controlled with scheduled acetaminophen and celecoxib supplemented by a single dose of oral oxycodone on the evening of surgery. She was seen by physical therapy for shoulder range-of-motion instruction and by the breast care nurse for drain care education and mastectomy camisole fitting.

Her hemoglobin declined from a preoperative 12.9 to 11.1 grams per deciliter, consistent with operative blood loss and dilution, with no transfusion required. Drain outputs were 70 and 45 milliliters on the first postoperative day. The mastectomy flaps were viable with no evidence of hematoma, seroma or ischemia. She tolerated a regular diet and ambulated independently.

She was seen by the medical oncology service prior to discharge. Given a node-negative, hormone receptor positive, HER2 negative tumor, a 21-gene recurrence score assay has been sent on the resection specimen to guide the decision regarding adjuvant chemotherapy. Adjuvant endocrine therapy with an aromatase inhibitor is planned regardless of the assay result. Post-mastectomy radiotherapy is not indicated for this stage with negative nodes and clear margins.

DISCHARGE DIAGNOSES
1. Invasive ductal carcinoma of the upper outer quadrant of the left breast, pT2 pN0 cM0, stage IIA, estrogen and progesterone receptor positive, HER2 negative
2. Ductal carcinoma in situ, intermediate grade, associated
3. Status post left total mastectomy with sentinel lymph node biopsy
4. Acute blood loss anemia, not requiring transfusion
5. Hypothyroidism
6. Family history of malignant neoplasm of the breast

DISCHARGE MEDICATIONS
Acetaminophen 1000 mg every eight hours scheduled for five days, celecoxib 200 mg twice daily for five days, oxycodone 5 mg every six hours as needed for severe pain with a quantity of twelve tablets, docusate 100 mg twice daily while taking opioids, levothyroxine 88 micrograms daily, cholecalciferol 2000 units daily.

FOLLOW-UP
Surgical oncology in seven days for drain assessment and likely removal. Medical oncology in three weeks to review the recurrence score assay and initiate endocrine therapy. Plastic surgery consultation for delayed reconstruction at her discretion. Lymphedema precautions reviewed, including avoidance of blood pressure measurement and venipuncture in the left arm. Return precautions given for fever, expanding flap erythema, sudden increase in drain output, or drain output that becomes bloody.
""",
    },
    {
        "title": "Displaced Femoral Neck Fracture — Total Hip Arthroplasty",
        "category": "Orthopedic Surgery",
        "expected_codes": ["S72.001A", "0SR904A", "W19.XXXA", "D62.", "N17.9", "E11.9", "I10."],
        "text": """DISCHARGE SUMMARY
==================
Patient: Harold Vintner, 78M | MRN: 5540127
Admission: 11/02/2025 | Discharge: 11/07/2025 | LOS: 5 days
Attending: Dr. S. Bergstrom, MD | Service: Orthopedic Surgery

CHIEF COMPLAINT
Right hip pain and inability to bear weight after a fall at home.

HISTORY OF PRESENT ILLNESS
Mr. Vintner is a 78-year-old man with type 2 diabetes mellitus, hypertension, and chronic kidney disease stage 3a who presented by ambulance after a mechanical fall in his kitchen. He reported tripping on a rug, falling directly onto his right side, and being unable to stand afterward. He denied preceding chest pain, palpitations, lightheadedness, or loss of consciousness, and the history is not suggestive of a syncopal event. He was on the floor for approximately forty minutes before his daughter found him.

He described severe right hip and groin pain, rated nine out of ten, worse with any attempted movement. He denied head strike, neck pain, or other injuries. He ambulates independently at baseline with occasional use of a cane outdoors and lives alone in a single-story home.

In the emergency department, vital signs were blood pressure 158/86 mmHg, heart rate 92 beats per minute, respiratory rate 18, temperature 36.6 degrees Celsius, and oxygen saturation 96% on room air. The right lower extremity was shortened and externally rotated with severe pain on any range of motion. Distal pulses were intact and there was no neurologic deficit. Skin was intact with no open wound.

Radiographs of the right hip and pelvis demonstrated a displaced subcapital femoral neck fracture, Garden classification III. Chest radiograph was clear. Electrocardiogram showed normal sinus rhythm without acute ischemic changes. Initial laboratory studies showed hemoglobin 12.4 grams per deciliter, creatinine 1.6 milligrams per deciliter above a baseline of 1.3, estimated glomerular filtration rate 44 milliliters per minute, glucose 214 milligrams per deciliter, and hemoglobin A1c of 7.8%.

PAST MEDICAL HISTORY
1. Type 2 diabetes mellitus, twelve years, on metformin and sitagliptin
2. Essential hypertension
3. Chronic kidney disease stage 3a
4. Benign prostatic hyperplasia
5. Osteoarthritis of both knees
6. Osteopenia, never treated with bisphosphonates

PAST SURGICAL HISTORY
1. Transurethral resection of the prostate, 2016
2. Cataract extraction, bilateral, 2019 and 2020

MEDICATIONS ON ADMISSION
Metformin 1000 mg twice daily, sitagliptin 50 mg daily, amlodipine 10 mg daily, tamsulosin 0.4 mg nightly, acetaminophen as needed.

ALLERGIES
Codeine, causing nausea.

SOCIAL HISTORY
Lives alone. Widowed. Daughter lives fifteen minutes away and is closely involved. Never smoker. No alcohol use. Retired postal worker.

HOSPITAL COURSE
Mr. Vintner was admitted to the orthopedic service with medicine co-management under a geriatric hip fracture pathway. Metformin was held on admission given the acute kidney injury and planned anesthesia. Intravenous fluids were administered judiciously with attention to his cardiac and renal status, and his creatinine improved from 1.6 to 1.3 milligrams per deciliter by the morning of surgery, consistent with prerenal acute kidney injury from dehydration and time on the floor.

Preoperative risk stratification found him at acceptable operative risk. A fascia iliaca compartment block was placed in the emergency department for analgesia, which substantially reduced his opioid requirement. He was taken to the operating room on hospital day one, within twenty-four hours of presentation, consistent with best practice for hip fracture.

PROCEDURE
Right total hip arthroplasty with cemented components and a ceramic-on-polyethylene bearing surface, performed 11/03/2025 by Dr. S. Bergstrom via a posterior approach. Total hip arthroplasty rather than hemiarthroplasty was selected given his independent ambulatory baseline and reasonable life expectancy. Intraoperative findings confirmed a displaced subcapital fracture with no evidence of pathologic lesion. Estimated blood loss was 350 milliliters. Tranexamic acid was administered. The patient tolerated the procedure under spinal anesthesia with sedation.

Postoperatively he was managed with multimodal analgesia including scheduled acetaminophen, a short course of low-dose oxycodone, and continuation of the regional block catheter for twenty-four hours. Codeine was avoided given his documented intolerance.

His hemoglobin fell from 12.4 preoperatively to 8.7 grams per deciliter on postoperative day one and to 8.2 on postoperative day two, consistent with acute blood loss anemia. He remained hemodynamically stable and asymptomatic without chest pain or dyspnea, and per a restrictive transfusion strategy he received no transfusion. Hemoglobin stabilized at 8.4 by postoperative day four.

Physical therapy began on postoperative day zero with weight bearing as tolerated. Posterior hip precautions were reviewed. He progressed from a rolling walker with two-person assist to a rolling walker with contact guard assist by postoperative day four, ambulating 45 meters and negotiating three stairs.

Glycemic control was managed with a basal-bolus insulin regimen while metformin was held, with glucose values ranging from 132 to 218 milligrams per deciliter. Metformin was resumed on postoperative day three once creatinine returned to baseline. Venous thromboembolism prophylaxis was provided with enoxaparin adjusted for renal function, transitioning to a planned thirty-five day course. Delirium screening with the Confusion Assessment Method was negative throughout.

Occupational therapy and case management arranged discharge to a skilled nursing facility for short-term rehabilitation, as he lives alone and had not yet reached independence with transfers.

DISCHARGE DIAGNOSES
1. Displaced subcapital fracture of the right femoral neck, Garden III, due to a fall
2. Status post right total hip arthroplasty
3. Acute blood loss anemia
4. Acute kidney injury on chronic kidney disease stage 3a, resolved
5. Type 2 diabetes mellitus without complication
6. Essential hypertension
7. Osteopenia

DISCHARGE MEDICATIONS
Enoxaparin 30 mg subcutaneously daily for thirty-five days, acetaminophen 1000 mg every eight hours, oxycodone 5 mg every six hours as needed, docusate 100 mg twice daily, metformin 1000 mg twice daily, sitagliptin 50 mg daily, amlodipine 10 mg daily, tamsulosin 0.4 mg nightly, cholecalciferol 2000 units daily and calcium carbonate 600 mg twice daily newly started.

FOLLOW-UP
Orthopedic surgery in two weeks for wound check and radiographs. Primary care in three weeks for diabetes and renal function. Referral placed for bone health evaluation and osteoporosis treatment, given a fragility fracture. Falls assessment and home safety evaluation arranged. Posterior hip precautions to be maintained for six weeks.
""",
    },
    {
        "title": "Severe Pre-eclampsia — Cesarean Delivery at 34 Weeks",
        "category": "Obstetrics",
        "expected_codes": ["O14.13", "10D00Z1", "O60.14X0", "D62."],
        "text": """DISCHARGE SUMMARY
==================
Patient: Amina Terzi, 33F | MRN: 6612905
Admission: 05/18/2026 | Discharge: 05/22/2026 | LOS: 4 days
Attending: Dr. R. Castellano, MD | Service: Obstetrics and Maternal-Fetal Medicine

CHIEF COMPLAINT
Severe headache and elevated blood pressure at 34 weeks and 2 days gestation.

HISTORY OF PRESENT ILLNESS
Ms. Terzi is a 33-year-old gravida 2 para 1 at 34 weeks and 2 days gestation by a certain last menstrual period confirmed by first-trimester ultrasound, who presented to labor and delivery triage with a two-day history of persistent frontal headache unrelieved by acetaminophen, associated with intermittent blurred vision and scotomata. She also described right upper quadrant discomfort beginning the morning of presentation. She denied vaginal bleeding, leakage of fluid, or contractions, and reported normal fetal movement.

Her prenatal course had been complicated by gestational hypertension diagnosed at 31 weeks, for which she was started on labetalol and monitored with twice-weekly blood pressure checks and weekly antenatal testing. Her prior pregnancy was complicated by pre-eclampsia without severe features, delivered vaginally at 38 weeks. She had been taking low-dose aspirin 81 mg daily from 14 weeks for pre-eclampsia prophylaxis.

On arrival, blood pressure was 172/112 mmHg, repeated at 168/108 mmHg fifteen minutes later. Heart rate was 96 beats per minute. Deep tendon reflexes were 3 plus with two beats of clonus. There was mild right upper quadrant tenderness. Fundal height was consistent with dates. Fetal heart tracing was category I with a baseline of 140 beats per minute, moderate variability, accelerations present, and no decelerations.

Laboratory studies showed platelets 96 thousand per microliter, aspartate aminotransferase 148 units per liter, alanine aminotransferase 132 units per liter, creatinine 1.1 milligrams per deciliter, and a urine protein to creatinine ratio of 1.9. Lactate dehydrogenase was 340 units per liter with a normal peripheral smear and haptoglobin, not meeting full criteria for HELLP syndrome. The diagnosis was pre-eclampsia with severe features based on severe-range blood pressures, thrombocytopenia, elevated transaminases, and neurologic symptoms.

PAST MEDICAL HISTORY
1. Pre-eclampsia without severe features in a prior pregnancy, 2022
2. Iron deficiency anemia of pregnancy
3. Subclinical hypothyroidism on levothyroxine

OBSTETRIC HISTORY
G2 P1. Prior spontaneous vaginal delivery at 38 weeks, 2022, live female infant 3,180 grams.

MEDICATIONS ON ADMISSION
Labetalol 200 mg twice daily, prenatal vitamin, ferrous sulfate 325 mg daily, aspirin 81 mg daily, levothyroxine 50 micrograms daily.

ALLERGIES
No known drug allergies.

HOSPITAL COURSE
Ms. Terzi was admitted for delivery given pre-eclampsia with severe features at 34 weeks and 2 days, which is beyond the threshold for expectant management. Magnesium sulfate was initiated for seizure prophylaxis with a 4 gram loading dose followed by a 2 gram per hour infusion, continued intrapartum and for twenty-four hours postpartum. Intravenous labetalol was given in escalating doses for acute severe-range hypertension, achieving blood pressures in the 140s over 90s. Betamethasone had been administered at 31 weeks during her initial gestational hypertension evaluation, so a rescue course was not given.

Given an unfavorable cervix at 1 centimeter, a persistent severe headache, and a downtrending platelet count from 96 to 84 thousand per microliter over eight hours, the decision was made to proceed with cesarean delivery rather than attempt induction. Neuraxial anesthesia was discussed with anesthesiology and spinal anesthesia was deemed acceptable at a platelet count above 70 thousand.

PROCEDURE
Primary low transverse cesarean delivery, performed 05/19/2026 by Dr. R. Castellano under spinal anesthesia. A live female infant was delivered in cephalic presentation with Apgar scores of 7 at one minute and 9 at five minutes, birth weight 2,140 grams, appropriate for gestational age. Arterial cord pH was 7.28. The placenta was delivered intact and sent to pathology, which subsequently demonstrated accelerated villous maturation and decidual vasculopathy consistent with hypertensive disease of pregnancy. Estimated blood loss was 900 milliliters. The uterus was closed in two layers. Oxytocin and a single dose of tranexamic acid were administered.

The infant was transferred to the neonatal intensive care unit for prematurity at 34 weeks, requiring continuous positive airway pressure for eighteen hours for transient respiratory distress, then transitioned to room air. The infant was feeding by nasogastric tube with progression to oral feeds at the time of maternal discharge and is expected to remain hospitalized for approximately two more weeks.

Postpartum, magnesium sulfate was continued for twenty-four hours with monitoring of reflexes, respiratory rate and urine output, with no evidence of toxicity. Blood pressures remained in the severe range intermittently on postpartum day one, requiring two additional doses of intravenous hydralazine, and her oral labetalol was increased to 400 mg three times daily with the addition of extended-release nifedipine 30 mg daily. By postpartum day three her pressures were consistently below 150 over 100.

Her platelet count nadired at 78 thousand per microliter on postpartum day one and recovered to 121 thousand by postpartum day three. Transaminases peaked at aspartate aminotransferase 176 units per liter and were downtrending at discharge. Hemoglobin fell from 11.2 to 8.9 grams per deciliter, consistent with operative blood loss, and she was managed with oral iron rather than transfusion given hemodynamic stability and minimal symptoms.

She was counselled extensively about postpartum pre-eclampsia, which can present or worsen up to six weeks after delivery, and given specific return precautions. Lactation support was provided with pumping for the infant in the neonatal intensive care unit, and her antihypertensive regimen was selected to be compatible with breastfeeding.

DISCHARGE DIAGNOSES
1. Pre-eclampsia with severe features, third trimester
2. Status post primary low transverse cesarean delivery at 34 weeks and 2 days
3. Preterm delivery, 34 weeks
4. Thrombocytopenia complicating pregnancy and the puerperium, improving
5. Acute blood loss anemia
6. Subclinical hypothyroidism

DISCHARGE MEDICATIONS
Labetalol 400 mg three times daily, nifedipine extended release 30 mg daily, ibuprofen 600 mg every six hours as needed, acetaminophen 1000 mg every eight hours, oxycodone 5 mg every six hours as needed with a quantity of ten tablets, ferrous sulfate 325 mg twice daily with vitamin C, docusate 100 mg twice daily, levothyroxine 50 micrograms daily, prenatal vitamin continued while breastfeeding.

FOLLOW-UP
Blood pressure check in the obstetric clinic in three days, which is standard for hypertensive disorders of pregnancy. Postpartum visit in two weeks rather than the usual six. Neonatal intensive care unit visitation and lactation support ongoing. Return immediately for headache unrelieved by acetaminophen, visual changes, right upper quadrant pain, shortness of breath, or a blood pressure above 160 over 110. Counselled that a history of pre-eclampsia confers elevated lifetime cardiovascular risk and warrants long-term primary care follow-up.
"""
    },
    {
        "title": "Motor Vehicle Collision — Multiple Rib Fractures and Hemopneumothorax",
        "category": "Trauma Surgery",
        "expected_codes": ["S22.42XA", "S22.5XXA", "S27.2XXA", "0W9B30Z", "S27.321A", "V43.52XA", "J96.01", "D62."],
        "text": """DISCHARGE SUMMARY
==================
Patient: Curtis Delahunt, 46M | MRN: 8873316
Admission: 07/09/2026 | Discharge: 07/16/2026 | LOS: 7 days
Attending: Dr. M. Ashworth, MD | Service: Trauma and Acute Care Surgery

CHIEF COMPLAINT
Chest pain and shortness of breath after a motor vehicle collision.

HISTORY OF PRESENT ILLNESS
Mr. Delahunt is a 46-year-old previously healthy man who was the restrained driver of a sedan struck on the driver side at an intersection by a vehicle travelling at approximately 45 miles per hour. There was intrusion into the driver compartment and prolonged extrication of about twenty minutes. Airbags deployed. He did not lose consciousness and recalled the event clearly.

He was brought in by ground emergency medical services on a backboard with a cervical collar in place, complaining of severe left-sided chest pain worse with inspiration, and progressive shortness of breath during transport. He denied abdominal pain, and reported no head strike, neck pain, or extremity deformity.

On arrival to the trauma bay, primary survey showed a patent airway, decreased breath sounds at the left base with paradoxical chest wall motion over the left lateral chest, and palpable radial pulses. Vital signs were blood pressure 104/68 mmHg, heart rate 118 beats per minute, respiratory rate 28, oxygen saturation 89% on room air improving to 94% on a non-rebreather, and Glasgow Coma Scale 15. Extended focused assessment with sonography for trauma was negative for pericardial or intraperitoneal free fluid but showed absent lung sliding on the left.

Chest radiograph demonstrated left-sided rib fractures with a moderate hemopneumothorax. CT of the chest, abdomen and pelvis with contrast showed fractures of the left fourth through ninth ribs, with segmental fractures of the fifth, sixth and seventh ribs producing a flail segment, a left hemopneumothorax with approximately 400 milliliters of blood, and an underlying pulmonary contusion involving the left lower lobe. There was no aortic injury, no solid organ injury, and no pelvic fracture. CT of the head and cervical spine were negative and the collar was cleared clinically.

PAST MEDICAL HISTORY
1. Seasonal allergic rhinitis
2. Otherwise healthy, no chronic conditions

PAST SURGICAL HISTORY
None.

MEDICATIONS ON ADMISSION
Loratadine as needed.

ALLERGIES
No known drug allergies.

SOCIAL HISTORY
Never smoker. Occasional alcohol. Works as an electrician. Lives with his partner and two school-age children.

HOSPITAL COURSE
A left tube thoracostomy was placed in the trauma bay with immediate return of 420 milliliters of blood and a large air leak, with subsequent improvement in oxygen saturation to 97% on 4 liters by nasal cannula. He was admitted to the surgical intensive care unit for management of a flail chest with pulmonary contusion.

PROCEDURE
Left tube thoracostomy, 32 French, performed 07/09/2026 in the trauma bay by Dr. M. Ashworth. Drainage of 420 milliliters of blood on insertion. The tube was placed in the fifth intercostal space at the anterior axillary line and directed posteriorly.

The central management problem was analgesia. Inadequate pain control with a flail segment leads to splinting, atelectasis, and pneumonia, and this drove his course. Acute pain service placed a thoracic epidural catheter on hospital day one, which substantially improved his incentive spirometry volumes from 750 to 1,800 milliliters and allowed effective coughing. He also received scheduled acetaminophen, ketorolac for a limited course, and gabapentin, with intravenous opioid used sparingly as breakthrough.

He was monitored for respiratory failure. On hospital day two he developed worsening hypoxemia with oxygen saturations in the high 80s on 6 liters, and a chest radiograph showed progression of the left lower lobe contusion with new atelectasis. He was placed on high-flow nasal cannula at 40 liters per minute and 50% fraction of inspired oxygen, with aggressive pulmonary toilet, chest physiotherapy, and early mobilization. He did not require intubation or mechanical ventilation. By hospital day four he was weaned to 2 liters by nasal cannula and by hospital day six to room air.

Surgical stabilization of rib fractures was considered given the flail segment. After multidisciplinary discussion, operative fixation was deferred because his respiratory status was improving on non-invasive support, he had never required mechanical ventilation, and his pain was well controlled on the epidural.

The chest tube air leak resolved on hospital day three. The tube was placed to water seal on hospital day four, and a repeat chest radiograph showed full lung expansion with no recurrent pneumothorax. The tube was removed on hospital day five, with a post-pull radiograph confirming no recurrence.

His hemoglobin fell from 14.1 on presentation to 9.8 grams per deciliter by hospital day two, reflecting hemothorax and ongoing contusion, and stabilized at 9.6 without transfusion. Venous thromboembolism prophylaxis with enoxaparin was started at twenty-four hours after confirming no intracranial or solid organ injury. He had no fever and no evidence of pneumonia or empyema throughout.

The epidural was removed on hospital day five and he transitioned to oral analgesia. Physical and occupational therapy cleared him for discharge home with his partner. Trauma social work provided counselling regarding the collision and screened for acute stress symptoms, which were present but mild, and outpatient resources were provided.

DISCHARGE DIAGNOSES
1. Multiple fractures of the left ribs, fourth through ninth, with flail chest
2. Traumatic hemopneumothorax on the left
3. Pulmonary contusion of the left lower lobe
4. Acute respiratory failure with hypoxia, resolved without intubation
5. Acute blood loss anemia
6. Status post left tube thoracostomy
7. Driver injured in a motor vehicle collision

DISCHARGE MEDICATIONS
Acetaminophen 1000 mg every eight hours scheduled, ibuprofen 600 mg every eight hours with food, gabapentin 300 mg three times daily with a taper plan, oxycodone 5 mg every six hours as needed for severe pain with a quantity of twenty tablets, docusate 100 mg twice daily, incentive spirometer to be used ten times hourly while awake.

FOLLOW-UP
Trauma surgery clinic in two weeks with an upright chest radiograph. Primary care in three weeks. No lifting over fifteen pounds and no return to electrical work for six weeks. Instructed to continue incentive spirometry and to return for fever, worsening shortness of breath, productive cough, or a sudden increase in chest pain, given the ongoing risk of pneumonia and delayed hemothorax after rib fractures.
"""
    },
    {
        "title": "Acute Ischemic Stroke — Mechanical Thrombectomy for MCA Occlusion",
        "category": "Neurology / Neurointervention",
        "expected_codes": ["I63.412", "03CG3ZZ", "I48.91", "I10.", "R47.01", "G81.91", "E78.5"],
        "text": """DISCHARGE SUMMARY
==================
Patient: Beatrice Nwachukwu, 71F | MRN: 4429078
Admission: 02/14/2026 | Discharge: 02/21/2026 | LOS: 7 days
Attending: Dr. K. Lindqvist, MD | Service: Neurology / Stroke

CHIEF COMPLAINT
Sudden right-sided weakness and inability to speak.

HISTORY OF PRESENT ILLNESS
Ms. Nwachukwu is a 71-year-old right-handed woman with hypertension and hyperlipidemia who was witnessed by her son to develop sudden onset right-sided weakness and expressive difficulty while eating breakfast. Last known well was 08:15. Emergency medical services were activated immediately and she arrived at 08:52, thirty-seven minutes from onset.

On arrival she was awake with a global aphasia, right facial droop, right hemiplegia with no antigravity movement in the arm and minimal movement in the leg, and a right visual field deficit. National Institutes of Health Stroke Scale score was 19. Blood pressure was 186/98 mmHg, heart rate 104 beats per minute and irregularly irregular. Fingerstick glucose was 118 milligrams per deciliter.

Non-contrast CT of the head showed no hemorrhage with an Alberta Stroke Program Early CT Score of 9 and a hyperdense left middle cerebral artery sign. CT angiography of the head and neck demonstrated an occlusion of the left middle cerebral artery at the M1 segment. CT perfusion showed a core infarct volume of 14 milliliters with a penumbra of 96 milliliters, giving a favorable mismatch ratio.

Electrocardiogram demonstrated atrial fibrillation with a rapid ventricular response, new to the patient with no prior documented diagnosis. She had not been on anticoagulation.

PAST MEDICAL HISTORY
1. Essential hypertension, fifteen years
2. Hyperlipidemia
3. Osteoarthritis
4. No prior stroke or transient ischemic attack

MEDICATIONS ON ADMISSION
Amlodipine 5 mg daily, atorvastatin 20 mg nightly.

ALLERGIES
No known drug allergies.

SOCIAL HISTORY
Never smoker. Lives with her son. Independent in all activities of daily living prior to this event, walking without an aid and managing her own finances and medications. Retired schoolteacher.

HOSPITAL COURSE
She was evaluated by the stroke team on arrival. Intravenous thrombolysis with tenecteplase was administered at 09:14, fifty-nine minutes from last known well and twenty-two minutes from door, with no contraindications identified. She was simultaneously taken for mechanical thrombectomy given a large vessel occlusion with a favorable perfusion profile.

PROCEDURE
Cerebral angiography with mechanical thrombectomy of the left middle cerebral artery, performed 02/14/2026 by Dr. A. Ferreira, interventional neuroradiology. Right common femoral arterial access was obtained. Angiography confirmed a left M1 occlusion with Thrombolysis in Cerebral Infarction grade 0 flow. A stent retriever was deployed with aspiration assistance. Two passes achieved TICI 2b to 3 reperfusion. Groin puncture to reperfusion time was 34 minutes. Total time from last known well to reperfusion was 2 hours and 11 minutes. There were no procedural complications, no vessel perforation, and no distal embolization to a new territory.

She was admitted to the neurologic intensive care unit for post-thrombectomy monitoring. Repeat CT of the head at twenty-four hours showed a small established infarct in the left basal ganglia and insular cortex without hemorrhagic transformation. Her NIHSS improved dramatically from 19 on arrival to 7 at twenty-four hours and to 4 by hospital day three, with substantial recovery of right-sided strength and marked improvement in her aphasia, which evolved from global to a mild expressive aphasia with intact comprehension.

The etiology was determined to be cardioembolic secondary to newly diagnosed atrial fibrillation, with a CHA2DS2-VASc score of 5. Transthoracic echocardiography showed a left ventricular ejection fraction of 55% with mild left atrial enlargement and no intracardiac thrombus. Carotid imaging on the CT angiogram showed no significant extracranial stenosis. Telemetry confirmed persistent atrial fibrillation.

Anticoagulation was deliberately delayed given the infarct size and recent thrombolysis, and apixaban was initiated on hospital day five following a repeat CT showing no hemorrhagic transformation. Rate control was achieved with metoprolol. Her home amlodipine was continued and her atorvastatin was increased to 80 mg nightly for high-intensity statin therapy after a low-density lipoprotein of 132 milligrams per deciliter.

She underwent a formal swallow evaluation on arrival, initially failing with a recommendation for nil per os, then passing on hospital day two and advancing to a regular diet with thin liquids. Physical, occupational and speech therapy worked with her daily. By discharge she was ambulating 60 meters with a rolling walker and contact guard assist, and her modified Rankin Scale score was 2 compared with 0 at baseline.

She had no seizures, no fever, and no evidence of aspiration pneumonia or urinary tract infection during the admission. Deep vein thrombosis prophylaxis was maintained with intermittent pneumatic compression until anticoagulation began.

DISCHARGE DIAGNOSES
1. Acute ischemic stroke of the left middle cerebral artery territory, cardioembolic
2. Status post intravenous thrombolysis and mechanical thrombectomy with TICI 2b to 3 reperfusion
3. Atrial fibrillation, new diagnosis, CHA2DS2-VASc 5
4. Expressive aphasia, improving
5. Right hemiparesis, improving
6. Essential hypertension
7. Hyperlipidemia

DISCHARGE MEDICATIONS
Apixaban 5 mg twice daily, metoprolol succinate 50 mg daily, amlodipine 5 mg daily, atorvastatin 80 mg nightly, acetaminophen as needed. Aspirin discontinued given initiation of anticoagulation.

FOLLOW-UP
Discharged to acute inpatient rehabilitation. Stroke clinic in four weeks. Cardiology in three weeks for atrial fibrillation management. Repeat lipid panel and liver function in six weeks. Counselled on stroke warning signs and the importance of anticoagulation adherence, including that missing doses substantially raises recurrence risk. Driving restricted pending neurologic clearance.
"""
    },
]
