'use client'

import { useEffect, useRef } from 'react'
import { Brain } from 'lucide-react'
import { ChatMessage } from './ChatMessage'
import type { ChatMessageLocal } from '@/hooks/useChat'

interface ChatPanelProps {
  messages: ChatMessageLocal[]
  streaming: boolean
  onSuggestionClick?: (text: string) => void
}

const SUGGESTIONS = [
  'Why was heart failure predicted?',
  'What are the key activated concepts?',
  'What additional workup would you recommend?',
]

export function ChatPanel({ messages, streaming, onSuggestionClick }: ChatPanelProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, streaming])

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center gap-4 px-8 text-center">
        <div
          className="w-12 h-12 rounded-2xl flex items-center justify-center"
          style={{ background: 'var(--accent-dim)' }}
        >
          <Brain className="w-6 h-6" style={{ color: 'var(--accent)' }} />
        </div>
        <div>
          <p className="font-medium text-sm mb-1" style={{ color: 'var(--text-primary)' }}>
            ShifaMind Clinical Assistant
          </p>
          <p className="text-xs leading-relaxed max-w-xs" style={{ color: 'var(--text-secondary)' }}>
            Ask me to explain the predictions, discuss differentials, or suggest next steps based on the clinical context.
          </p>
        </div>
        <div className="flex flex-col gap-2 w-full max-w-sm mt-2">
          {SUGGESTIONS.map(suggestion => (
            <button
              key={suggestion}
              onClick={() => onSuggestionClick?.(suggestion)}
              className="px-3 py-2 rounded-xl text-xs text-left transition-colors"
              style={{
                background: 'var(--glass-bg)',
                border: '1px solid var(--glass-border)',
                color: 'var(--text-secondary)',
                cursor: onSuggestionClick ? 'pointer' : 'default',
              }}
              onMouseEnter={e => {
                if (onSuggestionClick) {
                  e.currentTarget.style.background = 'var(--glass-hover)'
                  e.currentTarget.style.color = 'var(--text-primary)'
                }
              }}
              onMouseLeave={e => {
                e.currentTarget.style.background = 'var(--glass-bg)'
                e.currentTarget.style.color = 'var(--text-secondary)'
              }}
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
      {messages.map(msg => (
        <ChatMessage key={msg.id} message={msg} />
      ))}
      <div ref={bottomRef} />
    </div>
  )
}
