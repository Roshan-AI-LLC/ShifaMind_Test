'use client'

import { usePathname } from 'next/navigation'
import { LogOut, Bell } from 'lucide-react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'

const BREADCRUMBS: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/dashboard/workspace': 'Workspace',
  '/dashboard/chat': 'Chat',
  '/dashboard/history': 'History',
  '/dashboard/profile': 'Profile',
  '/admin': 'Admin',
}

export function Header() {
  const pathname = usePathname()
  const router = useRouter()
  const { doctor } = useAuth()
  const supabase = createClient()

  const label = BREADCRUMBS[pathname] ?? 'ShifaMind'

  async function handleSignOut() {
    await supabase.auth.signOut()
    router.push('/login')
  }

  const initials = doctor?.full_name
    ? doctor.full_name.split(' ').map((n: string) => n[0]).join('').slice(0, 2).toUpperCase()
    : 'DR'

  return (
    <header
      className="fixed top-0 right-0 h-16 z-30 flex items-center justify-between px-6
        glass border-b border-white/[0.06] transition-all duration-300"
      style={{ left: '64px' }}
    >
      {/* Breadcrumb */}
      <div className="flex items-center gap-2">
        <span className="text-xs" style={{ color: 'var(--text-muted)' }}>ShifaMind</span>
        <span className="text-xs" style={{ color: 'var(--text-muted)' }}>/</span>
        <span className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>{label}</span>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        <button className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-white/[0.06] transition-colors">
          <Bell className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
        </button>

        {/* Avatar */}
        <div className="flex items-center gap-2">
          <div
            className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold"
            style={{
              background: 'var(--accent-dim)',
              border: '1px solid var(--accent-glow)',
              color: 'var(--accent)',
            }}
          >
            {initials}
          </div>
          {doctor && (
            <span className="text-sm hidden sm:block" style={{ color: 'var(--text-secondary)' }}>
              {doctor.full_name}
            </span>
          )}
        </div>

        <button
          onClick={handleSignOut}
          className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-white/[0.06] transition-colors"
          title="Sign out"
        >
          <LogOut className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
        </button>
      </div>
    </header>
  )
}
