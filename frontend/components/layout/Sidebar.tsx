'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'
import {
  LayoutDashboard,
  FlaskConical,
  MessageSquare,
  History,
  User,
  ChevronRight,
  Brain,
  Shield,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const NAV_ITEMS = [
  { href: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { href: '/dashboard/workspace', icon: FlaskConical, label: 'Workspace' },
  { href: '/dashboard/chat', icon: MessageSquare, label: 'Chat' },
  { href: '/dashboard/history', icon: History, label: 'History' },
  { href: '/dashboard/profile', icon: User, label: 'Profile' },
]

const ADMIN_ITEMS = [
  { href: '/admin', icon: Shield, label: 'Admin' },
]

interface SidebarProps {
  isAdmin?: boolean
}

export function Sidebar({ isAdmin = false }: SidebarProps) {
  const [expanded, setExpanded] = useState(false)
  const pathname = usePathname()

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 h-full z-40 flex flex-col',
        'glass border-r border-white/[0.06] transition-all duration-300',
        expanded ? 'w-60' : 'w-16'
      )}
    >
      {/* Logo */}
      <div className="flex items-center h-16 px-4 border-b border-white/[0.06] shrink-0">
        <div className="flex items-center gap-3 overflow-hidden">
          <div
            className="w-8 h-8 rounded-xl flex items-center justify-center shrink-0"
            style={{ background: 'var(--accent-dim)', border: '1px solid var(--accent-glow)' }}
          >
            <Brain className="w-4 h-4" style={{ color: 'var(--accent)' }} />
          </div>
          {expanded && (
            <span className="font-semibold text-sm whitespace-nowrap" style={{ color: 'var(--text-primary)' }}>
              ShifaMind
            </span>
          )}
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 py-4 space-y-1 px-2 overflow-y-auto">
        {NAV_ITEMS.map(({ href, icon: Icon, label }) => {
          const active = pathname === href || (href !== '/dashboard' && pathname.startsWith(href))
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                'flex items-center gap-3 rounded-xl px-3 py-2.5 transition-colors duration-150',
                'group relative',
                active
                  ? 'bg-[var(--accent-dim)] text-[var(--accent)]'
                  : 'text-[var(--text-secondary)] hover:bg-white/[0.06] hover:text-[var(--text-primary)]'
              )}
            >
              <Icon className="w-5 h-5 shrink-0" />
              {expanded && <span className="text-sm font-medium truncate">{label}</span>}
              {/* Tooltip when collapsed */}
              {!expanded && (
                <div className="absolute left-full ml-2 px-2 py-1 rounded-md text-xs whitespace-nowrap
                  bg-[#1a2340] border border-white/[0.08] text-white/80
                  opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity z-50">
                  {label}
                </div>
              )}
            </Link>
          )
        })}

        {isAdmin && (
          <>
            <div className="my-2 border-t border-white/[0.06]" />
            {ADMIN_ITEMS.map(({ href, icon: Icon, label }) => {
              const active = pathname.startsWith(href)
              return (
                <Link
                  key={href}
                  href={href}
                  className={cn(
                    'flex items-center gap-3 rounded-xl px-3 py-2.5 transition-colors duration-150 group relative',
                    active
                      ? 'bg-[var(--accent-dim)] text-[var(--accent)]'
                      : 'text-[var(--text-secondary)] hover:bg-white/[0.06] hover:text-[var(--text-primary)]'
                  )}
                >
                  <Icon className="w-5 h-5 shrink-0" />
                  {expanded && <span className="text-sm font-medium truncate">{label}</span>}
                  {!expanded && (
                    <div className="absolute left-full ml-2 px-2 py-1 rounded-md text-xs whitespace-nowrap
                      bg-[#1a2340] border border-white/[0.08] text-white/80
                      opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity z-50">
                      {label}
                    </div>
                  )}
                </Link>
              )
            })}
          </>
        )}
      </nav>

      {/* Expand toggle */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="m-2 flex items-center justify-center h-9 rounded-xl border border-white/[0.08]
          bg-white/[0.03] hover:bg-white/[0.06] transition-colors text-white/40 hover:text-white/70"
      >
        <ChevronRight className={cn('w-4 h-4 transition-transform duration-300', expanded && 'rotate-180')} />
      </button>
    </aside>
  )
}
