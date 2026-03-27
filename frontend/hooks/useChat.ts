'use client'

import { useState, useCallback, useRef } from 'react'
import { getAuthToken } from '@/lib/api'

export interface ChatMessageLocal {
  id: string
  role: 'user' | 'assistant'
  content: string
  streaming?: boolean
}

interface UseChatOptions {
  predictionId?: string | null
  initialSessionId?: string | null
}

interface UseChatState {
  messages: ChatMessageLocal[]
  sessionId: string | null
  streaming: boolean
  error: string | null
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? ''

export function useChat({ predictionId, initialSessionId }: UseChatOptions = {}) {
  const [state, setState] = useState<UseChatState>({
    messages: [],
    sessionId: initialSessionId ?? null,
    streaming: false,
    error: null,
  })

  const abortRef = useRef<AbortController | null>(null)

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || state.streaming) return

    // Abort any ongoing stream
    abortRef.current?.abort()
    const controller = new AbortController()
    abortRef.current = controller

    const userMsg: ChatMessageLocal = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
    }
    const assistantMsg: ChatMessageLocal = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: '',
      streaming: true,
    }

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMsg, assistantMsg],
      streaming: true,
      error: null,
    }))

    try {
      const token = await getAuthToken()

      const res = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: content,
          prediction_id: predictionId ?? null,
          session_id: state.sessionId,
          stream: true,
        }),
        signal: controller.signal,
      })

      if (!res.ok || !res.body) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body?.detail ?? `Server error ${res.status}`)
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const raw = line.slice(6).trim()
          if (!raw) continue

          try {
            const event = JSON.parse(raw)

            if (event.type === 'token') {
              setState(prev => ({
                ...prev,
                messages: prev.messages.map(m =>
                  m.id === assistantMsg.id
                    ? { ...m, content: m.content + event.content }
                    : m
                ),
              }))
            } else if (event.type === 'done') {
              setState(prev => ({
                ...prev,
                sessionId: event.session_id ?? prev.sessionId,
                streaming: false,
                messages: prev.messages.map(m =>
                  m.id === assistantMsg.id ? { ...m, streaming: false } : m
                ),
              }))
            } else if (event.type === 'error') {
              throw new Error(event.content)
            }
          } catch (parseErr) {
            // Ignore malformed SSE lines
          }
        }
      }
    } catch (err) {
      if ((err as Error).name === 'AbortError') return

      const message = err instanceof Error ? err.message : 'Chat failed'
      setState(prev => ({
        ...prev,
        streaming: false,
        error: message,
        messages: prev.messages.map(m =>
          m.id === assistantMsg.id
            ? { ...m, streaming: false, content: m.content || '(error)' }
            : m
        ),
      }))
    }
  }, [state.streaming, state.sessionId, predictionId])

  const reset = useCallback(() => {
    abortRef.current?.abort()
    setState({ messages: [], sessionId: null, streaming: false, error: null })
  }, [])

  return {
    messages: state.messages,
    sessionId: state.sessionId,
    streaming: state.streaming,
    error: state.error,
    sendMessage,
    reset,
  }
}
