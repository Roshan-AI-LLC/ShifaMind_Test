'use client'

import { createContext, useContext, useState, useCallback, useRef } from 'react'
import { CheckCircle, XCircle, AlertCircle, X } from 'lucide-react'
import { cn } from '@/lib/utils'

type ToastType = 'success' | 'error' | 'info'

interface Toast {
  id: string
  type: ToastType
  message: string
}

interface ToastContextValue {
  toast: (message: string, type?: ToastType) => void
}

const ToastContext = createContext<ToastContextValue>({ toast: () => {} })

export function useToast() {
  return useContext(ToastContext)
}

const ICONS = {
  success: CheckCircle,
  error: XCircle,
  info: AlertCircle,
}

const COLORS = {
  success: { bg: 'rgba(78,205,196,0.12)', border: 'rgba(78,205,196,0.3)', color: '#4ecdc4' },
  error:   { bg: 'rgba(255,107,107,0.12)', border: 'rgba(255,107,107,0.3)', color: '#ff6b6b' },
  info:    { bg: 'rgba(255,255,255,0.06)', border: 'rgba(255,255,255,0.12)', color: 'rgba(255,255,255,0.7)' },
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])
  const timers = useRef<Record<string, ReturnType<typeof setTimeout>>>({})

  const dismiss = useCallback((id: string) => {
    clearTimeout(timers.current[id])
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  const toast = useCallback((message: string, type: ToastType = 'info') => {
    const id = crypto.randomUUID()
    setToasts(prev => [...prev, { id, type, message }])
    timers.current[id] = setTimeout(() => dismiss(id), 4000)
  }, [dismiss])

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      {/* Toast container */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-2 pointer-events-none">
        {toasts.map(t => {
          const Icon = ICONS[t.type]
          const style = COLORS[t.type]
          return (
            <div
              key={t.id}
              className="flex items-start gap-3 px-4 py-3 rounded-xl text-sm shadow-xl animate-fade-in pointer-events-auto max-w-sm"
              style={{
                background: style.bg,
                border: `1px solid ${style.border}`,
                backdropFilter: 'blur(20px)',
              }}
            >
              <Icon className="w-4 h-4 mt-0.5 shrink-0" style={{ color: style.color }} />
              <span style={{ color: 'var(--text-primary)' }} className="flex-1">{t.message}</span>
              <button
                onClick={() => dismiss(t.id)}
                className="shrink-0 ml-1 opacity-50 hover:opacity-100 transition-opacity"
              >
                <X className="w-3.5 h-3.5" style={{ color: 'var(--text-primary)' }} />
              </button>
            </div>
          )
        })}
      </div>
    </ToastContext.Provider>
  )
}
