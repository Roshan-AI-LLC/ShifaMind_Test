"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  FlaskConical,
  MessageSquare,
  History,
  User,
  Shield,
  ChevronLeft,
  Brain,
  X,
} from "lucide-react"

interface NavItem {
  label: string
  href: string
  icon: React.ElementType
  adminOnly?: boolean
}

const navItems: NavItem[] = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Workspace", href: "/dashboard/workspace", icon: FlaskConical },
  { label: "Chat", href: "/dashboard/chat", icon: MessageSquare },
  { label: "History", href: "/dashboard/history", icon: History },
  { label: "Profile", href: "/dashboard/profile", icon: User },
]

const adminItems: NavItem[] = [
  { label: "Admin", href: "/dashboard/admin", icon: Shield, adminOnly: true },
]

interface SidebarProps {
  isAdmin?: boolean
  isMobileOpen?: boolean
  onMobileClose?: () => void
}

export function Sidebar({ isAdmin = false, isMobileOpen = false, onMobileClose }: SidebarProps) {
  const pathname = usePathname()
  const [isExpanded, setIsExpanded] = React.useState(false)

  const allItems = isAdmin ? [...navItems, ...adminItems] : navItems

  return (
    <>
      {/* Mobile overlay */}
      {isMobileOpen && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={onMobileClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed top-0 left-0 h-full z-50 transition-all duration-300 ease-out",
          "bg-sidebar/80 backdrop-blur-xl border-r border-sidebar-border",
          // Desktop: icon-only by default, expands on hover
          "hidden lg:flex lg:flex-col",
          isExpanded ? "lg:w-60" : "lg:w-16",
          // Mobile: full overlay
          "max-lg:w-60",
          isMobileOpen ? "max-lg:flex max-lg:flex-col" : "max-lg:hidden"
        )}
        onMouseEnter={() => setIsExpanded(true)}
        onMouseLeave={() => setIsExpanded(false)}
      >
        {/* Logo area */}
        <div className="flex items-center h-16 px-4 border-b border-sidebar-border">
          <Link href="/dashboard" className="flex items-center gap-3">
            <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-primary/20">
              <Brain className="w-5 h-5 text-primary" />
            </div>
            <span 
              className={cn(
                "font-semibold text-lg text-foreground whitespace-nowrap transition-opacity duration-200",
                isExpanded || isMobileOpen ? "opacity-100" : "opacity-0 lg:hidden"
              )}
            >
              ShifaMind
            </span>
          </Link>
          
          {/* Mobile close button */}
          <button
            onClick={onMobileClose}
            className="ml-auto lg:hidden p-2 rounded-lg hover:bg-white/[0.06] transition-colors"
            aria-label="Close sidebar"
          >
            <X className="w-5 h-5 text-foreground-muted" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 px-2 space-y-1 overflow-y-auto">
          {allItems.map((item, index) => {
            const isActive = pathname === item.href || 
              (item.href !== "/dashboard" && pathname.startsWith(item.href))
            const Icon = item.icon
            const showDivider = item.adminOnly && index > 0

            return (
              <React.Fragment key={item.href}>
                {showDivider && (
                  <div className="my-3 mx-2 border-t border-sidebar-border" />
                )}
                <Link
                  href={item.href}
                  onClick={onMobileClose}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-150",
                    "hover:bg-white/[0.06]",
                    isActive && "bg-sidebar-accent border-l-2 border-primary"
                  )}
                >
                  <Icon 
                    className={cn(
                      "w-5 h-5 shrink-0",
                      isActive ? "text-primary" : "text-foreground-muted"
                    )} 
                  />
                  <span 
                    className={cn(
                      "text-sm whitespace-nowrap transition-opacity duration-200",
                      isActive ? "text-foreground font-medium" : "text-foreground-muted",
                      isExpanded || isMobileOpen ? "opacity-100" : "opacity-0 lg:hidden"
                    )}
                  >
                    {item.label}
                  </span>
                </Link>
              </React.Fragment>
            )
          })}
        </nav>

        {/* Collapse indicator (desktop only) */}
        <div className="hidden lg:flex items-center justify-center py-4 border-t border-sidebar-border">
          <ChevronLeft 
            className={cn(
              "w-4 h-4 text-foreground-subtle transition-transform duration-300",
              !isExpanded && "rotate-180"
            )}
          />
        </div>
      </aside>
    </>
  )
}
