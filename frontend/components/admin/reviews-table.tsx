"use client"

import { Star, TrendingUp, TrendingDown } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"

interface Review {
  id: string
  user: string
  diagnosis: string
  overallScore: number
  accuracy: number
  interpretability: number
  comment: string
  date: string
  status: "helpful" | "partial" | "incorrect"
}

const reviews: Review[] = [
  {
    id: "rev-001",
    user: "Dr. Sarah Smith",
    diagnosis: "Type 2 Diabetes Mellitus",
    overallScore: 5,
    accuracy: 5,
    interpretability: 5,
    comment: "Excellent analysis with clear supporting evidence.",
    date: "Jan 15, 2024",
    status: "helpful",
  },
  {
    id: "rev-002",
    user: "Dr. James Wilson",
    diagnosis: "Hypertensive Crisis",
    overallScore: 4,
    accuracy: 4,
    interpretability: 5,
    comment: "Good predictions but missed one important differential.",
    date: "Jan 14, 2024",
    status: "partial",
  },
  {
    id: "rev-003",
    user: "Dr. Maria Garcia",
    diagnosis: "Acute Bronchitis",
    overallScore: 5,
    accuracy: 5,
    interpretability: 4,
    comment: "Perfect diagnosis. Interface could be clearer for concept attribution.",
    date: "Jan 13, 2024",
    status: "helpful",
  },
  {
    id: "rev-004",
    user: "Dr. Robert Brown",
    diagnosis: "GERD",
    overallScore: 3,
    accuracy: 3,
    interpretability: 4,
    comment: "Some concepts were off-target. Needs refinement.",
    date: "Jan 12, 2024",
    status: "partial",
  },
  {
    id: "rev-005",
    user: "Dr. Lisa Chen",
    diagnosis: "Acute Sinusitis",
    overallScore: 2,
    accuracy: 2,
    interpretability: 3,
    comment: "Missed the mark on this one. Consider retraining.",
    date: "Jan 11, 2024",
    status: "incorrect",
  },
]

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

export function ReviewsTable() {
  const avgScore = (reviews.reduce((sum, r) => sum + r.overallScore, 0) / reviews.length).toFixed(1)
  const helpfulCount = reviews.filter((r) => r.status === "helpful").length
  const trend = ((helpfulCount / reviews.length) * 100).toFixed(0)

  return (
    <GlassCard className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-semibold text-foreground">User Reviews & Feedback</h3>
          <p className="text-sm text-foreground-muted mt-1">{reviews.length} feedback entries</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/[0.06] border border-white/[0.08]">
          <TrendingUp className="w-4 h-4 text-primary" />
          <span className="text-sm font-semibold text-foreground">{trend}%</span>
          <span className="text-xs text-foreground-muted">helpful</span>
        </div>
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
                Diagnosis
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
            {reviews.map((review) => {
              const colors = statusColors[review.status]
              return (
                <tr key={review.id} className="border-b border-white/[0.06] hover:bg-white/[0.03] transition-colors">
                  <td className="py-3 px-4">
                    <div className="font-medium text-foreground">{review.user}</div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="text-sm text-foreground-muted">{review.diagnosis}</div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex gap-2 items-center">
                      <StarRating score={review.overallScore} />
                      <span className="text-xs font-medium text-foreground ml-1">
                        {review.overallScore}.0
                      </span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${colors.bg} ${colors.text} border ${colors.border}`}
                    >
                      {review.status.charAt(0).toUpperCase() + review.status.slice(1)}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-foreground-muted text-xs">{review.date}</td>
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
          <p className="text-xs text-foreground-muted mb-1">Helpful</p>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-semibold text-primary">{helpfulCount}</span>
            <span className="text-xs text-foreground-muted">/ {reviews.length}</span>
          </div>
        </div>
        <div>
          <p className="text-xs text-foreground-muted mb-1">Accuracy Rate</p>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-semibold text-gold">
              {((reviews.filter((r) => r.status === "helpful").length / reviews.length) * 100).toFixed(0)}%
            </span>
          </div>
        </div>
      </div>
    </GlassCard>
  )
}
