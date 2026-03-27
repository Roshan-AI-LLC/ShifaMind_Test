import { GlassCard } from '@/components/shared/GlassCard'
import { MessageSquare } from 'lucide-react'

export default function ChatPage() {
  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <GlassCard className="p-12 flex flex-col items-center justify-center text-center">
        <div
          className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
          style={{ background: 'rgba(167,139,250,0.15)' }}
        >
          <MessageSquare className="w-7 h-7" style={{ color: '#a78bfa' }} />
        </div>
        <h2 className="text-lg font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>
          Chat
        </h2>
        <p style={{ color: 'var(--text-secondary)' }} className="text-sm">
          Streaming LLM chat grounded in predictions — coming in Part 3.
        </p>
      </GlassCard>
    </div>
  )
}
