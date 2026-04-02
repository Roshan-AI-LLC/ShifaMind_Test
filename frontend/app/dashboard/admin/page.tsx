"use client"

import { Shield, Database, Activity } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { AdminStats } from "@/components/admin/admin-stats"
import { ReviewsTable } from "@/components/admin/reviews-table"

export default function AdminPage() {
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

      {/* System Status Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <GlassCard className="space-y-4">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-primary" />
            <h3 className="font-medium text-foreground">API Status</h3>
          </div>
          <div>
            <div className="w-full h-2 rounded-full bg-white/[0.06] overflow-hidden">
              <div className="h-full w-full bg-gradient-to-r from-primary to-teal-400 rounded-full" />
            </div>
            <p className="text-xs text-foreground-muted mt-2">99.8% uptime (30 days)</p>
          </div>
          <div className="pt-3 border-t border-white/[0.06]">
            <p className="text-xs text-foreground-muted mb-2">Response Time</p>
            <p className="text-sm font-mono text-primary">324ms avg</p>
          </div>
        </GlassCard>

        <GlassCard className="space-y-4">
          <div className="flex items-center gap-2">
            <Database className="w-5 h-5 text-gold" />
            <h3 className="font-medium text-foreground">Model Performance</h3>
          </div>
          <div>
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs text-foreground-muted">Accuracy</p>
              <p className="text-sm font-semibold text-gold">94.2%</p>
            </div>
            <div className="w-full h-2 rounded-full bg-white/[0.06] overflow-hidden">
              <div className="h-full w-[94.2%] bg-gradient-to-r from-gold to-yellow-400 rounded-full" />
            </div>
          </div>
          <div className="pt-3 border-t border-white/[0.06]">
            <p className="text-xs text-foreground-muted mb-2">Last Training</p>
            <p className="text-sm font-mono text-foreground">Jan 12, 2024</p>
          </div>
        </GlassCard>

        <GlassCard className="space-y-4">
          <div className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-primary" />
            <h3 className="font-medium text-foreground">Security</h3>
          </div>
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-primary" />
              <span className="text-xs text-foreground-muted">SSL Encrypted</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-primary" />
              <span className="text-xs text-foreground-muted">HIPAA Compliant</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-primary" />
              <span className="text-xs text-foreground-muted">2FA Enabled</span>
            </div>
          </div>
        </GlassCard>
      </div>

      {/* Reviews & Feedback */}
      <ReviewsTable />

      {/* Activity Log */}
      <GlassCard className="space-y-4">
        <h3 className="font-semibold text-foreground">Recent System Activity</h3>
        <div className="space-y-3">
          {[
            { event: "Model retraining completed", time: "2 hours ago", status: "success" },
            { event: "Database backup finished", time: "4 hours ago", status: "success" },
            { event: "Security audit scheduled", time: "1 day ago", status: "info" },
            { event: "API rate limit adjustment", time: "2 days ago", status: "warning" },
            { event: "New user milestone: 250 active users", time: "3 days ago", status: "success" },
          ].map((item, i) => (
            <div key={i} className="flex items-start justify-between py-3 border-b border-white/[0.06] last:border-0">
              <div className="flex-1">
                <p className="text-sm text-foreground">{item.event}</p>
              </div>
              <span className="text-xs text-foreground-muted ml-4 whitespace-nowrap">{item.time}</span>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  )
}
