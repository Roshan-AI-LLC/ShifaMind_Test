'use client'

import { useState, useEffect } from 'react'
import { ChevronDown, FlaskConical, Loader2, FileText } from 'lucide-react'
import { listNotes } from '@/lib/api'
import { MOCK_NOTES } from '@/lib/mock-data'
import type { SampleNote } from '@/types'
import { cn } from '@/lib/utils'

interface NoteInputProps {
  onSubmit: (text: string) => void
  loading: boolean
}

const CATEGORIES = [
  'Cardiology', 'Pulmonary', 'Infectious Disease',
  'Renal', 'Endocrine', 'GI', 'Neurology', 'Multi-System',
]

function estimateTokens(text: string): number {
  return Math.round(text.split(/\s+/).filter(Boolean).length * 1.3)
}

export function NoteInput({ onSubmit, loading }: NoteInputProps) {
  const [text, setText] = useState('')
  const [sampleNotes, setSampleNotes] = useState<SampleNote[]>([])
  const [selectorOpen, setSelectorOpen] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [loadingNotes, setLoadingNotes] = useState(false)

  const tokenCount = estimateTokens(text)
  const overLimit = tokenCount > 512

  useEffect(() => {
    setLoadingNotes(true)
    listNotes()
      .then(setSampleNotes)
      .catch(() => setSampleNotes(MOCK_NOTES))
      .then(() => setLoadingNotes(false))
  }, [])

  const filteredNotes = selectedCategory
    ? sampleNotes.filter(n => n.category === selectedCategory)
    : sampleNotes

  function handleSelectNote(note: SampleNote) {
    setText(note.text)
    setSelectorOpen(false)
    setSelectedCategory(null)
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!text.trim() || loading) return
    onSubmit(text.trim())
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 h-full">
      {/* Sample note selector */}
      <div className="relative">
        <button
          type="button"
          onClick={() => setSelectorOpen(!selectorOpen)}
          className="w-full flex items-center justify-between gap-2 px-4 py-2.5 rounded-xl text-sm
            transition-colors duration-150"
          style={{
            background: 'var(--glass-bg)',
            border: '1px solid var(--glass-border)',
            color: 'var(--text-secondary)',
          }}
        >
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4 shrink-0" />
            <span>Choose a sample clinical note…</span>
          </div>
          <ChevronDown className={cn('w-4 h-4 shrink-0 transition-transform', selectorOpen && 'rotate-180')} />
        </button>

        {selectorOpen && (
          <div
            className="absolute top-full left-0 right-0 mt-1 rounded-xl z-20 overflow-hidden"
            style={{
              background: '#0d1526',
              border: '1px solid var(--glass-border)',
              boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
            }}
          >
            {/* Category filter */}
            <div className="flex flex-wrap gap-1.5 p-3 border-b border-white/[0.06]">
              <button
                type="button"
                onClick={() => setSelectedCategory(null)}
                className={cn(
                  'px-2.5 py-1 rounded-full text-xs transition-colors',
                  !selectedCategory ? 'bg-[var(--accent-dim)] text-[var(--accent)]' : 'text-white/40 hover:text-white/70'
                )}
              >
                All
              </button>
              {CATEGORIES.map(cat => (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setSelectedCategory(cat)}
                  className={cn(
                    'px-2.5 py-1 rounded-full text-xs transition-colors',
                    selectedCategory === cat ? 'bg-[var(--accent-dim)] text-[var(--accent)]' : 'text-white/40 hover:text-white/70'
                  )}
                >
                  {cat}
                </button>
              ))}
            </div>

            {/* Notes list */}
            <div className="max-h-56 overflow-y-auto">
              {loadingNotes ? (
                <div className="flex items-center justify-center py-6">
                  <Loader2 className="w-4 h-4 animate-spin" style={{ color: 'var(--text-muted)' }} />
                </div>
              ) : filteredNotes.length === 0 ? (
                <p className="text-xs text-center py-4" style={{ color: 'var(--text-muted)' }}>
                  No notes found
                </p>
              ) : (
                filteredNotes.map(note => (
                  <button
                    key={note.id}
                    type="button"
                    onClick={() => handleSelectNote(note)}
                    className="w-full flex items-start gap-3 px-4 py-3 hover:bg-white/[0.04] transition-colors text-left"
                  >
                    <div className="min-w-0">
                      <p className="text-sm font-medium truncate" style={{ color: 'var(--text-primary)' }}>
                        {note.title}
                      </p>
                      <p className="text-xs mt-0.5" style={{ color: 'var(--text-muted)' }}>
                        {note.category} · {note.note_length} chars
                      </p>
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        )}
      </div>

      {/* Textarea */}
      <div className="flex-1 flex flex-col gap-2">
        <label className="text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>
          Clinical note
        </label>
        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Paste or type a clinical note here…&#10;&#10;e.g. 72M presented with progressive dyspnea, orthopnea, and bilateral lower extremity edema..."
          className="flex-1 min-h-[320px] w-full p-4 rounded-xl text-sm font-mono resize-none outline-none transition-all leading-relaxed"
          style={{
            background: 'var(--glass-bg)',
            border: `1px solid ${overLimit ? 'rgba(255,107,107,0.5)' : 'var(--glass-border)'}`,
            color: 'var(--text-primary)',
          }}
          onFocus={e => {
            if (!overLimit) {
              e.target.style.borderColor = 'rgba(78, 205, 196, 0.5)'
              e.target.style.boxShadow = '0 0 0 1px rgba(78, 205, 196, 0.2)'
            }
          }}
          onBlur={e => {
            e.target.style.borderColor = overLimit ? 'rgba(255,107,107,0.5)' : 'var(--glass-border)'
            e.target.style.boxShadow = 'none'
          }}
        />
        {/* Token count */}
        <div className="flex items-center justify-between">
          <span className="text-xs" style={{ color: overLimit ? 'var(--accent-warm)' : 'var(--text-muted)' }}>
            ~{tokenCount} tokens{overLimit ? ' — note will be truncated to 512 tokens' : ''}
          </span>
          {text && (
            <button
              type="button"
              onClick={() => setText('')}
              className="text-xs transition-colors"
              style={{ color: 'var(--text-muted)' }}
              onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent-warm)')}
              onMouseLeave={e => (e.currentTarget.style.color = 'var(--text-muted)')}
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={!text.trim() || loading}
        className="flex items-center justify-center gap-2 py-3 rounded-xl font-medium text-sm
          transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed
          hover:brightness-110 hover:shadow-[0_0_20px_rgba(78,205,196,0.3)] active:scale-[0.98]"
        style={{
          background: '#4ecdc4',
          color: '#060a13',
          boxShadow: '0 4px 20px rgba(78, 205, 196, 0.25)',
        }}
      >
        {loading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Analyzing…
          </>
        ) : (
          <>
            <FlaskConical className="w-4 h-4" />
            Analyze with ShifaMind
          </>
        )}
      </button>
    </form>
  )
}
