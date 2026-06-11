"use client"

import { useEffect, useState } from "react"
import { Users, Database, Zap, TrendingUp, AlertCircle } from "lucide-react"
import { StatsTrend } from "@/components/ui/stats-trend"
import { useAuth } from "@/hooks/use-auth"
import { fetchAdminStats, AdminStatsResponse } from "@/lib/api"

export function AdminStats() {
  const { session } = useAuth()
  const [stats, setStats] = useState<AdminStatsResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!session?.access_token) return
    fetchAdminStats(session.access_token)
      .then(setStats)
      .catch((e) => setError(e.message))
  }, [session])

  if (error) {
    return (
      <div className="p-4 rounded-xl border border-destructive/30 bg-destructive/10 text-destructive flex items-center gap-2">
        <AlertCircle className="w-5 h-5" />
        <p className="text-sm font-medium">Failed to load stats: {error}</p>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 animate-pulse">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-28 rounded-xl bg-muted" />
        ))}
      </div>
    )
  }

  const adminStats = [
    {
      label: "Active Users",
      value: stats.active_doctors,
      icon: <Users className="w-5 h-5" />,
      iconColor: "teal" as const,
    },
    {
      label: "Total Predictions",
      value: stats.total_predictions,
      icon: <Database className="w-5 h-5" />,
      iconColor: "gold" as const,
    },
    {
      label: "Chat Sessions",
      value: stats.total_chat_sessions,
      icon: <Zap className="w-5 h-5" />,
      iconColor: "teal" as const,
    },
    {
      label: "Avg User Rating",
      value: stats.avg_rating ? `${stats.avg_rating.toFixed(1)} / 5.0` : "N/A",
      icon: <TrendingUp className="w-5 h-5" />,
      iconColor: "gold" as const,
    },
  ]

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {adminStats.map((stat, i) => (
        <div key={i} className={`animate-fade-in stagger-${i + 1}`}>
          <StatsTrend {...stat} />
        </div>
      ))}
    </div>
  )
}
