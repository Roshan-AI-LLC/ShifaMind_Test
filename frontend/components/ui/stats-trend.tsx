"use client"

import * as React from "react"
import { TrendingUp } from "lucide-react"
import { GlassCard } from "./glass-card"
import { cn } from "@/lib/utils"

interface StatsTrendProps {
  label: string
  value: number | string
  unit?: string
  trend?: {
    direction: "up" | "down"
    percentage: number
    period: string
  }
  icon?: React.ReactNode
  iconColor?: "teal" | "gold" | "red" | "green"
  variant?: "default" | "compact"
}

const iconColorMap = {
  teal: "text-primary bg-primary/20",
  gold: "text-gold bg-gold/20",
  red: "text-destructive bg-destructive/20",
  green: "text-green-400 bg-green-500/20",
}

export function StatsTrend({
  label,
  value,
  unit,
  trend,
  icon,
  iconColor = "teal",
  variant = "default",
}: StatsTrendProps) {
  if (variant === "compact") {
    return (
      <div className="text-center p-4 rounded-xl bg-white/[0.04]">
        {icon && <div className="flex justify-center mb-2">{icon}</div>}
        <p className="text-2xl font-semibold font-mono text-foreground">{value}</p>
        <p className="text-xs text-foreground-muted mt-1">{label}</p>
      </div>
    )
  }

  return (
    <GlassCard className="flex items-start gap-4">
      {icon && (
        <div className={cn("w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0", iconColorMap[iconColor])}>
          {icon}
        </div>
      )}
      <div className="flex-1">
        <p className="text-foreground-muted text-sm">{label}</p>
        <div className="flex items-baseline gap-2 mt-1">
          <p className="text-3xl font-semibold font-mono text-foreground">{value}</p>
          {unit && <p className="text-sm text-foreground-muted">{unit}</p>}
        </div>
        {trend && (
          <div className="flex items-center gap-1 mt-3">
            <TrendingUp
              className={cn(
                "w-4 h-4",
                trend.direction === "up" ? "text-green-400" : "text-destructive rotate-180"
              )}
            />
            <span
              className={cn(
                "text-xs font-medium",
                trend.direction === "up" ? "text-green-400" : "text-destructive"
              )}
            >
              {trend.direction === "up" ? "+" : "-"}
              {trend.percentage}% {trend.period}
            </span>
          </div>
        )}
      </div>
    </GlassCard>
  )
}
