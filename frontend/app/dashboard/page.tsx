import { createClient } from '@/lib/supabase/server'
import { GlassCard } from '@/components/shared/GlassCard'
import { FlaskConical, MessageSquare, History, TrendingUp, Brain } from 'lucide-react'
import Link from 'next/link'

export default async function DashboardPage() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  const { data: doctor } = await supabase
    .from('doctors')
    .select('full_name, specialty')
    .eq('id', user!.id)
    .single()

  const { count: predictionCount } = await supabase
    .from('predictions')
    .select('*', { count: 'exact', head: true })
    .eq('doctor_id', user!.id)

  const { count: chatCount } = await supabase
    .from('chat_sessions')
    .select('*', { count: 'exact', head: true })
    .eq('doctor_id', user!.id)

  const lastName = doctor?.full_name?.split(' ').pop()

  const QUICK_ACTIONS = [
    {
      href: '/dashboard/workspace',
      icon: FlaskConical,
      label: 'New Prediction',
      description: 'Analyze a clinical note with Phase 1 AI',
      color: 'var(--accent)',
    },
    {
      href: '/dashboard/chat',
      icon: MessageSquare,
      label: 'Chat',
      description: 'Discuss predictions with the clinical assistant',
      color: '#a78bfa',
    },
    {
      href: '/dashboard/history',
      icon: History,
      label: 'History',
      description: 'Review past predictions and conversations',
      color: 'var(--accent-gold)',
    },
  ]

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in">
      {/* Welcome */}
      <div>
        <h1 className="text-xl sm:text-2xl font-semibold mb-1" style={{ color: 'var(--text-primary)' }}>
          Welcome back{lastName ? `, Dr. ${lastName}` : ''}
        </h1>
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          ShifaMind Platform — Interpretable Clinical Decision Support
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <GlassCard className="p-6">
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
              style={{ background: 'var(--accent-dim)' }}
            >
              <TrendingUp className="w-5 h-5" style={{ color: 'var(--accent)' }} />
            </div>
            <div>
              <p className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
                {predictionCount ?? 0}
              </p>
              <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>Predictions run</p>
            </div>
          </div>
        </GlassCard>
        <GlassCard className="p-6">
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
              style={{ background: 'rgba(167,139,250,0.15)' }}
            >
              <MessageSquare className="w-5 h-5" style={{ color: '#a78bfa' }} />
            </div>
            <div>
              <p className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
                {chatCount ?? 0}
              </p>
              <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>Chat sessions</p>
            </div>
          </div>
        </GlassCard>
      </div>

      {/* Quick actions */}
      <div>
        <h2 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-secondary)' }}>
          Quick actions
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {QUICK_ACTIONS.map(({ href, icon: Icon, label, description, color }, i) => (
            <Link
              key={href}
              href={href}
              className="animate-fade-in"
              style={{ animationDelay: `${i * 60}ms`, animationFillMode: 'backwards' }}
            >
              <GlassCard hover className="p-6 h-full">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center mb-3"
                  style={{ background: `${color}20` }}
                >
                  <Icon className="w-5 h-5" style={{ color }} />
                </div>
                <p className="font-medium text-sm mb-1" style={{ color: 'var(--text-primary)' }}>
                  {label}
                </p>
                <p className="text-xs leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
                  {description}
                </p>
              </GlassCard>
            </Link>
          ))}
        </div>
      </div>

      {/* First-time welcome banner */}
      {(predictionCount ?? 0) === 0 && (chatCount ?? 0) === 0 && (
        <GlassCard className="p-6 border-l-2 border-l-[#4ecdc4]">
          <p className="text-sm font-medium mb-1" style={{ color: 'var(--text-primary)' }}>
            Welcome to ShifaMind Platform
          </p>
          <p className="text-xs mb-3 leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
            Start by analyzing a clinical note in the Workspace. ShifaMind will predict ICD-10 diagnoses
            and show you exactly which clinical concepts drove each prediction.
          </p>
          <Link
            href="/dashboard/workspace"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all
              hover:brightness-110 hover:shadow-[0_0_20px_rgba(78,205,196,0.3)] active:scale-[0.98]"
            style={{ background: '#4ecdc4', color: '#060a13' }}
          >
            Open Workspace →
          </Link>
        </GlassCard>
      )}

      {/* System status */}
      <GlassCard className="p-6">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div className="flex items-center gap-3">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
              style={{ background: 'var(--accent-dim)' }}
            >
              <Brain className="w-4 h-4" style={{ color: 'var(--accent)' }} />
            </div>
            <div>
              <p className="text-xs font-medium mb-0.5" style={{ color: 'var(--text-secondary)' }}>
                System Status
              </p>
              <p className="text-sm" style={{ color: 'var(--text-primary)' }}>
                Phase 1 · BioClinicalBERT · 111 Concepts · 50 ICD-10 Codes
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full animate-pulse" style={{ background: 'var(--accent)' }} />
            <span className="text-xs" style={{ color: 'var(--accent)' }}>Ready</span>
          </div>
        </div>
      </GlassCard>
    </div>
  )
}
