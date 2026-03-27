import { GlassCard } from '@/components/shared/GlassCard'
import { User } from 'lucide-react'

export default function ProfilePage() {
  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      <GlassCard className="p-12 flex flex-col items-center justify-center text-center">
        <div
          className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
          style={{ background: 'var(--glass-bg)' }}
        >
          <User className="w-7 h-7" style={{ color: 'var(--text-secondary)' }} />
        </div>
        <h2 className="text-lg font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
          Profile
        </h2>
        <p style={{ color: 'var(--text-secondary)' }} className="text-sm">
          Doctor profile and settings — coming in Part 4.
        </p>
      </GlassCard>
    </div>
  )
}
