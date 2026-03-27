'use client'

import { useState } from 'react'
import { Star, X, Loader2, CheckCircle } from 'lucide-react'
import { submitReview } from '@/lib/api'
import { useToast } from '@/components/shared/Toast'
import { cn } from '@/lib/utils'

interface FeedbackWidgetProps {
  predictionId: string
  onClose: () => void
}

function StarRating({
  value,
  onChange,
  label,
}: {
  value: number
  onChange: (v: number) => void
  label: string
}) {
  const [hover, setHover] = useState(0)
  return (
    <div>
      <p className="text-xs mb-1.5" style={{ color: 'var(--text-secondary)' }}>
        {label}
      </p>
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map(star => (
          <button
            key={star}
            type="button"
            onClick={() => onChange(star)}
            onMouseEnter={() => setHover(star)}
            onMouseLeave={() => setHover(0)}
          >
            <Star
              className="w-5 h-5 transition-colors"
              style={{
                color: star <= (hover || value) ? 'var(--accent-gold)' : 'var(--text-muted)',
                fill: star <= (hover || value) ? 'var(--accent-gold)' : 'transparent',
              }}
            />
          </button>
        ))}
      </div>
    </div>
  )
}

export function FeedbackWidget({ predictionId, onClose }: FeedbackWidgetProps) {
  const [rating, setRating] = useState(0)
  const [accuracyRating, setAccuracyRating] = useState(0)
  const [interpretabilityRating, setInterpretabilityRating] = useState(0)
  const [comment, setComment] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { toast } = useToast()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (rating === 0) { setError('Please select an overall rating.'); return }
    setLoading(true)
    setError(null)
    try {
      await submitReview({
        prediction_id: predictionId,
        rating,
        accuracy_rating: accuracyRating || undefined,
        interpretability_rating: interpretabilityRating || undefined,
        comment: comment.trim() || undefined,
      })
      setSuccess(true)
      toast('Review submitted — thank you!', 'success')
      setTimeout(onClose, 1800)
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to submit review'
      setError(msg)
      toast(msg, 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: 'rgba(6,10,19,0.8)', backdropFilter: 'blur(8px)' }}
    >
      <div
        className="w-full max-w-md rounded-2xl p-6 animate-fade-in"
        style={{ background: '#0d1526', border: '1px solid var(--glass-border)' }}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-5">
          <h3 className="font-semibold" style={{ color: 'var(--text-primary)' }}>
            Rate this prediction
          </h3>
          <button
            type="button"
            onClick={onClose}
            className="w-7 h-7 rounded-xl flex items-center justify-center hover:bg-white/[0.06] transition-colors"
          >
            <X className="w-4 h-4" style={{ color: 'var(--text-muted)' }} />
          </button>
        </div>

        {success ? (
          <div className="flex flex-col items-center py-6 gap-3">
            <CheckCircle className="w-10 h-10" style={{ color: 'var(--accent)' }} />
            <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
              Thank you for your feedback!
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <StarRating value={rating} onChange={setRating} label="Overall quality *" />
            <StarRating value={accuracyRating} onChange={setAccuracyRating} label="Diagnostic accuracy" />
            <StarRating value={interpretabilityRating} onChange={setInterpretabilityRating} label="Concept interpretability" />

            <div>
              <label className="block text-xs mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                Comments (optional)
              </label>
              <textarea
                value={comment}
                onChange={e => setComment(e.target.value)}
                rows={3}
                placeholder="What did you think of the predictions? Any corrections?"
                className="w-full px-3 py-2.5 rounded-xl text-sm resize-none outline-none transition-all"
                style={{
                  background: 'var(--glass-bg)',
                  border: '1px solid var(--glass-border)',
                  color: 'var(--text-primary)',
                }}
                onFocus={e => {
                  e.target.style.borderColor = 'rgba(78,205,196,0.4)'
                }}
                onBlur={e => {
                  e.target.style.borderColor = 'var(--glass-border)'
                }}
              />
            </div>

            {error && (
              <p className="text-xs" style={{ color: 'var(--accent-warm)' }}>{error}</p>
            )}

            <div className="flex gap-3 pt-1">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 py-2.5 rounded-xl text-sm transition-colors"
                style={{
                  background: 'var(--glass-bg)',
                  border: '1px solid var(--glass-border)',
                  color: 'var(--text-secondary)',
                }}
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium transition-all disabled:opacity-50
                  hover:brightness-110 active:scale-[0.98]"
                style={{ background: '#4ecdc4', color: '#060a13' }}
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Submit review'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
