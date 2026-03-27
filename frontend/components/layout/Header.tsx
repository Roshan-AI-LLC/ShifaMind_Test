'use client'

import { usePathname } from 'next/navigation'
import { LogOut, Menu } from 'lucide-react'
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

interface HeaderProps {
  onMobileMenuToggle?: () => void
}

export function Header({ onMobileMenuToggle }: HeaderProps) {
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
    <header className="sticky top-0 w-full h-16 z-20 flex items-center justify-between px-6
      glass border-b border-white/[0.06] transition-all duration-300">
      {/* Left: hamburger (mobile only) + breadcrumb */}
      <div className="flex items-center gap-3">
        <button
          onClick={onMobileMenuToggle}
          className="lg:hidden w-8 h-8 rounded-xl flex items-center justify-center hover:bg-white/[0.06] transition-colors"
          aria-label="Toggle menu"
        >
          <Menu className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
        </button>
        <div className="flex items-center gap-2">
          <span className="text-xs" style={{ color: 'var(--text-muted)' }}>ShifaMind</span>
          <span className="text-xs" style={{ color: 'var(--text-muted)' }}>/</span>
          <span className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>{label}</span>
        </div>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <div
            className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold shrink-0"
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
          className="w-8 h-8 rounded-xl flex items-center justify-center hover:bg-white/[0.06] transition-colors"
          title="Sign out"
        >
          <LogOut className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
        </button>
      </div>
    </header>
  )
}
