'use client'

import { useEffect, useState } from 'react'
import { User } from '@supabase/supabase-js'
import { createClient } from '@/lib/supabase/client'

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

export function useAuth(): AuthState {
  const [user, setUser] = useState<User | null>(null)
  const [doctor, setDoctor] = useState<Doctor | null>(null)
  const [loading, setLoading] = useState(true)
  const supabase = createClient()

  useEffect(() => {
    async function getSession() {
      const { data: { user } } = await supabase.auth.getUser()
      setUser(user)

      if (user) {
        const { data } = await supabase
          .from('doctors')
          .select('*')
          .eq('id', user.id)
          .single()
        setDoctor(data)
      }

      setLoading(false)
    }

    getSession()

    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      setUser(session?.user ?? null)

      if (session?.user) {
        const { data } = await supabase
          .from('doctors')
          .select('*')
          .eq('id', session.user.id)
          .single()
        setDoctor(data)
      } else {
        setDoctor(null)
      }

      setLoading(false)
    })

    return () => subscription.unsubscribe()
  }, [])

  return { user, doctor, loading }
}
