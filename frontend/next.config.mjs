import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const parentEnvPath = path.join(__dirname, '..', '.env')

/** Minimal .env parser (parent `shifamind_test/.env` is not auto-loaded when cwd is `frontend/`). */
function parseEnvFile(filePath) {
  try {
    const src = fs.readFileSync(filePath, 'utf8')
    const out = {}
    for (const raw of src.split('\n')) {
      const line = raw.trim()
      if (!line || line.startsWith('#')) continue
      const eq = line.indexOf('=')
      if (eq === -1) continue
      const key = line.slice(0, eq).trim()
      let val = line.slice(eq + 1).trim()
      if (
        (val.startsWith('"') && val.endsWith('"')) ||
        (val.startsWith("'") && val.endsWith("'"))
      ) {
        val = val.slice(1, -1)
      }
      out[key] = val
    }
    return out
  } catch {
    return {}
  }
}

const parentEnv = parseEnvFile(parentEnvPath)

/** Build `env` entries for the browser. Prefer OS/Netlify env, then parent `.env`. */
function publicEnvFromParent() {
  const keys = new Set([
    ...Object.keys(parentEnv).filter((k) => k.startsWith('NEXT_PUBLIC_')),
  ])
  for (const k of Object.keys(process.env)) {
    if (k.startsWith('NEXT_PUBLIC_')) keys.add(k)
  }
  const env = {}
  for (const k of keys) {
    const v = process.env[k] || parentEnv[k]
    if (v) env[k] = v
  }
  return env
}

/**
 * Path-based hosting under platform.roshan-ai.com/shifamind.
 * Opt-in: only takes effect when NEXT_PUBLIC_BASE_PATH is set (e.g. "/shifamind"),
 * so the current platform.shifamind.me deploy keeps working until the cutover.
 * At cutover, set NEXT_PUBLIC_BASE_PATH=/shifamind in Netlify and add the rewrite
 * on platform.roshan-ai.com (see DOMAIN_MIGRATION.md).
 */
const basePath = (process.env.NEXT_PUBLIC_BASE_PATH || parentEnv.NEXT_PUBLIC_BASE_PATH || '').replace(/\/$/, '')

/** @type {import('next').NextConfig} */
const nextConfig = {
  devIndicators: false,
  ...(basePath ? { basePath, assetPrefix: basePath } : {}),
  env: { ...publicEnvFromParent(), NEXT_PUBLIC_BASE_PATH: basePath },
  images: {
    unoptimized: true,
  },
  async redirects() {
    return [
      {
        source: '/',
        destination: '/login',
        permanent: false,
      },
    ]
  },
}

export default nextConfig
