'use client'

import { useEffect, useState } from 'react'
import {
  Shield, TrendingUp, MessageSquare, Star, Users,
  FlaskConical, ChevronLeft, ChevronRight
} from 'lucide-react'
import { GlassCard } from '@/components/shared/GlassCard'
import { ConfidenceBar } from '@/components/shared/ConfidenceBar'
import { healthCheck } from '@/lib/api'

interface Stats {
  total_predictions: number
  total_chat_sessions: number
  total_reviews: number
  active_doctors: number
  avg_rating: number | null
  top_icd10_codes: Array<{ code: string; count: number }>
}

interface Review {
  id: string
  rating: number
  accuracy_rating: number | null
  interpretability_rating: number | null
  comment: string | null
  created_at: string
  doctor: { full_name: string; email: string; specialty: string | null } | null
  prediction: { id: string; input_text: string } | null
}

interface ReviewsPage {
  reviews: Review[]
  total: number
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? ''
const PAGE_SIZE = 20

async function fetchWithAuth(path: string) {
  const { createClient } = await import('@/lib/supabase/client')
  const sb = createClient()
  const { data: { session } } = await sb.auth.getSession()
  const res = await fetch(`${API_URL}${path}`, {
    headers: { Authorization: `Bearer ${session?.access_token}` },
  })
  if (!res.ok) throw new Error(`${res.status}`)
  return res.json()
}

function StatTile({ icon: Icon, label, value, color }: {
  icon: React.ElementType; label: string; value: string | number; color: string
}) {
  return (
    <GlassCard className="p-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
          style={{ background: `${color}20` }}>
          <Icon className="w-5 h-5" style={{ color }} />
        </div>
        <div>
          <p className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>{value}</p>
          <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>{label}</p>
        </div>
      </div>
    </GlassCard>
  )
}

function StarDisplay({ rating }: { rating: number | null }) {
  if (!rating) return <span style={{ color: 'var(--text-muted)' }}>—</span>
  return (
    <div className="flex items-center gap-1">
      {[1, 2, 3, 4, 5].map(s => (
        <div key={s} className="w-2.5 h-2.5 rounded-sm" style={{
          background: s <= rating ? 'var(--accent-gold)' : 'var(--glass-bg)',
        }} />
      ))}
      <span className="text-xs ml-1 font-mono" style={{ color: 'var(--text-secondary)' }}>{rating}/5</span>
    </div>
  )
}

export default function AdminPage() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [reviews, setReviews] = useState<ReviewsPage | null>(null)
  const [page, setPage] = useState(0)
  const [loadingStats, setLoadingStats] = useState(true)
  const [loadingReviews, setLoadingReviews] = useState(true)
  const [apiHealth, setApiHealth] = useState<{ status: string; model_loaded: boolean } | null>(null)

  useEffect(() => {
    fetchWithAuth('/api/admin/stats')
      .then(setStats)
      .catch(() => {})
      .then(() => setLoadingStats(false))

    healthCheck()
      .then(setApiHealth)
      .catch(() => {})
  }, [])

  useEffect(() => {
    setLoadingReviews(true)
    fetchWithAuth(`/api/admin/reviews?limit=${PAGE_SIZE}&offset=${page * PAGE_SIZE}`)
      .then(setReviews)
      .catch(() => {})
      .then(() => setLoadingReviews(false))
  }, [page])

  const totalPages = reviews ? Math.ceil(reviews.total / PAGE_SIZE) : 0

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-fade-in">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl flex items-center justify-center"
              style={{ background: 'rgba(255,107,107,0.1)' }}>
              <Shield className="w-5 h-5" style={{ color: 'var(--accent-warm)' }} />
            </div>
            <div>
              <h1 className="text-xl font-semibold" style={{ color: 'var(--text-primary)' }}>Admin Dashboard</h1>
              <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>Platform usage and feedback</p>
            </div>
          </div>
          {/* API health badge */}
          {apiHealth && (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs"
              style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)' }}>
              <div className="w-1.5 h-1.5 rounded-full"
                style={{ background: apiHealth.status === 'ok' ? 'var(--accent)' : 'var(--accent-warm)' }} />
              <span style={{ color: 'var(--text-secondary)' }}>API {apiHealth.status}</span>
              <span style={{ color: 'var(--text-muted)' }}>·</span>
              <span style={{ color: apiHealth.model_loaded ? 'var(--accent)' : 'var(--accent-warm)' }}>
                Model {apiHealth.model_loaded ? 'loaded' : 'not loaded'}
              </span>
            </div>
          )}
        </div>

        {/* Stats grid */}
        {loadingStats ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => <div key={i} className="skeleton h-20 rounded-2xl" />)}
          </div>
        ) : stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatTile icon={FlaskConical} label="Total predictions" value={stats.total_predictions} color="var(--accent)" />
            <StatTile icon={MessageSquare} label="Chat sessions" value={stats.total_chat_sessions} color="#a78bfa" />
            <StatTile icon={Star} label="Reviews" value={stats.total_reviews} color="var(--accent-gold)" />
            <StatTile icon={Users} label="Active doctors" value={stats.active_doctors} color="var(--accent-warm)" />
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Avg rating */}
          {stats && (
            <GlassCard className="p-6">
              <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-secondary)' }}>
                Average rating
              </h3>
              {stats.avg_rating ? (
                <div className="flex items-center gap-4">
                  <p className="text-4xl font-bold" style={{ color: 'var(--accent-gold)' }}>
                    {stats.avg_rating.toFixed(1)}
                  </p>
                  <div className="flex-1">
                    <ConfidenceBar value={stats.avg_rating / 5} />
                    <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>
                      out of 5.0 · {stats.total_reviews} reviews
                    </p>
                  </div>
                </div>
              ) : (
                <p className="text-sm" style={{ color: 'var(--text-muted)' }}>No reviews yet</p>
              )}
            </GlassCard>
          )}

          {/* Top ICD-10 codes */}
          {stats && stats.top_icd10_codes.length > 0 && (
            <GlassCard className="p-6">
              <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-secondary)' }}>
                Top predicted codes
              </h3>
              <div className="space-y-2">
                {stats.top_icd10_codes.slice(0, 6).map((item, i) => (
                  <div key={item.code} className="flex items-center gap-3">
                    <span className="text-xs w-4 text-right shrink-0" style={{ color: 'var(--text-muted)' }}>{i + 1}</span>
                    <span className="font-mono text-xs w-16 shrink-0" style={{ color: 'var(--accent)' }}>{item.code}</span>
                    <div className="flex-1">
                      <ConfidenceBar
                        value={item.count / (stats.top_icd10_codes[0]?.count || 1)}
                        showLabel={false}
                      />
                    </div>
                    <span className="text-xs font-mono w-8 text-right shrink-0" style={{ color: 'var(--text-muted)' }}>
                      {item.count}
                    </span>
                  </div>
                ))}
              </div>
            </GlassCard>
          )}
        </div>

        {/* Reviews table */}
        <GlassCard className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold" style={{ color: 'var(--text-secondary)' }}>
              All reviews {reviews && <span style={{ color: 'var(--text-muted)' }}>({reviews.total})</span>}
            </h3>
            {totalPages > 1 && (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setPage(p => Math.max(0, p - 1))}
                  disabled={page === 0}
                  className="w-7 h-7 rounded-xl flex items-center justify-center transition-colors disabled:opacity-30"
                  style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)' }}
                >
                  <ChevronLeft className="w-3.5 h-3.5" style={{ color: 'var(--text-secondary)' }} />
                </button>
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
                  {page + 1} / {totalPages}
                </span>
                <button
                  onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
                  disabled={page >= totalPages - 1}
                  className="w-7 h-7 rounded-xl flex items-center justify-center transition-colors disabled:opacity-30"
                  style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)' }}
                >
                  <ChevronRight className="w-3.5 h-3.5" style={{ color: 'var(--text-secondary)' }} />
                </button>
              </div>
            )}
          </div>

          {loadingReviews ? (
            <div className="space-y-2">
              {[...Array(5)].map((_, i) => <div key={i} className="skeleton h-14 rounded-xl" />)}
            </div>
          ) : !reviews?.reviews.length ? (
            <p className="text-sm text-center py-8" style={{ color: 'var(--text-muted)' }}>
              No reviews submitted yet
            </p>
          ) : (
            <div className="overflow-x-auto -mx-2 sm:mx-0">
            <div className="min-w-[600px] px-2 sm:px-0 space-y-2">
              {reviews.reviews.map(r => (
                <div key={r.id}
                  className="flex items-start gap-4 px-4 py-3 rounded-xl"
                  style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)' }}
                >
                  {/* Doctor */}
                  <div className="min-w-0 w-44 shrink-0">
                    <p className="text-sm font-medium truncate" style={{ color: 'var(--text-primary)' }}>
                      {r.doctor?.full_name ?? '—'}
                    </p>
                    <p className="text-xs truncate" style={{ color: 'var(--text-muted)' }}>
                      {r.doctor?.specialty ?? r.doctor?.email ?? ''}
                    </p>
                  </div>
                  {/* Ratings */}
                  <div className="shrink-0">
                    <StarDisplay rating={r.rating} />
                  </div>
                  {/* Comment */}
                  <div className="flex-1 min-w-0">
                    {r.comment ? (
                      <p className="text-xs leading-relaxed line-clamp-2" style={{ color: 'var(--text-secondary)' }}>
                        {r.comment}
                      </p>
                    ) : (
                      <p className="text-xs" style={{ color: 'var(--text-muted)' }}>No comment</p>
                    )}
                  </div>
                  {/* Date */}
                  <div className="shrink-0 text-right">
                    <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                      {new Date(r.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
            </div>
          )}
        </GlassCard>
    </div>
  )
}
