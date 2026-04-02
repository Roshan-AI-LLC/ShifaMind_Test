"use client"

import { AppShell } from "@/components/app-shell"
import { useAuth } from "@/hooks/use-auth"

function initials(name: string): string {
  return name
    .split(" ")
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() ?? "")
    .join("")
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { user, isLoading } = useAuth()

  const displayName =
    user?.user_metadata?.full_name ||
    user?.user_metadata?.name ||
    user?.email?.split("@")[0] ||
    "Doctor"

  const doctorUser = user
    ? {
        name: displayName,
        email: user.email ?? "",
        initials: initials(displayName),
      }
    : undefined

  const isAdmin = user?.user_metadata?.role === "admin"

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <AppShell
      user={doctorUser}
      isAdmin={isAdmin}
      isDemoMode={false}
    >
      {children}
    </AppShell>
  )
}
