"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface ConceptBadgeProps {
  /** Concept label from the API; may be missing on some records. */
  name?: string | null
  /** Gate value, 0-1. Rendered as a percentage. */
  score?: number
  /**
   * Signed contribution to a code's logit. When provided this is shown INSTEAD
   * of `score`, because a contribution is not a percentage: it is the exact
   * per-concept term in `logit = bias + sum(contributions)` and it is unbounded.
   * Rendering +2.708 as "271%" would be a lie, and a negative contribution has
   * no percentage reading at all.
   */
  contribution?: number
  showScore?: boolean
  size?: "sm" | "md"
  className?: string
}

function formatConceptName(name: string | null | undefined): string {
  if (name == null || name === "") return ""
  return name.replace(/_/g, " ")
}

const ConceptBadge = React.forwardRef<HTMLSpanElement, ConceptBadgeProps>(
  ({ name, score = 0, contribution, showScore = true, size = "md", className }, ref) => {
    const signed = contribution !== undefined
    const against = signed && contribution < 0
    // |contribution| >= 1 is roughly where a concept stops being incidental.
    const strong = signed ? Math.abs(contribution) >= 1 : score >= 0.7

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
          against
            ? "bg-secondary text-foreground-muted border border-dashed border-border"
            : strong
              ? "bg-gradient-to-r from-primary/30 to-primary/20 text-foreground border border-primary/30"
              : "bg-secondary text-foreground-muted border border-border",
          className
        )}
        title={
          signed
            ? `${against ? "Argues against" : "Supports"} this code. Contribution ${contribution.toFixed(3)}`
            : undefined
        }
      >
        <span className="capitalize">{formatConceptName(name) || "\u2014"}</span>
        {showScore && (
          <span
            className={cn(
              "font-mono",
              against
                ? "text-foreground-subtle"
                : strong
                  ? "text-primary"
                  : "text-foreground-subtle"
            )}
          >
            {signed
              ? `${contribution >= 0 ? "+" : "\u2212"}${Math.abs(contribution).toFixed(2)}`
              : `${Math.round(score * 100)}%`}
          </span>
        )}
      </span>
    )
  }
)
ConceptBadge.displayName = "ConceptBadge"

export { ConceptBadge }
