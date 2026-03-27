import { createClient } from '@/lib/supabase/server'
import { GlassCard } from '@/components/shared/GlassCard'
import { FlaskConical, MessageSquare, History, TrendingUp } from 'lucide-react'
import Link from 'next/link'

export default async function DashboardPage() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  const { data: doctor } = await supabase
    .from('doctors')
    .select('full_name, specialty')
    .eq('id', user!.id)
    .single()

  // Stats
  const { count: predictionCount } = await supabase
    .from('predictions')
    .select('*', { count: 'exact', head: true })
    .eq('doctor_id', user!.id)

  const { count: chatCount } = await supabase
    .from('chat_sessions')
    .select('*', { count: 'exact', head: true })
    .eq('doctor_id', user!.id)

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
        <h1 className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
          Welcome back{doctor?.full_name ? `, ${doctor.full_name.split(' ')[0]}` : ''}
        </h1>
        {doctor?.specialty && (
          <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>
            {doctor.specialty}
          </p>
        )}
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <GlassCard className="p-5">
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center"
              style={{ background: 'var(--accent-dim)' }}
            >
              <TrendingUp className="w-5 h-5" style={{ color: 'var(--accent)' }} />
            </div>
            <div>
              <p className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
                {predictionCount ?? 0}
              </p>
              <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>Predictions</p>
            </div>
          </div>
        </GlassCard>
        <GlassCard className="p-5">
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center"
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
        <h2 className="text-sm font-medium mb-3" style={{ color: 'var(--text-secondary)' }}>
          Quick actions
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {QUICK_ACTIONS.map(({ href, icon: Icon, label, description, color }) => (
            <Link key={href} href={href}>
              <GlassCard hover className="p-5 h-full">
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
    </div>
  )
}
