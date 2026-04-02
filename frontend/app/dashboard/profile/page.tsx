"use client"

import { User, Mail, Building, Stethoscope, Shield, Activity, MessageSquare, Star, Zap, Key, Bell } from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { StatsTrend } from "@/components/ui/stats-trend"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

// Mock user data
const user = {
  name: "Dr. Sarah Smith",
  email: "sarah.smith@hospital.com",
  initials: "SS",
  specialty: "Internal Medicine",
  institution: "City General Hospital",
  role: "Physician",
  licenseNumber: "MD-2847362",
  memberSince: "January 2024",
  lastLogin: "Today at 2:45 PM",
  stats: {
    predictions: 24,
    chatSessions: 8,
    reviews: 12,
  },
  subscriptionTier: "Pro",
  features: [
    { name: "Unlimited Predictions", icon: Zap },
    { name: "Advanced Analytics", icon: Activity },
    { name: "Priority Support", icon: Zap },
  ]
}

export default function ProfilePage() {
  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-semibold text-foreground">Profile</h1>

      {/* Avatar card */}
      <GlassCard className="flex items-center gap-6">
        <Avatar className="w-20 h-20 bg-primary/20 border-2 border-primary/30">
          <AvatarFallback className="text-2xl font-semibold text-primary bg-transparent">
            {user.initials}
          </AvatarFallback>
        </Avatar>
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-semibold text-foreground">{user.name}</h2>
            <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-gold/20 text-gold border border-gold/30">
              Demo
            </span>
          </div>
          <div className="flex items-center gap-2 mt-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/20 text-primary border border-primary/30">
              {user.role}
            </span>
            <span className="text-sm text-foreground-muted">Member since {user.memberSince}</span>
          </div>
        </div>
      </GlassCard>

      {/* Details card */}
      <GlassCard className="space-y-4">
        <h3 className="font-medium text-foreground">Account Details</h3>
        <div className="space-y-3">
          <div className="flex items-center gap-3 py-2 border-b border-white/[0.06]">
            <Mail className="w-4 h-4 text-foreground-subtle" />
            <span className="text-sm text-foreground-muted w-24">Email</span>
            <span className="text-sm text-foreground">{user.email}</span>
          </div>
          <div className="flex items-center gap-3 py-2 border-b border-white/[0.06]">
            <Stethoscope className="w-4 h-4 text-foreground-subtle" />
            <span className="text-sm text-foreground-muted w-24">Specialty</span>
            <span className="text-sm text-foreground">{user.specialty}</span>
          </div>
          <div className="flex items-center gap-3 py-2 border-b border-white/[0.06]">
            <Building className="w-4 h-4 text-foreground-subtle" />
            <span className="text-sm text-foreground-muted w-24">Institution</span>
            <span className="text-sm text-foreground">{user.institution}</span>
          </div>
          <div className="flex items-center gap-3 py-2">
            <Shield className="w-4 h-4 text-foreground-subtle" />
            <span className="text-sm text-foreground-muted w-24">Role</span>
            <span className="text-sm text-foreground">{user.role}</span>
          </div>
        </div>
      </GlassCard>

      {/* Activity stats */}
      <div className="grid grid-cols-3 gap-4">
        <StatsTrend
          label="Predictions"
          value={user.stats.predictions}
          icon={<Activity className="w-5 h-5" />}
          iconColor="teal"
          variant="compact"
        />
        <StatsTrend
          label="Chat Sessions"
          value={user.stats.chatSessions}
          icon={<MessageSquare className="w-5 h-5" />}
          iconColor="gold"
          variant="compact"
        />
        <StatsTrend
          label="Reviews"
          value={user.stats.reviews}
          icon={<Star className="w-5 h-5" />}
          iconColor="red"
          variant="compact"
        />
      </div>

      {/* Subscription & Features */}
      <GlassCard className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-medium text-foreground">Subscription</h3>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-primary/20 text-primary border border-primary/30">
            {user.subscriptionTier}
          </span>
        </div>
        <p className="text-sm text-foreground-muted">
          You have access to all Pro features. Renews on February 1, 2025.
        </p>
        <button className="px-4 py-2 rounded-lg bg-primary/20 border border-primary/30 text-sm text-primary hover:bg-primary/30 transition-colors">
          Manage Subscription
        </button>
      </GlassCard>

      {/* Security & Preferences */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <GlassCard className="space-y-4">
          <div className="flex items-center gap-2">
            <Key className="w-5 h-5 text-primary" />
            <h3 className="font-medium text-foreground">Security</h3>
          </div>
          <p className="text-sm text-foreground-muted">
            Manage your authentication and security settings.
          </p>
          <button className="px-4 py-2 rounded-lg bg-white/[0.06] border border-white/[0.08] text-sm text-foreground hover:bg-white/[0.1] transition-colors">
            Update Password
          </button>
        </GlassCard>

        <GlassCard className="space-y-4">
          <div className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-gold" />
            <h3 className="font-medium text-foreground">Notifications</h3>
          </div>
          <p className="text-sm text-foreground-muted">
            Control how ShifaMind contacts you.
          </p>
          <button className="px-4 py-2 rounded-lg bg-white/[0.06] border border-white/[0.08] text-sm text-foreground hover:bg-white/[0.1] transition-colors">
            Preferences
          </button>
        </GlassCard>
      </div>

      {/* Additional info */}
      <GlassCard className="space-y-4">
        <h3 className="font-medium text-foreground">Additional Information</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2 border-b border-white/[0.06]">
            <span className="text-sm text-foreground-muted">Last Login</span>
            <span className="text-sm text-foreground">{user.lastLogin}</span>
          </div>
          <div className="flex items-center justify-between py-2 border-b border-white/[0.06]">
            <span className="text-sm text-foreground-muted">License #</span>
            <span className="text-sm text-foreground font-mono">{user.licenseNumber}</span>
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-sm text-foreground-muted">API Key</span>
            <button className="text-xs px-2 py-1 rounded bg-white/[0.06] hover:bg-white/[0.1] transition-colors text-foreground">
              Generate
            </button>
          </div>
        </div>
      </GlassCard>

      {/* Danger Zone */}
      <GlassCard className="space-y-4 border-l-4 border-l-destructive">
        <h3 className="font-medium text-foreground">Danger Zone</h3>
        <p className="text-sm text-foreground-muted">
          These actions are permanent and cannot be undone.
        </p>
        <button className="px-4 py-2 rounded-lg bg-destructive/20 border border-destructive/30 text-sm text-destructive hover:bg-destructive/30 transition-colors">
          Delete Account
        </button>
      </GlassCard>
    </div>
  )
}
