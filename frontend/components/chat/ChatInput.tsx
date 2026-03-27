'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ChatInputProps {
  onSend: (message: string) => void
  disabled?: boolean
  placeholder?: string
}

export function ChatInput({ onSend, disabled = false, placeholder }: ChatInputProps) {
  const [value, setValue] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 200) + 'px'
  }, [value])

  function handleSubmit() {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setValue('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div
      className="flex items-end gap-3 p-3 rounded-2xl"
      style={{
        background: 'var(--glass-bg)',
        border: '1px solid var(--glass-border)',
      }}
    >
      <textarea
        ref={textareaRef}
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        rows={1}
        placeholder={placeholder ?? 'Ask about the predictions… (Enter to send, Shift+Enter for newline)'}
        className="flex-1 bg-transparent resize-none outline-none text-sm leading-relaxed"
        style={{
          color: 'var(--text-primary)',
          minHeight: '24px',
          maxHeight: '200px',
        }}
      />
      <button
        type="button"
        onClick={handleSubmit}
        disabled={!value.trim() || disabled}
        className={cn(
          'shrink-0 w-9 h-9 rounded-xl flex items-center justify-center transition-all',
          value.trim() && !disabled
            ? 'bg-[#4ecdc4] text-[#060a13] hover:bg-[#3dbdb5] shadow-lg shadow-[#4ecdc4]/20'
            : 'bg-white/[0.06] text-white/30 cursor-not-allowed'
        )}
      >
        {disabled
          ? <Loader2 className="w-4 h-4 animate-spin" />
          : <Send className="w-4 h-4" />
        }
      </button>
    </div>
  )
}
