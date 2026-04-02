"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  hover?: boolean
  glow?: "teal" | "gold" | "red" | "none"
  padding?: "none" | "sm" | "md" | "lg"
}

const GlassCard = React.forwardRef<HTMLDivElement, GlassCardProps>(
  ({ className, hover = false, glow = "none", padding = "md", children, ...props }, ref) => {
    const paddingClasses = {
      none: "",
      sm: "p-4",
      md: "p-6",
      lg: "p-8",
    }

    const glowClasses = {
      none: "",
      teal: "shadow-[0_0_30px_rgba(78,205,196,0.15)]",
      gold: "shadow-[0_0_30px_rgba(255,217,61,0.15)]",
      red: "shadow-[0_0_30px_rgba(255,107,107,0.15)]",
    }

    return (
      <div
        ref={ref}
        className={cn(
          "glass-card",
          paddingClasses[padding],
          glowClasses[glow],
          hover && "glass-card-hover cursor-pointer",
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)
GlassCard.displayName = "GlassCard"

export { GlassCard }
