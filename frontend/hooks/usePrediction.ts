'use client'

import { useState, useCallback } from 'react'
import { predict } from '@/lib/api'
import { isDemoMode } from '@/lib/demo-mode'
import { selectMockResult } from '@/lib/mock-data'
import type { PredictResponse } from '@/types'

interface UsePredictionState {
  result: PredictResponse | null
  loading: boolean
  error: string | null
  demoMode: boolean
}

export function usePrediction() {
  const [state, setState] = useState<UsePredictionState>({
    result: null,
    loading: false,
    error: null,
    demoMode: false,
  })

  const runPrediction = useCallback(async (text: string, applyTunedThresholds = true) => {
    setState({ result: null, loading: true, error: null, demoMode: false })

    // Check demo mode first (3s timeout health check)
    const demo = await isDemoMode()

    if (demo) {
      // Simulate realistic inference delay
      await new Promise(r => setTimeout(r, 800 + Math.random() * 600))
      const result = selectMockResult(text)
      setState({ result, loading: false, error: null, demoMode: true })
      return result
    }

    try {
      const result = await predict(text, applyTunedThresholds)
      setState({ result, loading: false, error: null, demoMode: false })
      return result
    } catch (err) {
      // If real API fails mid-request, fall back to demo
      const result = selectMockResult(text)
      setState({ result, loading: false, error: null, demoMode: true })
      return result
    }
  }, [])

  const reset = useCallback(() => {
    setState({ result: null, loading: false, error: null, demoMode: false })
  }, [])

  return {
    ...state,
    runPrediction,
    reset,
  }
}
