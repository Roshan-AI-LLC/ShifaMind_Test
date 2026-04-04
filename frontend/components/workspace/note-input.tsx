"use client"

import { useEffect, useMemo, useState } from "react"
import { FlaskConical, Loader2 } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useAuth } from "@/hooks/use-auth"
import { listSampleNotes, type SampleNote } from "@/lib/api"

export function NoteInput({ onAnalyze }: { onAnalyze: (note: string) => void }) {
  const { session } = useAuth()
  const [note, setNote] = useState<string>("")
  const [isLoading, setIsLoading] = useState(false)
  const [samples, setSamples] = useState<SampleNote[]>([])
  const [samplesLoading, setSamplesLoading] = useState(false)
  const [samplesError, setSamplesError] = useState<string | null>(null)
  const [templatePickerKey, setTemplatePickerKey] = useState(0)

  const wordCount = note.split(/\s+/).filter((w) => w.length > 0).length
  const tokenEstimate = Math.ceil(wordCount * 1.3)
  const exceedsLimit = tokenEstimate > 1024

  useEffect(() => {
    const token = session?.access_token
    if (!token) {
      setSamples([])
      setSamplesError(null)
      return
    }
    let cancelled = false
    setSamplesLoading(true)
    setSamplesError(null)
    listSampleNotes(token)
      .then((rows) => {
        if (!cancelled) setSamples(rows)
      })
      .catch((e: Error) => {
        if (!cancelled) setSamplesError(e.message ?? "Failed to load templates")
      })
      .finally(() => {
        if (!cancelled) setSamplesLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [session?.access_token])

  const samplesByCategory = useMemo(() => {
    const m = new Map<string, SampleNote[]>()
    for (const n of samples) {
      const cat = n.category?.trim() || "Other"
      if (!m.has(cat)) m.set(cat, [])
      m.get(cat)!.push(n)
    }
    return [...m.entries()].sort(([a], [b]) => a.localeCompare(b))
  }, [samples])

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

      <div className="space-y-2">
        <div className="flex items-center justify-between gap-2">
          <label className="text-xs font-medium text-foreground-muted">Sample templates</label>
          {samplesLoading && (
            <Loader2 className="w-3.5 h-3.5 animate-spin text-foreground-subtle" aria-hidden />
          )}
        </div>
        <Select
          key={templatePickerKey}
          disabled={!session?.access_token || samplesLoading || samples.length === 0}
          onValueChange={(id) => {
            const picked = samples.find((s) => s.id === id)
            if (picked) setNote(picked.text)
            setTemplatePickerKey((k) => k + 1)
          }}
        >
          <SelectTrigger
            size="sm"
            className="w-full max-w-none border-white/[0.08] bg-white/[0.04] text-foreground text-xs h-9"
          >
            <SelectValue
              placeholder={
                !session?.access_token
                  ? "Sign in to load templates"
                  : samplesLoading
                    ? "Loading templates…"
                    : samples.length === 0
                      ? "No templates available"
                      : "Choose a template to try…"
              }
            />
          </SelectTrigger>
          <SelectContent className="max-h-72 border-white/[0.08] bg-[#0f1419] text-foreground">
            {samplesByCategory.map(([category, rows]) => (
              <SelectGroup key={category}>
                <SelectLabel className="text-foreground-subtle text-[10px] uppercase tracking-wide">
                  {category}
                </SelectLabel>
                {rows.map((s) => (
                  <SelectItem
                    key={s.id}
                    value={s.id}
                    className="text-xs focus:bg-white/[0.08] focus:text-foreground"
                  >
                    <span className="truncate">{s.title}</span>
                  </SelectItem>
                ))}
              </SelectGroup>
            ))}
          </SelectContent>
        </Select>
        {samplesError && (
          <p className="text-[11px] text-destructive leading-snug">
            {samplesError}
            <span className="text-foreground-subtle block mt-0.5">
              Check that the API is running and <code className="text-foreground-muted">NEXT_PUBLIC_API_URL</code>{" "}
              points to it. Seed notes with{" "}
              <code className="text-foreground-muted">python scripts/seed_notes.py</code>.
            </span>
          </p>
        )}
        {!samplesError &&
          !samplesLoading &&
          session?.access_token &&
          samples.length === 0 && (
          <p className="text-[11px] text-foreground-subtle leading-snug">
            No rows in <code className="text-foreground-muted">sample_notes</code>. Run{" "}
            <code className="text-foreground-muted">python scripts/seed_notes.py</code> against your Supabase project.
          </p>
        )}
      </div>

      <textarea
        value={note}
        onChange={(e) => setNote(e.target.value)}
        placeholder="Paste clinical note here…"
        className={`flex-1 min-h-64 p-3 rounded-lg bg-white/[0.04] border ${
          exceedsLimit ? "border-destructive" : "border-white/[0.08]"
        } text-foreground text-sm font-mono focus:outline-none focus:border-primary/50 resize-none placeholder:text-foreground-subtle`}
      />

      <div className="flex items-center justify-between text-xs">
        <span className="text-foreground-muted">
          {wordCount} words (~{tokenEstimate} tokens)
        </span>
        <span className={exceedsLimit ? "text-destructive" : "text-foreground-muted"}>
          {exceedsLimit ? "Exceeds 1024 token limit — note will be truncated" : ""}
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
