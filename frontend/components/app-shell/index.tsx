"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import { Sidebar } from "./sidebar"
import { Header } from "./header"
import { cn } from "@/lib/utils"

interface AppShellProps {
  children: React.ReactNode
  user?: {
    name: string
    email: string
    initials: string
  }
  isAdmin?: boolean
  isDemoMode?: boolean
  noPadding?: boolean
}

export function AppShell({ 
  children, 
  user, 
  isAdmin = false, 
  isDemoMode = false,
  noPadding = false 
}: AppShellProps) {
  const router = useRouter()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false)

  const handleSignOut = () => {
    // For now, just redirect to login
    router.push("/login")
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <Sidebar 
        isAdmin={isAdmin}
        isMobileOpen={isMobileMenuOpen}
        onMobileClose={() => setIsMobileMenuOpen(false)}
      />

      {/* Main content area - shifts right of sidebar on desktop */}
      <div className="lg:pl-16 min-h-screen flex flex-col">
        {/* Header */}
        <Header 
          user={user}
          onMenuClick={() => setIsMobileMenuOpen(true)}
          onSignOut={handleSignOut}
        />

        {/* Demo mode banner */}
        {isDemoMode && (
          <div className="bg-gold/10 border-b border-gold/20 px-4 py-2">
            <p className="text-sm text-gold text-center">
              <span className="font-medium">Demo Mode</span> — Backend unavailable. Using mock data.
            </p>
          </div>
        )}

        {/* Page content */}
        <main className={cn(
          "flex-1",
          !noPadding && "p-4 lg:p-6"
        )}>
          {children}
        </main>
      </div>
    </div>
  )
}

export { Sidebar } from "./sidebar"
export { Header } from "./header"
