import { Brain } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { ChatMessageLocal } from '@/hooks/useChat'

interface ChatMessageProps {
  message: ChatMessageLocal
}

function TypingIndicator() {
  return (
    <div className="flex gap-1 items-center h-5 px-1">
      {[0, 1, 2].map(i => (
        <div
          key={i}
          className="w-1.5 h-1.5 rounded-full"
          style={{
            background: 'var(--accent)',
            animation: `pulse-dot 1.4s ease-in-out ${i * 0.16}s infinite`,
          }}
        />
      ))}
    </div>
  )
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={cn('flex items-end gap-2', isUser ? 'justify-end' : 'justify-start')}>
      {/* Assistant avatar */}
      {!isUser && (
        <div
          className="w-6 h-6 rounded-lg flex items-center justify-center shrink-0 mb-0.5"
          style={{
            background: 'var(--accent-dim)',
            border: '1px solid var(--accent-glow)',
          }}
        >
          <Brain className="w-3.5 h-3.5" style={{ color: 'var(--accent)' }} />
        </div>
      )}

      <div
        className={cn(
          'max-w-[80%] sm:max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed',
          isUser ? 'rounded-tr-sm' : 'rounded-bl-sm'
        )}
        style={
          isUser
            ? {
                background: 'rgba(78, 205, 196, 0.12)',
                border: '1px solid rgba(78, 205, 196, 0.2)',
                color: 'var(--text-primary)',
                boxShadow: '0 2px 12px rgba(78, 205, 196, 0.15)',
              }
            : {
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid var(--glass-border)',
                color: 'var(--text-primary)',
              }
        }
      >
        {message.streaming && !message.content ? (
          <TypingIndicator />
        ) : (
          <div className="whitespace-pre-wrap">
            {message.content}
            {message.streaming && (
              <span
                className="inline-block w-0.5 h-4 ml-0.5 align-text-bottom animate-pulse"
                style={{ background: 'var(--accent)' }}
              />
            )}
          </div>
        )}
      </div>
    </div>
  )
}
