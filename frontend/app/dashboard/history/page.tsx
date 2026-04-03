"use client"

import { useEffect, useState } from "react"
import { GlassCard } from "@/components/ui/glass-card"
import { HistoryCard } from "@/components/ui/history-card"
import { useAuth } from "@/hooks/use-auth"
import { createClient } from "@/lib/supabase"
import { History } from "lucide-react"

interface HistoryEntry {
  id: string
  date: string
  diagnosis: string
  content: string
  codes: { code: string; label: string; confidence: number }[]
  userFeedback?: string
}

export default function HistoryPage() {
  const { user } = useAuth()
  const [predictions, setPredictions] = useState<HistoryEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [expandedId, setExpandedId] = useState<string | null>(null)

  useEffect(() => {
    if (!user) return
    const supabase = createClient()
    supabase
      .from("predictions")
      .select("id, text, predictions, created_at")
      .eq("user_id", user.id)
      .order("created_at", { ascending: false })
      .limit(50)
      .then(({ data, error }) => {
        if (error || !data) { setIsLoading(false); return }
        const entries: HistoryEntry[] = data.map((row) => {
          const preds: any[] = row.predictions ?? []
          const topAbove = preds.filter((p) => p.above_threshold)
          const topDiag = topAbove[0]?.description ?? preds[0]?.description ?? "Unknown"
          return {
            id: row.id,
            date: new Date(row.created_at).toLocaleString(),
            diagnosis: topDiag,
            content: row.text ?? "",
            codes: preds.slice(0, 3).map((p) => ({
              code: p.code,
              label: p.description,
              confidence: p.confidence,
            })),
          }
        })
        setPredictions(entries)
        setIsLoading(false)
      })
  }, [user])

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Prediction History</h1>
          <p className="text-foreground-muted mt-1">Review your past analyses and predictions</p>
        </div>
        <span className="px-3 py-1 rounded-full text-sm font-medium bg-white/[0.06] text-foreground-muted w-fit">
          {predictions.length} predictions
        </span>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-16">
          <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
      ) : predictions.length === 0 ? (
        <GlassCard className="flex flex-col items-center justify-center py-16">
          <div className="w-16 h-16 rounded-2xl bg-white/[0.06] flex items-center justify-center">
            <History className="w-8 h-8 text-foreground-subtle" />
          </div>
          <h2 className="text-lg font-medium text-foreground mt-6">No predictions yet</h2>
          <p className="text-foreground-muted text-sm mt-1 text-center max-w-sm">
            Go to the Workspace to analyze your first clinical note.
          </p>
        </GlassCard>
      ) : (
        <div className="space-y-3">
          {predictions.map((prediction, index) => (
            <div key={prediction.id} className={`animate-fade-in stagger-${Math.min(index + 1, 6)}`}>
              <HistoryCard
                {...prediction}
                onExpand={(id) => setExpandedId(expandedId === id ? null : id)}
                isExpanded={expandedId === prediction.id}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
