"use client"

import { useState } from "react"
import { FlaskConical, ChevronDown } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"

const sampleNotes = {
  Cardiology: {
    "Heart Failure": "68-year-old male with 2-week history of progressive dyspnea, orthopnea, and lower extremity edema. Presents with fatigue and reduced exercise tolerance. Physical exam reveals elevated JVP, bilateral crackles, and 2+ pitting edema. Echocardiogram shows EF 35% with global hypokinesis. BNP elevated at 850 pg/mL. Patient on lisinopril and metoprolol but inadequately controlled.",
    "Acute Coronary Syndrome": "62-year-old female presenting with 3 hours of substernal chest pressure radiating to left arm, associated with diaphoresis and nausea. Onset during rest. EKG shows 2mm ST elevation in leads II, III, aVF. Troponin I: 2.4 ng/mL. History of hypertension and smoking. Denies prior cardiac history.",
  },
  Pulmonary: {
    "Pneumonia": "45-year-old male with 5-day fever, productive cough with green sputum, dyspnea, and pleuritic chest pain. Recent URI. Temp 39.2C, RR 24, O2 sat 92%. CXR shows left lower lobe consolidation. WBC 14.2. Procalcitonin 2.1. No prior lung disease.",
    "COPD Exacerbation": "72-year-old male with 40-pack-year smoking history presenting with acute worsening of baseline dyspnea, increased sputum production, and wheezing. Peak flow 180 (baseline 320). Using rescue inhaler 10x daily. Recent upper respiratory infection. On tiotropium and albuterol maintenance.",
  },
  "Infectious Disease": {
    "Sepsis": "55-year-old female with fever (40.1C), tachycardia (HR 118), tachypnea (RR 22), hypotension (BP 92/58), and altered mental status. Source: UTI with positive urine culture (E. coli). WBC 16.5, lactate 3.2, glucose 245. CRP 24. No recent antibiotics. Confused, appearing toxic.",
    "Meningitis": "28-year-old male with severe frontal headache, fever (39.8C), neck stiffness, photophobia, and confusion. Rash noted on trunk. Kernig and Brudzinski signs positive. CSF: elevated protein (180), low glucose (35), elevated WBC (850 neutrophils). Gram stain pending.",
  },
  Renal: {
    "Acute Kidney Injury": "64-year-old male with sudden rise in creatinine from baseline 1.0 to 3.2 mg/dL over 2 days. Oliguria (UOP 280 mL/24h). Recent contrast CT scan 3 days ago. Urine Na 12, FENa 0.8%. No recent NSAID use. BP 165/95. History of DM2 and HTN. Urine dipstick negative for protein/blood.",
    "Chronic Kidney Disease": "58-year-old female with CKD stage 3b, baseline Cr 1.8, eGFR 38. Proteinuria 2.5 g/24h. HTN controlled on amlodipine and lisinopril. DM2 on metformin. Recent UA shows RBC casts. Anemia of CKD, Hgb 10.2. Renal ultrasound shows normal-sized kidneys with increased echogenicity.",
  },
}

export function NoteInput({ onAnalyze }: { onAnalyze: (note: string) => void }) {
  const [category, setCategory] = useState<string>("Cardiology")
  const [scenario, setScenario] = useState<string>("Heart Failure")
  const [note, setNote] = useState<string>(sampleNotes["Cardiology" as keyof typeof sampleNotes]["Heart Failure"])
  const [isLoading, setIsLoading] = useState(false)

  const categories = Object.keys(sampleNotes)
  const scenarios = Object.keys(sampleNotes[category as keyof typeof sampleNotes])
  const wordCount = note.split(/\s+/).filter(w => w.length > 0).length
  const tokenEstimate = Math.ceil(wordCount * 1.3)
  const exceedsLimit = tokenEstimate > 512

  const handleCategoryChange = (newCategory: string) => {
    setCategory(newCategory)
    const newScenario = Object.keys(sampleNotes[newCategory as keyof typeof sampleNotes])[0]
    setScenario(newScenario)
    setNote(sampleNotes[newCategory as keyof typeof sampleNotes][newScenario as keyof typeof sampleNotes[keyof typeof sampleNotes]])
  }

  const handleScenarioChange = (newScenario: string) => {
    setScenario(newScenario)
    setNote(sampleNotes[category as keyof typeof sampleNotes][newScenario as keyof typeof sampleNotes[keyof typeof sampleNotes]])
  }

  const handleAnalyze = async () => {
    setIsLoading(true)
    await new Promise(resolve => setTimeout(resolve, 1500))
    onAnalyze(note)
    setIsLoading(false)
  }

  return (
    <GlassCard className="flex flex-col h-full space-y-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">
          <FlaskConical className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h2 className="font-medium text-foreground">Clinical Note Input</h2>
          <p className="text-xs text-foreground-muted">Select or paste a clinical note</p>
        </div>
      </div>

      <div className="space-y-3">
        {/* Category selector */}
        <div>
          <label className="text-xs text-foreground-muted uppercase tracking-wider block mb-2">Category</label>
          <div className="relative">
            <select
              value={category}
              onChange={(e) => handleCategoryChange(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-white/[0.06] border border-white/[0.08] text-foreground text-sm focus:outline-none focus:border-primary/50 appearance-none"
            >
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground-muted pointer-events-none" />
          </div>
        </div>

        {/* Scenario selector */}
        <div>
          <label className="text-xs text-foreground-muted uppercase tracking-wider block mb-2">Scenario</label>
          <div className="relative">
            <select
              value={scenario}
              onChange={(e) => handleScenarioChange(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-white/[0.06] border border-white/[0.08] text-foreground text-sm focus:outline-none focus:border-primary/50 appearance-none"
            >
              {scenarios.map(scen => (
                <option key={scen} value={scen}>{scen}</option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground-muted pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Textarea */}
      <textarea
        value={note}
        onChange={(e) => setNote(e.target.value)}
        placeholder="Enter or paste clinical note here..."
        className={`flex-1 min-h-64 p-3 rounded-lg bg-white/[0.04] border ${
          exceedsLimit ? "border-destructive" : "border-white/[0.08]"
        } text-foreground text-sm font-mono focus:outline-none focus:border-primary/50 resize-none placeholder:text-foreground-subtle`}
      />

      {/* Token counter */}
      <div className="flex items-center justify-between text-xs">
        <span className="text-foreground-muted">
          {wordCount} words (~{tokenEstimate} tokens)
        </span>
        <span className={exceedsLimit ? "text-destructive" : "text-foreground-muted"}>
          {exceedsLimit ? "Exceeds 512 token limit" : ""}
        </span>
      </div>

      {/* Analyze button */}
      <button
        onClick={handleAnalyze}
        disabled={isLoading || note.trim().length === 0 || exceedsLimit}
        className="w-full px-4 py-3 rounded-lg bg-primary text-primary-foreground font-medium hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-[0_0_20px_rgba(78,205,196,0.3)] flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
            Analyzing...
          </>
        ) : (
          <>
            <FlaskConical className="w-4 h-4" />
            Analyze with ShifaMind
          </>
        )}
      </button>
    </GlassCard>
  )
}
