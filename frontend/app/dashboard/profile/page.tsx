"use client"

import { useEffect, useState } from "react"
import { Mail, Activity, MessageSquare, Star, Key, Bell } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { StatsTrend } from "@/components/ui/stats-trend"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { useAuth } from "@/hooks/use-auth"
import { createClient } from "@/lib/supabase"

function initials(name: string): string {
  return name.split(" ").slice(0, 2).map((w) => w[0]?.toUpperCase() ?? "").join("")
}

export default function ProfilePage() {
  const { user } = useAuth()
  const [stats, setStats] = useState({ predictions: 0, chatSessions: 0, reviews: 0 })

  const displayName =
    user?.user_metadata?.full_name ||
    user?.user_metadata?.name ||
    user?.email?.split("@")[0] ||
    "Doctor"

  const memberSince = user?.created_at
    ? new Date(user.created_at).toLocaleDateString("en-US", { month: "long", year: "numeric" })
    : "—"

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
      supabase
        .from("reviews")
        .select("id", { count: "exact", head: true })
        .eq("doctor_id", user.id),
    ]).then(([pred, chat, rev]) => {
      setStats({
        predictions: pred.error ? 0 : pred.count ?? 0,
        chatSessions: chat.error ? 0 : chat.count ?? 0,
        reviews: rev.error ? 0 : rev.count ?? 0,
      })
    })
  }, [user])

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-semibold text-foreground">Profile</h1>

      <GlassCard className="flex items-center gap-6">
        <Avatar className="w-20 h-20 bg-primary/20 border-2 border-primary/30">
          <AvatarFallback className="text-2xl font-semibold text-primary bg-transparent">
            {initials(displayName)}
          </AvatarFallback>
        </Avatar>
        <div>
          <h2 className="text-xl font-semibold text-foreground">{displayName}</h2>
          <span className="text-sm text-foreground-muted">Member since {memberSince}</span>
        </div>
      </GlassCard>

      <GlassCard className="space-y-4">
        <h3 className="font-medium text-foreground">Account Details</h3>
        <div className="flex items-center gap-3 py-2">
          <Mail className="w-4 h-4 text-foreground-subtle" />
          <span className="text-sm text-foreground-muted w-24">Email</span>
          <span className="text-sm text-foreground">{user?.email ?? "—"}</span>
        </div>
      </GlassCard>

      <div className="grid grid-cols-3 gap-4">
        <StatsTrend
          label="Predictions"
          value={stats.predictions}
          icon={<Activity className="w-5 h-5" />}
          iconColor="teal"
          variant="compact"
        />
        <StatsTrend
          label="Chat Sessions"
          value={stats.chatSessions}
          icon={<MessageSquare className="w-5 h-5" />}
          iconColor="gold"
          variant="compact"
        />
        <StatsTrend
          label="Reviews"
          value={stats.reviews}
          icon={<Star className="w-5 h-5" />}
          iconColor="red"
          variant="compact"
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <GlassCard className="space-y-4">
          <div className="flex items-center gap-2">
            <Key className="w-5 h-5 text-primary" />
            <h3 className="font-medium text-foreground">Security</h3>
          </div>
          <p className="text-sm text-foreground-muted">Manage your authentication settings.</p>
          <button className="px-4 py-2 rounded-lg bg-secondary border border-border text-sm text-foreground hover:bg-secondary transition-colors">
            Update Password
          </button>
        </GlassCard>

        <GlassCard className="space-y-4">
          <div className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-gold" />
            <h3 className="font-medium text-foreground">Notifications</h3>
          </div>
          <p className="text-sm text-foreground-muted">Control how ShifaMind contacts you.</p>
          <button className="px-4 py-2 rounded-lg bg-secondary border border-border text-sm text-foreground hover:bg-secondary transition-colors">
            Preferences
          </button>
        </GlassCard>
      </div>

      <GlassCard className="space-y-4 border-l-4 border-l-destructive">
        <h3 className="font-medium text-foreground">Danger Zone</h3>
        <p className="text-sm text-foreground-muted">These actions are permanent and cannot be undone.</p>
        <button className="px-4 py-2 rounded-lg bg-destructive/20 border border-destructive/30 text-sm text-destructive hover:bg-destructive/30 transition-colors">
          Delete Account
        </button>
      </GlassCard>
    </div>
  )
}
