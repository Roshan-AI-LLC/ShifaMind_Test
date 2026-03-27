'use client'

import { Suspense, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { Brain, Mail, Lock, ArrowRight, Loader2, ExternalLink } from 'lucide-react'
import { GlassCard } from '@/components/shared/GlassCard'

type Mode = 'password' | 'magic'

export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  )
}

function LoginForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const redirectTo = searchParams.get('redirectTo') ?? '/dashboard'

  const [mode, setMode] = useState<Mode>('password')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [magicSent, setMagicSent] = useState(false)

  const supabase = createClient()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      if (mode === 'password') {
        const { error } = await supabase.auth.signInWithPassword({ email, password })
        if (error) {
          setError(
            error.message === 'Invalid login credentials'
              ? 'Invalid email or password. Please try again.'
              : error.message
          )
          setLoading(false)
          return
        }
        router.push(redirectTo)
      } else {
        const { error } = await supabase.auth.signInWithOtp({
          email,
          options: {
            emailRedirectTo: `${window.location.origin}/dashboard`,
          },
        })
        if (error) {
          setError(error.message)
          setLoading(false)
          return
        }
        setMagicSent(true)
        setLoading(false)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Connection error. Check your Supabase URL and key in .env.local.')
      setLoading(false)
    }
  }

  return (
    <div
      className="min-h-screen flex items-center justify-center p-4"
      style={{ background: 'var(--bg-deep)' }}
    >
      <div className="w-full max-w-md animate-fade-in">
        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
            style={{
              background: 'var(--accent-dim)',
              border: '1px solid var(--accent-glow)',
              boxShadow: '0 0 30px var(--accent-glow)',
            }}
          >
            <Brain className="w-7 h-7" style={{ color: 'var(--accent)' }} />
          </div>
          <h1 className="text-2xl font-semibold tracking-tight" style={{ color: 'var(--text-primary)' }}>
            ShifaMind
          </h1>
          <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>
            Clinical Decision Support Platform
          </p>
        </div>

        <GlassCard className="p-8">
          {magicSent ? (
            <div className="text-center py-4">
              <Mail className="w-10 h-10 mx-auto mb-4" style={{ color: 'var(--accent)' }} />
              <h2 className="font-semibold mb-2" style={{ color: 'var(--text-primary)' }}>Check your email</h2>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                We sent a magic link to <strong>{email}</strong>. Click it to sign in.
              </p>
              <button
                onClick={() => { setMagicSent(false); setMode('password') }}
                className="mt-6 text-sm underline"
                style={{ color: 'var(--text-muted)' }}
              >
                Back to sign in
              </button>
            </div>
          ) : (
            <>
              <h2 className="text-lg font-semibold mb-6" style={{ color: 'var(--text-primary)' }}>
                {mode === 'password' ? 'Sign in to your account' : 'Sign in with magic link'}
              </h2>

              {error && (
                <div
                  className="mb-4 px-4 py-3 rounded-xl text-sm"
                  style={{
                    background: 'rgba(255, 107, 107, 0.1)',
                    border: '1px solid rgba(255, 107, 107, 0.3)',
                    color: 'var(--accent-warm)',
                  }}
                >
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Email */}
                <div>
                  <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                    Email address
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style={{ color: 'var(--text-muted)' }} />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      placeholder="doctor@hospital.com"
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl text-sm outline-none transition-all"
                      style={{
                        background: 'var(--glass-bg)',
                        border: '1px solid var(--glass-border)',
                        color: 'var(--text-primary)',
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = 'rgba(78, 205, 196, 0.5)'
                        e.target.style.boxShadow = '0 0 0 1px rgba(78, 205, 196, 0.3)'
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = 'var(--glass-border)'
                        e.target.style.boxShadow = 'none'
                      }}
                    />
                  </div>
                </div>

                {/* Password */}
                {mode === 'password' && (
                  <div>
                    <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-secondary)' }}>
                      Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style={{ color: 'var(--text-muted)' }} />
                      <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        placeholder="••••••••"
                        className="w-full pl-10 pr-4 py-2.5 rounded-xl text-sm outline-none transition-all"
                        style={{
                          background: 'var(--glass-bg)',
                          border: '1px solid var(--glass-border)',
                          color: 'var(--text-primary)',
                        }}
                        onFocus={(e) => {
                          e.target.style.borderColor = 'rgba(78, 205, 196, 0.5)'
                          e.target.style.boxShadow = '0 0 0 1px rgba(78, 205, 196, 0.3)'
                        }}
                        onBlur={(e) => {
                          e.target.style.borderColor = 'var(--glass-border)'
                          e.target.style.boxShadow = 'none'
                        }}
                      />
                    </div>
                  </div>
                )}

                {/* Submit */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl font-medium text-sm
                    transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  style={{
                    background: '#4ecdc4',
                    color: '#060a13',
                    boxShadow: '0 4px 20px rgba(78, 205, 196, 0.2)',
                  }}
                >
                  {loading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <>
                      {mode === 'password' ? 'Sign in' : 'Send magic link'}
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </form>

              {/* Toggle mode */}
              <div className="mt-5 text-center">
                <button
                  onClick={() => { setMode(mode === 'password' ? 'magic' : 'password'); setError(null) }}
                  className="text-sm transition-colors"
                  style={{ color: 'var(--text-muted)' }}
                  onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--accent)')}
                  onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-muted)')}
                >
                  {mode === 'password'
                    ? 'Sign in with magic link instead'
                    : 'Sign in with password instead'}
                </button>
              </div>
            </>
          )}
        </GlassCard>

        {/* Back to main site */}
        <div className="mt-6 text-center">
          <a
            href="https://shifamind.me"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs transition-colors"
            style={{ color: 'var(--text-muted)' }}
            onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--text-secondary)')}
            onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-muted)')}
          >
            <ExternalLink className="w-3 h-3" />
            shifamind.me
          </a>
        </div>
      </div>
    </div>
  )
}
