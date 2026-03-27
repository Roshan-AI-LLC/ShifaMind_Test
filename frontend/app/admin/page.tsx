import { GlassCard } from '@/components/shared/GlassCard'
import { Shield } from 'lucide-react'

export default function AdminPage() {
  return (
    <div
      className="min-h-screen ml-16 pt-16 p-6"
      style={{ background: 'var(--bg-deep)' }}
    >
      <div className="max-w-5xl mx-auto animate-fade-in">
        <GlassCard className="p-12 flex flex-col items-center justify-center text-center">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
            style={{ background: 'rgba(255, 107, 107, 0.1)' }}
          >
            <Shield className="w-7 h-7" style={{ color: 'var(--accent-warm)' }} />
          </div>
          <h2 className="text-lg font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
            Admin Dashboard
          </h2>
          <p style={{ color: 'var(--text-secondary)' }} className="text-sm">
            Usage stats, reviews, doctor management — coming in Part 4.
          </p>
        </GlassCard>
      </div>
    </div>
  )
}
