'use client'

import { useState, useEffect } from 'react'
import { Sidebar } from './Sidebar'
import { Header } from './Header'
import { isDemoMode } from '@/lib/demo-mode'

interface AppShellProps {
  isAdmin?: boolean
  children: React.ReactNode
}

export function AppShell({ isAdmin = false, children }: AppShellProps) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [showDemoBanner, setShowDemoBanner] = useState(false)

  useEffect(() => {
    isDemoMode().then(setShowDemoBanner)
  }, [])

  return (
    <div className="min-h-screen relative" style={{ background: 'var(--bg-deep)' }}>

      {/* ── Ambient background ── */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div
          className="absolute rounded-full"
          style={{
            width: '500px', height: '500px',
            background: 'radial-gradient(circle, rgba(78,205,196,0.12), transparent 70%)',
            top: '-8%', left: '-5%',
            filter: 'blur(80px)',
            animation: 'float 25s ease-in-out infinite',
          }}
        />
        <div
          className="absolute rounded-full"
          style={{
            width: '400px', height: '400px',
            background: 'radial-gradient(circle, rgba(255,107,107,0.06), transparent 70%)',
            bottom: '-10%', right: '-5%',
            filter: 'blur(80px)',
            animation: 'float 25s ease-in-out infinite',
            animationDelay: '-8s',
          }}
        />
        <div
          className="absolute rounded-full"
          style={{
            width: '350px', height: '350px',
            background: 'radial-gradient(circle, rgba(78,205,196,0.06), transparent 70%)',
            top: '50%', left: '40%',
            transform: 'translate(-50%, -50%)',
            filter: 'blur(60px)',
            animation: 'float 25s ease-in-out infinite',
            animationDelay: '-15s',
          }}
        />
      </div>

      {/* ── Noise texture ── */}
      <div
        className="fixed inset-0 pointer-events-none z-[1]"
        style={{
          opacity: 0.02,
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
          backgroundRepeat: 'repeat',
        }}
      />

      {/* Mobile backdrop */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <Sidebar
        isAdmin={isAdmin}
        mobileOpen={mobileOpen}
        onMobileClose={() => setMobileOpen(false)}
      />

      {/* Content wrapper — shifts right of sidebar on desktop */}
      <div className="lg:ml-16 transition-all duration-300 relative z-[2]">
        {showDemoBanner && (
          <div
            className="flex items-center justify-center gap-2 px-4 py-2 text-xs text-center"
            style={{
              background: 'rgba(255, 217, 61, 0.08)',
              borderBottom: '1px solid rgba(255, 217, 61, 0.2)',
              color: '#ffd93d',
            }}
          >
            <span
              className="inline-block w-1.5 h-1.5 rounded-full animate-pulse"
              style={{ background: '#ffd93d' }}
            />
            Demo Mode — backend not connected. Showing mock BioClinicalBERT predictions.
          </div>
        )}
        <Header onMobileMenuToggle={() => setMobileOpen(v => !v)} />
        <main className="min-h-screen">
          <div className="p-4 sm:p-6">{children}</div>
        </main>
      </div>
    </div>
  )
}
