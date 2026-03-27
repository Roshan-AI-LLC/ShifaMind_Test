'use client'

import { useEffect, useState } from 'react'
import { User, Mail, Building2, Stethoscope, Key, Loader2, CheckCircle } from 'lucide-react'
import { createClient } from '@/lib/supabase/client'
import { GlassCard } from '@/components/shared/GlassCard'
import { useToast } from '@/components/shared/Toast'

interface DoctorProfile {
  id: string
  full_name: string
  specialty: string | null
  institution: string | null
  email: string
  role: 'doctor' | 'admin'
  created_at: string
}

interface Stats {
  predictions: number
  chats: number
  reviews: number
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="text-center p-4 rounded-xl" style={{ background: 'var(--glass-bg)', border: '1px solid var(--glass-border)' }}>
      <p className="text-2xl font-semibold mb-1" style={{ color: 'var(--text-primary)' }}>{value}</p>
      <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>{label}</p>
    </div>
  )
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<DoctorProfile | null>(null)
  const [stats, setStats] = useState<Stats>({ predictions: 0, chats: 0, reviews: 0 })
  const [loading, setLoading] = useState(true)
  const [magicLinkSent, setMagicLinkSent] = useState(false)
  const [sendingLink, setSendingLink] = useState(false)
  const { toast } = useToast()
  const supabase = createClient()

  useEffect(() => {
    async function load() {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      const [profileRes, predRes, chatRes, reviewRes] = await Promise.all([
        supabase.from('doctors').select('*').eq('id', user.id).single(),
        supabase.from('predictions').select('id', { count: 'exact', head: true }).eq('doctor_id', user.id),
        supabase.from('chat_sessions').select('id', { count: 'exact', head: true }).eq('doctor_id', user.id),
        supabase.from('reviews').select('id', { count: 'exact', head: true }).eq('doctor_id', user.id),
      ])

      setProfile(profileRes.data as DoctorProfile)
      setStats({
        predictions: predRes.count ?? 0,
        chats: chatRes.count ?? 0,
        reviews: reviewRes.count ?? 0,
      })
      setLoading(false)
    }
    load()
  }, [])

  async function handleMagicLink() {
    if (!profile?.email) return
    setSendingLink(true)
    const { error } = await supabase.auth.signInWithOtp({
      email: profile.email,
      options: { emailRedirectTo: `${window.location.origin}/dashboard` },
    })
    setSendingLink(false)
    if (error) {
      toast(error.message, 'error')
    } else {
      setMagicLinkSent(true)
      toast('Magic link sent to your email', 'success')
    }
  }

  const initials = profile?.full_name
    ?.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() ?? 'DR'

  const memberSince = profile
    ? new Date(profile.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long' })
    : ''

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto space-y-4">
        {[...Array(3)].map((_, i) => <div key={i} className="skeleton h-32 rounded-2xl" />)}
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto space-y-5 animate-fade-in">
      <h1 className="text-xl font-semibold" style={{ color: 'var(--text-primary)' }}>Profile</h1>

      {/* Avatar + name */}
      <GlassCard className="p-6">
        <div className="flex items-center gap-5">
          <div
            className="w-16 h-16 rounded-2xl flex items-center justify-center text-xl font-bold shrink-0"
            style={{ background: 'var(--accent-dim)', border: '1px solid var(--accent-glow)', color: 'var(--accent)' }}
          >
            {initials}
          </div>
          <div>
            <h2 className="text-lg font-semibold" style={{ color: 'var(--text-primary)' }}>
              {profile?.full_name}
            </h2>
            <div className="flex items-center gap-3 mt-1">
              {profile?.role === 'admin' && (
                <span className="text-xs px-2 py-0.5 rounded-lg" style={{ background: 'rgba(255,107,107,0.15)', color: 'var(--accent-warm)' }}>
                  Admin
                </span>
              )}
              <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                Member since {memberSince}
              </span>
            </div>
          </div>
        </div>
      </GlassCard>

      {/* Details */}
      <GlassCard className="p-6">
        <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-secondary)' }}>Details</h3>
        <div className="space-y-3">
          {[
            { icon: Mail, label: 'Email', value: profile?.email },
            { icon: Stethoscope, label: 'Specialty', value: profile?.specialty ?? '—' },
            { icon: Building2, label: 'Institution', value: profile?.institution ?? '—' },
            { icon: User, label: 'Role', value: profile?.role === 'admin' ? 'Administrator' : 'Doctor' },
          ].map(({ icon: Icon, label, value }) => (
            <div key={label} className="flex items-center gap-3">
              <Icon className="w-4 h-4 shrink-0" style={{ color: 'var(--text-muted)' }} />
              <span className="text-xs w-24 shrink-0" style={{ color: 'var(--text-secondary)' }}>{label}</span>
              <span className="text-sm" style={{ color: 'var(--text-primary)' }}>{value}</span>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Stats */}
      <GlassCard className="p-6">
        <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-secondary)' }}>Activity</h3>
        <div className="grid grid-cols-3 gap-3">
          <StatCard label="Predictions" value={stats.predictions} />
          <StatCard label="Chat sessions" value={stats.chats} />
          <StatCard label="Reviews given" value={stats.reviews} />
        </div>
      </GlassCard>

      {/* Security */}
      <GlassCard className="p-6">
        <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-secondary)' }}>Security</h3>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Key className="w-4 h-4" style={{ color: 'var(--text-muted)' }} />
            <div>
              <p className="text-sm" style={{ color: 'var(--text-primary)' }}>Password-less sign in</p>
              <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>
                Send a magic link to your email to sign in without a password
              </p>
            </div>
          </div>
          {magicLinkSent ? (
            <div className="flex items-center gap-1.5 text-sm" style={{ color: 'var(--accent)' }}>
              <CheckCircle className="w-4 h-4" />
              Sent
            </div>
          ) : (
            <button
              onClick={handleMagicLink}
              disabled={sendingLink}
              className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm transition-all disabled:opacity-50"
              style={{
                background: 'var(--glass-bg)',
                border: '1px solid var(--glass-border)',
                color: 'var(--text-secondary)',
              }}
            >
              {sendingLink ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Send magic link'}
            </button>
          )}
        </div>
      </GlassCard>
    </div>
  )
}
