'use client'

import { useState, useCallback, useRef, type Dispatch, type SetStateAction } from 'react'
import { getAuthToken } from '@/lib/api'
import { generateMockChatResponse } from '@/lib/mock-data'
import type { PredictResponse } from '@/types'

export interface ChatMessageLocal {
  id: string
  role: 'user' | 'assistant'
  content: string
  streaming?: boolean
}

interface UseChatOptions {
  predictionId?: string | null
  /** Optional prediction context used to generate context-aware mock responses. */
  predictionContext?: PredictResponse | null
  initialSessionId?: string | null
}

interface UseChatState {
  messages: ChatMessageLocal[]
  sessionId: string | null
  streaming: boolean
  error: string | null
  isDemo: boolean
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? ''

async function streamMockResponse(
  message: string,
  assistantId: string,
  setState: Dispatch<SetStateAction<UseChatState>>,
  context?: PredictResponse | null
) {
  const fullText = generateMockChatResponse(
    message,
    context?.predictions ?? [],
    context?.activated_concepts ?? []
  )

  // Word-by-word streaming with natural 30–70 ms cadence
  const words = fullText.split(' ')
  for (let i = 0; i < words.length; i++) {
    await new Promise(r => setTimeout(r, 30 + Math.random() * 40))
    const chunk = i === 0 ? words[i] : ' ' + words[i]
    setState(prev => ({
      ...prev,
      messages: prev.messages.map(m =>
        m.id === assistantId ? { ...m, content: m.content + chunk } : m
      ),
    }))
  }

  setState(prev => ({
    ...prev,
    streaming: false,
    messages: prev.messages.map(m =>
      m.id === assistantId ? { ...m, streaming: false } : m
    ),
  }))
}

export function useChat({ predictionId, predictionContext, initialSessionId }: UseChatOptions = {}) {
  const [state, setState] = useState<UseChatState>({
    messages: [],
    sessionId: initialSessionId ?? null,
    streaming: false,
    error: null,
    isDemo: false,
  })

  const abortRef = useRef<AbortController | null>(null)

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || state.streaming) return

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
          } catch {
            // Ignore malformed SSE lines
          }
        }
      }
    } catch (err) {
      if ((err as Error).name === 'AbortError') return

      // Backend unreachable — fall back to mock streaming with prediction context
      let ctx = predictionContext ?? null
      if (!ctx) {
        try {
          const stored = sessionStorage.getItem('shifamind_demo_prediction')
          if (stored) ctx = JSON.parse(stored) as PredictResponse
        } catch {
          // sessionStorage unavailable — proceed without context
        }
      }

      setState(prev => ({ ...prev, isDemo: true }))
      await streamMockResponse(content, assistantMsg.id, setState, ctx)
    }
  }, [state.streaming, state.sessionId, predictionId, predictionContext])

  const reset = useCallback(() => {
    abortRef.current?.abort()
    setState({ messages: [], sessionId: null, streaming: false, error: null, isDemo: false })
  }, [])

  return {
    messages: state.messages,
    sessionId: state.sessionId,
    streaming: state.streaming,
    error: state.error,
    isDemo: state.isDemo,
    sendMessage,
    reset,
  }
}
