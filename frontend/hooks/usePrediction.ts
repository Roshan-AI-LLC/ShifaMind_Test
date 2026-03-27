'use client'

import { useState, useCallback } from 'react'
import { predict } from '@/lib/api'
import { selectMockResult } from '@/lib/mock-data'
import type { PredictResponse } from '@/types'

interface UsePredictionState {
  result: PredictResponse | null
  loading: boolean
  error: string | null
  isDemo: boolean
}

export function usePrediction() {
  const [state, setState] = useState<UsePredictionState>({
    result: null,
    loading: false,
    error: null,
    isDemo: false,
  })

  const runPrediction = useCallback(async (text: string, applyTunedThresholds = true) => {
    setState({ result: null, loading: true, error: null, isDemo: false })

    try {
      const result = await predict(text, applyTunedThresholds)
      setState({ result, loading: false, error: null, isDemo: false })
      return result
    } catch {
      // Backend unreachable — fall back to mock data seamlessly
      await new Promise(r => setTimeout(r, 800 + Math.random() * 600))
      const result = selectMockResult(text)

      // Persist for the chat page to pick up without a real prediction_id
      try {
        sessionStorage.setItem('shifamind_demo_prediction', JSON.stringify(result))
      } catch {
        // sessionStorage unavailable (e.g. private browsing restrictions) — ignore
      }

      setState({ result, loading: false, error: null, isDemo: true })
      return result
    }
  }, [])

  const reset = useCallback(() => {
    setState({ result: null, loading: false, error: null, isDemo: false })
  }, [])

  return {
    ...state,
    runPrediction,
    reset,
  }
}
