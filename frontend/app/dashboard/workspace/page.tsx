import { GlassCard } from '@/components/shared/GlassCard'
import { FlaskConical } from 'lucide-react'

export default function WorkspacePage() {
  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <GlassCard className="p-12 flex flex-col items-center justify-center text-center">
        <div
          className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
          style={{ background: 'var(--accent-dim)' }}
        >
          <FlaskConical className="w-7 h-7" style={{ color: 'var(--accent)' }} />
        </div>
        <h2 className="text-lg font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
          Workspace
        </h2>
        <p style={{ color: 'var(--text-secondary)' }} className="text-sm">
          Note input + Phase 1 prediction — coming in Part 2.
        </p>
      </GlassCard>
    </div>
  )
}
