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
            background: 'var(--text-muted)',
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
    <div className={cn('flex', isUser ? 'justify-end' : 'justify-start')}>
      <div
        className={cn(
          'max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed',
          isUser
            ? 'rounded-tr-sm'
            : 'rounded-tl-sm'
        )}
        style={
          isUser
            ? {
                background: 'rgba(78, 205, 196, 0.12)',
                border: '1px solid rgba(78, 205, 196, 0.2)',
                color: 'var(--text-primary)',
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
