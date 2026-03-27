const API_URL = process.env.NEXT_PUBLIC_API_URL ?? ''

let _cached: boolean | null = null
let _cacheTime = 0
const CACHE_TTL = 30_000 // 30 seconds

export async function isDemoMode(): Promise<boolean> {
  // Return cached result within TTL
  if (_cached !== null && Date.now() - _cacheTime < CACHE_TTL) {
    return _cached
  }

  if (!API_URL) {
    _cached = true
    _cacheTime = Date.now()
    return true
  }

  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 3000)
    const res = await fetch(`${API_URL}/api/health`, { signal: controller.signal })
    clearTimeout(timeout)
    const data = await res.json()
    _cached = data.status !== 'ok' || !data.model_loaded
  } catch {
    _cached = true
  }

  _cacheTime = Date.now()
  return _cached as boolean
}

export function resetDemoCache() {
  _cached = null
  _cacheTime = 0
}
