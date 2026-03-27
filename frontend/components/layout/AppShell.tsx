'use client'

import { useState } from 'react'
import { Sidebar } from './Sidebar'
import { Header } from './Header'

interface AppShellProps {
  isAdmin?: boolean
  children: React.ReactNode
}

export function AppShell({ isAdmin = false, children }: AppShellProps) {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <>
      <Sidebar
        isAdmin={isAdmin}
        mobileOpen={mobileOpen}
        onMobileClose={() => setMobileOpen(false)}
      />

      {/* Mobile backdrop */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-30 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Content wrapper — shifts right of sidebar on desktop */}
      <div className="lg:ml-16 transition-all duration-300 relative z-10">
        <Header onMobileMenuToggle={() => setMobileOpen(v => !v)} />
        <main className="min-h-screen">
          <div className="p-6">{children}</div>
        </main>
      </div>
    </>
  )
}
