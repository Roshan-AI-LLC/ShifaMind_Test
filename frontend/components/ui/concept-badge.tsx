"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface ConceptBadgeProps {
  /** Concept label from the API; may be missing on some records. */
  name?: string | null
  score?: number // 0-1
  showScore?: boolean
  size?: "sm" | "md"
  className?: string
}

function formatConceptName(name: string | null | undefined): string {
  if (name == null || name === "") return ""
  return name.replace(/_/g, " ")
}

const ConceptBadge = React.forwardRef<HTMLSpanElement, ConceptBadgeProps>(
  ({ name, score = 0, showScore = true, size = "md", className }, ref) => {
    const isHighScore = score >= 0.7
    const scorePercent = Math.round(score * 100)

    const sizeClasses = {
      sm: "px-2 py-0.5 text-xs",
      md: "px-3 py-1 text-sm",
    }

    return (
      <span
        ref={ref}
        className={cn(
          "inline-flex items-center gap-1.5 rounded-full font-medium transition-colors",
          sizeClasses[size],
          isHighScore
            ? "bg-gradient-to-r from-primary/30 to-primary/20 text-foreground border border-primary/30"
            : "bg-secondary text-foreground-muted border border-border",
          className
        )}
      >
        <span className="capitalize">
          {formatConceptName(name) || "—"}
        </span>
        {showScore && (
          <span className={cn(
            "font-mono",
            isHighScore ? "text-primary" : "text-foreground-subtle"
          )}>
            {scorePercent}%
          </span>
        )}
      </span>
    )
  }
)
ConceptBadge.displayName = "ConceptBadge"

export { ConceptBadge }
