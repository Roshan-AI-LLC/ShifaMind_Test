"use client"

import Link from "next/link"
import { 
  FlaskConical, 
  MessageSquare, 
  History, 
  Brain,
  Activity,
  Zap,
  BarChart3,
  Clock
} from "lucide-react"
import { GlassCard } from "@/components/ui/glass-card"
import { StatsTrend } from "@/components/ui/stats-trend"
import { ActivityChart } from "@/components/ui/activity-chart"
import { cn } from "@/lib/utils"

// Mock data - will be replaced with real data
const stats = {
  predictions: 24,
  chatSessions: 8,
  accuracy: 94,
  avgConfidence: 87,
}

const weeklyActivity = [
  { day: "Mon", value: 3, max: 5 },
  { day: "Tue", value: 5, max: 5 },
  { day: "Wed", value: 2, max: 5 },
  { day: "Thu", value: 4, max: 5 },
  { day: "Fri", value: 5, max: 5 },
  { day: "Sat", value: 1, max: 5 },
  { day: "Sun", value: 0, max: 5 },
]

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
  const isFirstTime = stats.predictions === 0 && stats.chatSessions === 0

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Welcome heading */}
      <div className="animate-fade-in">
        <h1 className="text-2xl lg:text-3xl font-semibold text-foreground">
          Welcome back, Dr. Smith
        </h1>
        <p className="text-foreground-muted mt-1">
          Your clinical AI assistant is ready to help
        </p>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 animate-fade-in stagger-1">
        <StatsTrend
          label="Total Predictions"
          value={stats.predictions}
          icon={<Activity className="w-5 h-5" />}
          iconColor="teal"
          trend={{ direction: "up", percentage: 12, period: "vs last week" }}
        />
        <StatsTrend
          label="Chat Sessions"
          value={stats.chatSessions}
          icon={<MessageSquare className="w-5 h-5" />}
          iconColor="gold"
          trend={{ direction: "up", percentage: 3, period: "vs last week" }}
        />
        <StatsTrend
          label="Accuracy"
          value={`${stats.accuracy}%`}
          icon={<BarChart3 className="w-5 h-5" />}
          iconColor="green"
        />
        <StatsTrend
          label="Avg Confidence"
          value={`${stats.avgConfidence}%`}
          icon={<Clock className="w-5 h-5" />}
          iconColor="teal"
        />
      </div>

      {/* Activity Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 animate-fade-in stagger-2">
        <div className="lg:col-span-2">
          <ActivityChart 
            data={weeklyActivity}
            title="Weekly Predictions"
          />
        </div>
        <GlassCard className="space-y-4">
          <h3 className="font-medium text-foreground">Quick Stats</h3>
          <div className="space-y-3">
            <div>
              <p className="text-xs text-foreground-muted">Predictions/Day</p>
              <p className="text-2xl font-semibold text-primary mt-1">3.4</p>
            </div>
            <div className="pt-3 border-t border-white/[0.06]">
              <p className="text-xs text-foreground-muted">Most Active Day</p>
              <p className="text-sm font-medium text-foreground mt-1">Thursday</p>
            </div>
            <div className="pt-3 border-t border-white/[0.06]">
              <p className="text-xs text-foreground-muted">Streak</p>
              <p className="text-sm font-medium text-foreground mt-1">5 days</p>
            </div>
          </div>
        </GlassCard>
      </div>

      {/* Quick actions */}
      <div className="space-y-4">
        <h2 className="text-lg font-medium text-foreground">Quick Actions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map((action, index) => {
            const Icon = action.icon
            return (
              <Link key={action.href} href={action.href}>
                <GlassCard 
                  hover 
                  className={cn(
                    "h-full animate-fade-in",
                    `stagger-${index + 3}`
                  )}
                >
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

      {/* System status */}
      <GlassCard className="animate-fade-in stagger-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-white/[0.06] flex items-center justify-center">
            <Brain className="w-6 h-6 text-foreground-muted" />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <h3 className="text-foreground font-medium">BioClinicalBERT Model</h3>
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
            </div>
            <p className="text-foreground-muted text-sm">
              Model loaded and ready • ICD-10 prediction service active
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
