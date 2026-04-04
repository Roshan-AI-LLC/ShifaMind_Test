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

/** @type {import('next').NextConfig} */
const nextConfig = {
  env: publicEnvFromParent(),
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
}

export default nextConfig
