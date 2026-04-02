"use client"

import { useState } from "react"
import { Star, X } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"

interface FeedbackWidgetProps {
  onClose: () => void
}

export function FeedbackWidget({ onClose }: FeedbackWidgetProps) {
  const [overallRating, setOverallRating] = useState(0)
  const [accuracyRating, setAccuracyRating] = useState(0)
  const [interpretabilityRating, setInterpretabilityRating] = useState(0)
  const [comment, setComment] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async () => {
    setIsSubmitting(true)
    await new Promise(resolve => setTimeout(resolve, 1000))
    onClose()
    setIsSubmitting(false)
  }

  const StarRating = ({
    rating,
    onRate,
    label,
  }: {
    rating: number
    onRate: (value: number) => void
    label: string
  }) => (
    <div className="space-y-2">
      <label className="text-sm text-foreground-muted">{label}</label>
      <div className="flex gap-2">
        {[1, 2, 3, 4, 5].map(star => (
          <button
            key={star}
            onClick={() => onRate(star)}
            className={`p-1 rounded transition-colors ${
              star <= rating
                ? "bg-gold/20 text-gold"
                : "bg-white/[0.04] text-foreground-muted hover:bg-white/[0.08]"
            }`}
          >
            <Star className="w-5 h-5 fill-current" />
          </button>
        ))}
      </div>
    </div>
  )

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <GlassCard className="max-w-md w-full space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-foreground">Rate This Prediction</h2>
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-white/[0.08] transition-colors"
          >
            <X className="w-5 h-5 text-foreground-muted" />
          </button>
        </div>

        <div className="space-y-4">
          <StarRating
            rating={overallRating}
            onRate={setOverallRating}
            label="Overall Quality"
          />
          <StarRating
            rating={accuracyRating}
            onRate={setAccuracyRating}
            label="Accuracy"
          />
          <StarRating
            rating={interpretabilityRating}
            onRate={setInterpretabilityRating}
            label="Interpretability"
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm text-foreground-muted">Comments (optional)</label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Share your feedback..."
            className="w-full px-3 py-2 rounded-lg bg-white/[0.04] border border-white/[0.08] text-foreground text-sm focus:outline-none focus:border-primary/50 resize-none placeholder:text-foreground-subtle"
            rows={3}
          />
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 rounded-lg bg-white/[0.06] border border-white/[0.08] text-foreground hover:bg-white/[0.1] transition-colors font-medium"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="flex-1 px-4 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-colors font-medium flex items-center justify-center gap-2"
          >
            {isSubmitting ? (
              <>
                <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                Submitting...
              </>
            ) : (
              "Submit Feedback"
            )}
          </button>
        </div>
      </GlassCard>
    </div>
  )
}
