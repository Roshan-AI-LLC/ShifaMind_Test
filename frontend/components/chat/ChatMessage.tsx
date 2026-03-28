import { Brain } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { ChatMessageLocal } from '@/hooks/useChat'
import ReactMarkdown from 'react-markdown'

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
    <div className={cn(
      'flex items-end gap-2',
      isUser ? 'justify-end animate-slide-right' : 'justify-start animate-slide-left'
    )}>
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
        ) : isUser ? (
          <div className="whitespace-pre-wrap">
            {message.content}
          </div>
        ) : (
          <div className="prose prose-invert prose-sm max-w-none
            prose-headings:text-[var(--text-primary)] prose-headings:font-semibold prose-headings:mt-3 prose-headings:mb-1
            prose-h3:text-sm prose-h2:text-sm
            prose-p:text-[var(--text-primary)] prose-p:my-1 prose-p:leading-relaxed
            prose-strong:text-[var(--accent)] prose-strong:font-semibold
            prose-em:text-[var(--text-secondary)]
            prose-ul:my-1 prose-ol:my-1 prose-li:my-0.5
            prose-li:text-[var(--text-primary)]
            prose-code:text-[var(--accent)] prose-code:bg-white/5 prose-code:px-1 prose-code:rounded
            prose-hr:border-white/10">
            <ReactMarkdown>{message.content}</ReactMarkdown>
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
