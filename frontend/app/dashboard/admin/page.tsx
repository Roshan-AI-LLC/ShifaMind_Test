"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/hooks/use-auth"
import { Shield, Database, Activity, Lock } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { AdminStats } from "@/components/admin/admin-stats"
import { ReviewsTable } from "@/components/admin/reviews-table"

export default function AdminPage() {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && user?.email !== "admin@shifamind.me") {
      router.replace("/dashboard")
    }
  }, [user, isLoading, router])

  if (isLoading || user?.email !== "admin@shifamind.me") {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <Lock className="w-12 h-12 text-primary" />
        <h2 className="text-xl font-medium text-foreground">Admin Access Required</h2>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Admin Dashboard</h1>
          <p className="text-foreground-muted mt-1">System metrics, user activity, and model performance</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-gold/20 border border-gold/30">
          <div className="w-2 h-2 rounded-full bg-gold animate-pulse" />
          <span className="text-xs font-medium text-gold">System Healthy</span>
        </div>
      </div>

      {/* Top Stats */}
      <AdminStats />

      {/* Reviews & Feedback */}
      <ReviewsTable />
    </div>
  )
}
