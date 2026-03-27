import { GlassCard } from '@/components/shared/GlassCard'
import { History } from 'lucide-react'

export default function HistoryPage() {
  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <GlassCard className="p-12 flex flex-col items-center justify-center text-center">
        <div
          className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
          style={{ background: 'rgba(255, 217, 61, 0.15)' }}
        >
          <History className="w-7 h-7" style={{ color: 'var(--accent-gold)' }} />
        </div>
        <h2 className="text-lg font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
          History
        </h2>
        <p style={{ color: 'var(--text-secondary)' }} className="text-sm">
          Past predictions and chat sessions — coming in Part 4.
        </p>
      </GlassCard>
    </div>
  )
}
