"use client"

import { Users, Database, Zap, TrendingUp } from "lucide-react"
import { StatsTrend } from "@/components/ui/stats-trend"

const adminStats = [
  {
    label: "Active Users",
    value: 247,
    icon: <Users className="w-5 h-5" />,
    iconColor: "teal" as const,
    trend: { direction: "up" as const, percentage: 18, period: "vs last month" },
  },
  {
    label: "Total Predictions",
    value: 3847,
    icon: <Database className="w-5 h-5" />,
    iconColor: "gold" as const,
    trend: { direction: "up" as const, percentage: 42, period: "vs last month" },
  },
  {
    label: "API Uptime",
    value: "99.8%",
    icon: <Zap className="w-5 h-5" />,
    iconColor: "teal" as const,
  },
  {
    label: "Model Version",
    value: "2.4.1",
    icon: <TrendingUp className="w-5 h-5" />,
    iconColor: "gold" as const,
  },
]

export function AdminStats() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {adminStats.map((stat, i) => (
        <div key={i} className={`animate-fade-in stagger-${i + 1}`}>
          <StatsTrend {...stat} />
        </div>
      ))}
    </div>
  )
}
