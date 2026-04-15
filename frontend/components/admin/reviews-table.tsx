"use client"

import { useEffect, useState } from "react"
import { Star, TrendingUp, AlertCircle } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { useAuth } from "@/hooks/use-auth"
import { fetchAdminReviews, ReviewListResponse } from "@/lib/api"

const statusColors = {
  helpful: { bg: "bg-primary/20", text: "text-primary", border: "border-primary/30" },
  partial: { bg: "bg-gold/20", text: "text-gold", border: "border-gold/30" },
  incorrect: { bg: "bg-destructive/20", text: "text-destructive", border: "border-destructive/30" },
}

function StarRating({ score }: { score: number }) {
  return (
    <div className="flex gap-1">
      {[...Array(5)].map((_, i) => (
        <Star
          key={i}
          className={`w-3 h-3 ${
            i < score ? "fill-gold text-gold" : "text-foreground-subtle"
          }`}
        />
      ))}
    </div>
  )
}

function getStatus(rating: number): "helpful" | "partial" | "incorrect" {
  if (rating >= 4) return "helpful"
  if (rating === 3) return "partial"
  return "incorrect"
}

export function ReviewsTable() {
  const { session } = useAuth()
  const [data, setData] = useState<ReviewListResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!session?.access_token) return
    fetchAdminReviews(session.access_token)
      .then(setData)
      .catch((e) => setError(e.message))
  }, [session])

  if (error) {
    return (
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 text-destructive">
          <AlertCircle className="w-5 h-5" />
          <p className="text-sm font-medium">Failed to load reviews: {error}</p>
        </div>
      </GlassCard>
    )
  }

  if (!data) {
    return (
      <GlassCard className="space-y-6 animate-pulse">
        <div className="h-6 w-48 bg-white/[0.04] rounded" />
        <div className="h-64 bg-white/[0.04] rounded-lg mt-4" />
      </GlassCard>
    )
  }

  const reviews = data.reviews
  const avgScore = reviews.length ? (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1) : "0.0"
  const helpfulCount = reviews.filter((r) => r.rating >= 4).length
  const accuracyRate = reviews.length ? ((helpfulCount / reviews.length) * 100).toFixed(0) : "0"

  return (
    <GlassCard className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-semibold text-foreground">User Reviews & Feedback</h3>
          <p className="text-sm text-foreground-muted mt-1">{data.total} feedback entries</p>
        </div>
        {reviews.length > 0 && (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/[0.06] border border-white/[0.08]">
            <TrendingUp className="w-4 h-4 text-primary" />
            <span className="text-sm font-semibold text-foreground">{accuracyRate}%</span>
            <span className="text-xs text-foreground-muted">helpful</span>
          </div>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/[0.08]">
              <th className="text-left py-3 px-4 text-xs font-semibold text-foreground-muted uppercase">
                User
              </th>
              <th className="text-left py-3 px-4 text-xs font-semibold text-foreground-muted uppercase">
                Diagnosis Context
              </th>
              <th className="text-left py-3 px-4 text-xs font-semibold text-foreground-muted uppercase">
                Quality
              </th>
              <th className="text-left py-3 px-4 text-xs font-semibold text-foreground-muted uppercase">
                Status
              </th>
              <th className="text-left py-3 px-4 text-xs font-semibold text-foreground-muted uppercase">
                Date
              </th>
            </tr>
          </thead>
          <tbody>
            {reviews.length === 0 && (
              <tr>
                <td colSpan={5} className="py-8 text-center text-foreground-muted">
                  No reviews submitted yet.
                </td>
              </tr>
            )}
            {reviews.map((review) => {
              const status = getStatus(review.rating)
              const colors = statusColors[status]
              const dateStr = new Date(review.created_at).toLocaleDateString()
              
              return (
                <tr key={review.id} className="border-b border-white/[0.06] hover:bg-white/[0.03] transition-colors">
                  <td className="py-3 px-4 max-w-[200px]">
                    <div className="font-medium text-foreground truncate">{review.doctor?.full_name || 'Unknown'}</div>
                    <div className="text-xs text-foreground-muted truncate">{review.doctor?.email}</div>
                  </td>
                  <td className="py-3 px-4 max-w-[250px]">
                    <div className="text-sm text-foreground-muted truncate">
                      {review.prediction?.input_text || 'No context provided'}
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex gap-2 items-center">
                      <StarRating score={review.rating} />
                      <span className="text-xs font-medium text-foreground ml-1">
                        {review.rating}.0
                      </span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${colors.bg} ${colors.text} border ${colors.border}`}
                    >
                      {status.charAt(0).toUpperCase() + status.slice(1)}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-foreground-muted text-xs">{dateStr}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Average Score Card */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-4 border-t border-white/[0.08]">
        <div>
          <p className="text-xs text-foreground-muted mb-1">Average Score</p>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-semibold text-primary">{avgScore}</span>
            <span className="text-xs text-foreground-muted">/5.0</span>
          </div>
        </div>
        <div>
          <p className="text-xs text-foreground-muted mb-1">Helpful (4-5 stars)</p>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-semibold text-primary">{helpfulCount}</span>
            <span className="text-xs text-foreground-muted">/ {reviews.length}</span>
          </div>
        </div>
        <div>
          <p className="text-xs text-foreground-muted mb-1">Accuracy Rate</p>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-semibold text-gold">
              {accuracyRate}%
            </span>
          </div>
        </div>
      </div>
    </GlassCard>
  )
}
