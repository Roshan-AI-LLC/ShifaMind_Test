'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState, useRef } from 'react'
import {
  LayoutDashboard,
  FlaskConical,
  MessageSquare,
  History,
  User,
  ChevronRight,
  Brain,
  Shield,
  X,
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
  mobileOpen?: boolean
  onMobileClose?: () => void
}

export function Sidebar({ isAdmin = false, mobileOpen = false, onMobileClose }: SidebarProps) {
  const [expanded, setExpanded] = useState(false)
  const collapseTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const pathname = usePathname()

  function handleMouseEnter() {
    if (collapseTimerRef.current) clearTimeout(collapseTimerRef.current)
    setExpanded(true)
  }

  function handleMouseLeave() {
    collapseTimerRef.current = setTimeout(() => setExpanded(false), 300)
  }

  const showLabels = expanded || mobileOpen

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 h-full z-40 flex flex-col',
        'border-r border-white/[0.06] transition-all duration-300',
        expanded ? 'lg:w-60' : 'lg:w-16',
        mobileOpen ? 'translate-x-0 w-64' : '-translate-x-full lg:translate-x-0',
      )}
      style={{
        background: 'rgba(6, 10, 19, 0.85)',
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        boxShadow: '4px 0 24px rgba(0, 0, 0, 0.2)',
      }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
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
          {showLabels && (
            <span className="font-semibold text-sm whitespace-nowrap" style={{ color: 'var(--text-primary)' }}>
              ShifaMind
            </span>
          )}
        </div>
        {/* Close button — mobile only */}
        {mobileOpen && (
          <button
            onClick={onMobileClose}
            className="ml-auto w-8 h-8 rounded-xl flex items-center justify-center hover:bg-white/[0.06] transition-colors lg:hidden"
          >
            <X className="w-4 h-4" style={{ color: 'var(--text-muted)' }} />
          </button>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 py-4 space-y-0.5 px-2 overflow-y-auto">
        {NAV_ITEMS.map(({ href, icon: Icon, label }, i) => {
          const active = pathname === href || (href !== '/dashboard' && pathname.startsWith(href))
          return (
            <Link
              key={href}
              href={href}
              prefetch={true}
              onClick={onMobileClose}
              title={!showLabels ? label : undefined}
              className={cn(
                'animate-fade-in',
                'flex items-center gap-3 rounded-xl px-3 py-2.5 transition-all duration-150',
                'border-l-2',
                active
                  ? 'bg-white/[0.08] border-l-[#4ecdc4] text-[var(--accent)]'
                  : 'border-l-transparent text-[var(--text-secondary)] hover:bg-white/[0.06] hover:text-[var(--text-primary)] hover:brightness-125'
              )}
              style={{
                animationDelay: `${i * 40}ms`,
                animationFillMode: 'backwards',
                ...(active && { boxShadow: 'inset 3px 0 8px rgba(78,205,196,0.15)' }),
              }}
            >
              <Icon className="w-5 h-5 shrink-0" />
              {showLabels && <span className="text-sm font-medium truncate">{label}</span>}
            </Link>
          )
        })}

        {isAdmin && (
          <>
            <div className="my-2 mx-2 border-t border-white/[0.06]" />
            {ADMIN_ITEMS.map(({ href, icon: Icon, label }) => {
              const active = pathname.startsWith(href)
              return (
                <Link
                  key={href}
                  href={href}
                  prefetch={true}
                  onClick={onMobileClose}
                  title={!showLabels ? label : undefined}
                  className={cn(
                    'flex items-center gap-3 rounded-xl px-3 py-2.5 transition-all duration-150',
                    'border-l-2',
                    active
                      ? 'bg-white/[0.08] border-l-[#4ecdc4] text-[var(--accent)]'
                      : 'border-l-transparent text-[var(--text-secondary)] hover:bg-white/[0.06] hover:text-[var(--text-primary)] hover:brightness-125'
                  )}
                >
                  <Icon className="w-5 h-5 shrink-0" />
                  {showLabels && <span className="text-sm font-medium truncate">{label}</span>}
                </Link>
              )
            })}
          </>
        )}
      </nav>

      {/* Expand toggle — desktop only */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="m-2 hidden lg:flex items-center justify-center h-9 rounded-xl border border-white/[0.08]
          hover:bg-white/[0.06] transition-colors"
        style={{ background: 'rgba(255,255,255,0.02)', color: 'rgba(255,255,255,0.35)' }}
      >
        <ChevronRight className={cn('w-4 h-4 transition-transform duration-300', expanded && 'rotate-180')} />
      </button>
    </aside>
  )
}
