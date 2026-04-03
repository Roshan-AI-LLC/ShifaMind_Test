"use client"

import { useState } from "react"
import { FlaskConical } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"

export function NoteInput({ onAnalyze }: { onAnalyze: (note: string) => void }) {
  const [note, setNote] = useState<string>("")
  const [isLoading, setIsLoading] = useState(false)

  const wordCount = note.split(/\s+/).filter(w => w.length > 0).length
  const tokenEstimate = Math.ceil(wordCount * 1.3)
  const exceedsLimit = tokenEstimate > 6144

  const handleAnalyze = async () => {
    setIsLoading(true)
    await onAnalyze(note)
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
          <p className="text-xs text-foreground-muted">Paste a discharge summary or clinical note</p>
        </div>
      </div>

      <textarea
        value={note}
        onChange={(e) => setNote(e.target.value)}
        placeholder="Paste clinical note here..."
        className={`flex-1 min-h-64 p-3 rounded-lg bg-white/[0.04] border ${
          exceedsLimit ? "border-destructive" : "border-white/[0.08]"
        } text-foreground text-sm font-mono focus:outline-none focus:border-primary/50 resize-none placeholder:text-foreground-subtle`}
      />

      <div className="flex items-center justify-between text-xs">
        <span className="text-foreground-muted">
          {wordCount} words (~{tokenEstimate} tokens)
        </span>
        <span className={exceedsLimit ? "text-destructive" : "text-foreground-muted"}>
          {exceedsLimit ? "Exceeds 6144 token limit" : ""}
        </span>
      </div>

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
