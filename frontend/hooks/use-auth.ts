'use client'

import { useEffect, useState } from 'react'
import type { User, Session } from '@supabase/supabase-js'
import { createClient } from '@/lib/supabase'

interface AuthState {
  user: User | null
  session: Session | null
  isLoading: boolean
}

export function useAuth(): AuthState {
  const [state, setState] = useState<AuthState>({
    user: null,
    session: null,
    isLoading: true,
  })

  useEffect(() => {
    const supabase = createClient()

    // Initial session fetch
    supabase.auth.getSession().then(({ data: { session } }) => {
      setState({ user: session?.user ?? null, session, isLoading: false })
    })

    // Listen for auth state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setState({ user: session?.user ?? null, session, isLoading: false })
    })

    return () => subscription.unsubscribe()
  }, [])

  return state
}
