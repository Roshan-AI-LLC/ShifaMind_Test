"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface ConfidenceBarProps {
  value: number // 0-100
  showLabel?: boolean
  size?: "sm" | "md" | "lg"
  className?: string
}

function getColorByValue(value: number): string {
  if (value >= 70) return "bg-primary" // teal
  if (value >= 40) return "bg-gold" // gold
  return "bg-foreground-subtle" // gray
}

const ConfidenceBar = React.forwardRef<HTMLDivElement, ConfidenceBarProps>(
  ({ value, showLabel = false, size = "md", className }, ref) => {
    const clampedValue = Math.min(100, Math.max(0, value))
    
    const sizeClasses = {
      sm: "h-1",
      md: "h-2",
      lg: "h-3",
    }

    return (
      <div ref={ref} className={cn("flex items-center gap-3", className)}>
        <div 
          className={cn(
            "flex-1 rounded-full bg-white/[0.08] overflow-hidden",
            sizeClasses[size]
          )}
        >
          <div
            className={cn(
              "h-full rounded-full transition-all duration-600 ease-out",
              getColorByValue(clampedValue)
            )}
            style={{ width: `${clampedValue}%` }}
          />
        </div>
        {showLabel && (
          <span className="font-mono text-sm text-foreground-muted min-w-[3rem] text-right">
            {clampedValue.toFixed(0)}%
          </span>
        )}
      </div>
    )
  }
)
ConfidenceBar.displayName = "ConfidenceBar"

export { ConfidenceBar }
