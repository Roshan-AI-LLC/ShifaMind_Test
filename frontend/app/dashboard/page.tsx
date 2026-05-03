"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { FlaskConical, MessageSquare, History, Activity, Zap, BarChart3, Clock } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { StatsTrend } from "@/components/ui/stats-trend"
import { cn } from "@/lib/utils"
import { useAuth } from "@/hooks/use-auth"
import { createClient } from "@/lib/supabase"

const quickActions = [
  {
    title: "Workspace",
    description: "Analyze clinical notes with AI",
    href: "/dashboard/workspace",
    icon: FlaskConical,
    color: "text-primary",
    bgColor: "bg-primary/20",
  },
  {
    title: "Chat",
    description: "Discuss findings with AI assistant",
    href: "/dashboard/chat",
    icon: MessageSquare,
    color: "text-gold",
    bgColor: "bg-gold/20",
  },
  {
    title: "History",
    description: "Review past predictions",
    href: "/dashboard/history",
    icon: History,
    color: "text-destructive",
    bgColor: "bg-destructive/20",
  },
]

export default function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState({ predictions: 0, chatSessions: 0 })

  const displayName =
    user?.user_metadata?.full_name ||
    user?.user_metadata?.name ||
    user?.email?.split("@")[0] ||
    "Doctor"

  useEffect(() => {
    if (!user) return
    const supabase = createClient()
    Promise.all([
      supabase
        .from("predictions")
        .select("id", { count: "exact", head: true })
        .eq("doctor_id", user.id),
      supabase
        .from("chat_sessions")
        .select("id", { count: "exact", head: true })
        .eq("doctor_id", user.id),
    ]).then(([pred, chat]) => {
      setStats({
        predictions: pred.error ? 0 : pred.count ?? 0,
        chatSessions: chat.error ? 0 : chat.count ?? 0,
      })
    })
  }, [user])

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="animate-fade-in">
        <h1 className="text-2xl lg:text-3xl font-semibold text-foreground">
          Welcome back, {displayName}
        </h1>
        <p className="text-foreground-muted mt-1">Your clinical AI assistant is ready to help</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 animate-fade-in stagger-1">
        <StatsTrend
          label="Total Predictions"
          value={stats.predictions}
          icon={<Activity className="w-5 h-5" />}
          iconColor="teal"
        />
        <StatsTrend
          label="Chat Sessions"
          value={stats.chatSessions}
          icon={<MessageSquare className="w-5 h-5" />}
          iconColor="gold"
        />
      </div>

      <div className="space-y-4">
        <h2 className="text-lg font-medium text-foreground">Quick Actions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map((action, index) => {
            const Icon = action.icon
            return (
              <Link key={action.href} href={action.href}>
                <GlassCard hover className={cn("h-full animate-fade-in", `stagger-${index + 3}`)}>
                  <div className={cn("w-10 h-10 rounded-lg flex items-center justify-center", action.bgColor)}>
                    <Icon className={cn("w-5 h-5", action.color)} />
                  </div>
                  <h3 className="text-foreground font-medium mt-4">{action.title}</h3>
                  <p className="text-foreground-muted text-sm mt-1">{action.description}</p>
                </GlassCard>
              </Link>
            )
          })}
        </div>
      </div>

      <GlassCard className="animate-fade-in stagger-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-white/[0.06] flex items-center justify-center">
            <img src="/icon_transparent.png" className="w-8 h-8 object-contain opacity-80" alt="ShifaMind Model" />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <h3 className="text-foreground font-medium">ShifaMindMCB v2.1</h3>
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
            </div>
            <p className="text-foreground-muted text-sm">
              ShifaMind • 160 concepts • 50 ICD-10 codes
            </p>
          </div>
          <span className="hidden sm:inline-flex px-3 py-1 rounded-full text-xs font-medium bg-green-500/20 text-green-400 border border-green-500/30">
            Ready
          </span>
        </div>
      </GlassCard>
    </div>
  )
}
