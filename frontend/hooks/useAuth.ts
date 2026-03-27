'use client'

import { useEffect, useState } from 'react'
import type { User } from '@supabase/supabase-js'

interface Doctor {
  id: string
  full_name: string
  specialty: string | null
  institution: string | null
  email: string
  role: 'doctor' | 'admin'
  is_active: boolean
}

interface AuthState {
  user: User | null
  doctor: Doctor | null
  loading: boolean
}

// ── Module-level singleton ────────────────────────────────────────────────────
// Shared across every useAuth() caller so we fetch exactly once per session.

let _user: User | null = null
let _doctor: Doctor | null = null
let _loading = true
let _initialized = false
const _listeners = new Set<() => void>()

function notify() {
  _listeners.forEach(fn => fn())
}

function initAuth() {
  if (_initialized) return
  _initialized = true

  // Lazy import avoids calling createBrowserClient at module load time
  // (which throws when env vars are missing — e.g. demo environment)
  import('@/lib/supabase/client').then(({ createClient }) => {
    const supabase = createClient()

    supabase.auth.getUser()
      .then(({ data: { user } }) => {
        _user = user
        if (user) {
          void (async () => {
            try {
              const { data } = await supabase
                .from('doctors')
                .select('*')
                .eq('id', user.id)
                .single()
              _doctor = data
            } catch {}
            _loading = false
            notify()
          })()
        } else {
          _loading = false
          notify()
        }
      })
      .catch(() => {
        _loading = false
        notify()
      })

    supabase.auth.onAuthStateChange((_event, session) => {
      _user = session?.user ?? null
      if (!session?.user) {
        _doctor = null
        _loading = false
        notify()
      } else {
        void (async () => {
          try {
            const { data } = await supabase
              .from('doctors')
              .select('*')
              .eq('id', session.user.id)
              .single()
            _doctor = data
          } catch {}
          notify()
        })()
      }
    })
  }).catch(() => {
    // Supabase not configured (demo env) — mark as loaded with no user
    _loading = false
    notify()
  })
}

// ── Hook ─────────────────────────────────────────────────────────────────────

export function useAuth(): AuthState {
  // forceUpdate triggers a re-render when the module-level state changes
  const [, forceUpdate] = useState(0)

  useEffect(() => {
    initAuth()

    const listener = () => forceUpdate(n => n + 1)
    _listeners.add(listener)

    // If already initialized, trigger one render so stale state is flushed
    if (!_loading) listener()

    return () => {
      _listeners.delete(listener)
    }
  }, [])

  return { user: _user, doctor: _doctor, loading: _loading }
}
