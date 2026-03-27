'use client'

import { useState, useCallback } from 'react'
import { predict } from '@/lib/api'
import type { PredictResponse } from '@/types'

interface UsePredictionState {
  result: PredictResponse | null
  loading: boolean
  error: string | null
}

export function usePrediction() {
  const [state, setState] = useState<UsePredictionState>({
    result: null,
    loading: false,
    error: null,
  })

  const runPrediction = useCallback(async (text: string, applyTunedThresholds = true) => {
    setState({ result: null, loading: true, error: null })
    try {
      const result = await predict(text, applyTunedThresholds)
      setState({ result, loading: false, error: null })
      return result
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Prediction failed'
      setState({ result: null, loading: false, error: message })
      return null
    }
  }, [])

  const reset = useCallback(() => {
    setState({ result: null, loading: false, error: null })
  }, [])

  return {
    ...state,
    runPrediction,
    reset,
  }
}
