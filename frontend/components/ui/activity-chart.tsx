"use client"

import * as React from "react"
import { GlassCard } from "./glass-card"

interface ActivityData {
  day: string
  value: number
  max: number
}

interface ActivityChartProps {
  data: ActivityData[]
  title?: string
}

export function ActivityChart({ data, title = "Activity" }: ActivityChartProps) {
  const maxValue = Math.max(...data.map((d) => d.max))

  return (
    <GlassCard className="space-y-4">
      {title && <h3 className="font-medium text-foreground">{title}</h3>}
      <div className="space-y-2">
        {data.map((item) => {
          const percentage = (item.value / item.max) * 100
          return (
            <div key={item.day} className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="text-foreground-muted">{item.day}</span>
                <span className="text-foreground font-mono">{item.value}</span>
              </div>
              <div className="h-2 rounded-full bg-white/[0.06] overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-primary to-primary/70 rounded-full transition-all duration-500"
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          )
        })}
      </div>
    </GlassCard>
  )
}
