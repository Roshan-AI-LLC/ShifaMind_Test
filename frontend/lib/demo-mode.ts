const API_URL = process.env.NEXT_PUBLIC_API_URL ?? ''

let _cached: boolean | null = null
let _cacheTime = 0
let _checkPromise: Promise<boolean> | null = null
const CACHE_TTL = 30_000 // 30 seconds

export async function isDemoMode(): Promise<boolean> {
  if (_cached !== null && Date.now() - _cacheTime < CACHE_TTL) return _cached
  if (_checkPromise) return _checkPromise

  _checkPromise = (async () => {
    if (!API_URL) {
      _cached = true
      _cacheTime = Date.now()
      _checkPromise = null
      return true
    }

    try {
      const res = await fetch(`${API_URL}/api/health`, {
        signal: AbortSignal.timeout(3000),
      })
      const data = await res.json()
      _cached = data.status !== 'ok' || !data.model_loaded
    } catch {
      _cached = true
    }

    _cacheTime = Date.now()
    _checkPromise = null
    return _cached as boolean
  })()

  return _checkPromise
}

/** Synchronous getter — returns cached value (defaults true if never checked). */
export function getDemoMode(): boolean {
  return _cached ?? true
}

export function resetDemoCache() {
  _cached = null
  _cacheTime = 0
  _checkPromise = null
}
