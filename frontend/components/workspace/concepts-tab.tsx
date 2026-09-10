"use client"

import { useState } from "react"

interface Concept {
  name: string
  /** Largest signed contribution this concept made to any predicted code. */
  contribution: number
  /** The code it moved most. */
  code: string
  codeTitle: string
  gate: number
  span: string | null
  assertion: string | null
}

interface Suppressed {
  concept: string
  name: string
  gate: number
  assertion: string | null
  spans: { surface: string; assertion: string }[]
}

interface ConceptsTabProps {
  concepts: Concept[]
  suppressed?: Suppressed[]
}

const ASSERTION_LABEL: Record<string, string> = {
  affirmed: "",
  negated: "negated",
  hypothetical: "hypothetical",
  family: "family history",
  historical: "historical",
}

const ASSERTION_WHY: Record<string, string> = {
  negated: "denied in the note",
  hypothetical: "being ruled out",
  family: "someone else's history",
  historical: "a prior encounter",
}

export function ConceptsTab({ concepts, suppressed = [] }: ConceptsTabProps) {
  const [showAll, setShowAll] = useState(false)
  const [showSuppressed, setShowSuppressed] = useState(false)

  // A concept contributing less than a hundredth of the strongest one is real
  // but numerically irrelevant. Hidden by default, one click away, never
  // silently dropped.
  const top = Math.abs(concepts[0]?.contribution ?? 0)
  const cutoff = top * 0.01
  const shown = showAll ? concepts : concepts.filter((c) => Math.abs(c.contribution) >= cutoff)
  const hidden = concepts.length - shown.length
  const maxAbs = Math.max(...concepts.map((c) => Math.abs(c.contribution)), 1e-6)

  if (concepts.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-foreground-muted">No concepts matched this note</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-start gap-3 p-3 rounded-lg bg-muted border border-border">
        <p className="text-sm text-foreground-muted">
          Ranked by the largest contribution each concept made to any predicted
          code. Positive supports the code, negative argues against it.
        </p>
      </div>

      <div className="space-y-1.5">
        {shown.map((c) => {
          const against = c.contribution < 0
          const pct = (Math.abs(c.contribution) / maxAbs) * 100
          return (
            <div
              key={c.name + c.code}
              className="p-3 rounded-lg bg-muted border border-border"
            >
              <div className="flex items-baseline justify-between gap-3">
                <span className="text-sm font-medium text-foreground capitalize">
                  {c.name.replace(/_/g, " ")}
                  {c.assertion && ASSERTION_LABEL[c.assertion] && (
                    <span className="ml-2 text-xs font-normal text-foreground-subtle">
                      {ASSERTION_LABEL[c.assertion]}
                    </span>
                  )}
                </span>
                <span
                  className={`text-sm font-mono shrink-0 ${
                    against ? "text-foreground-subtle" : "text-primary"
                  }`}
                >
                  {c.contribution >= 0 ? "+" : "\u2212"}
                  {Math.abs(c.contribution).toFixed(2)}
                </span>
              </div>

              <div className="mt-2 h-1 w-full rounded-full bg-secondary overflow-hidden">
                <div
                  className={`h-full rounded-full ${against ? "bg-foreground-subtle" : "bg-primary"}`}
                  style={{ width: `${Math.max(pct, 1)}%` }}
                />
              </div>

              <div className="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-foreground-muted">
                <span className="font-mono text-foreground-subtle">{c.code}</span>
                <span className="truncate">{c.codeTitle}</span>
                {c.span && (
                  <span className="text-foreground-subtle">
                    &middot; matched &ldquo;{c.span}&rdquo;
                  </span>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {hidden > 0 && (
        <button
          onClick={() => setShowAll(true)}
          className="w-full py-2 rounded-lg bg-secondary border border-border text-sm text-foreground-muted hover:text-foreground transition-colors"
        >
          Show {hidden} more with negligible contribution
        </button>
      )}
      {showAll && (
        <button
          onClick={() => setShowAll(false)}
          className="w-full py-2 rounded-lg bg-secondary border border-border text-sm text-foreground-muted hover:text-foreground transition-colors"
        >
          Hide negligible contributions
        </button>
      )}

      {suppressed.length > 0 && (
        <div className="pt-4 mt-4 border-t border-border">
          <button
            onClick={() => setShowSuppressed(!showSuppressed)}
            className="w-full text-left"
          >
            <div className="flex items-baseline justify-between gap-3">
              <span className="text-sm font-medium text-foreground">
                {suppressed.length} concepts found and suppressed
              </span>
              <span className="text-xs text-foreground-muted shrink-0">
                {showSuppressed ? "Hide" : "Show"}
              </span>
            </div>
            <p className="mt-1 text-xs text-foreground-muted">
              Mentioned in the note, then shut off by the model. Their gates
              closed, so they contributed nothing to any code.
            </p>
          </button>

          {showSuppressed && (
            <div className="mt-3 space-y-1.5">
              {suppressed.map((c) => (
                <div
                  key={c.concept}
                  className="p-2.5 rounded-lg bg-secondary border border-dashed border-border"
                >
                  <div className="flex items-baseline justify-between gap-3">
                    <span className="text-sm text-foreground-muted capitalize">
                      {c.name.replace(/_/g, " ")}
                    </span>
                    <span className="text-xs font-mono text-foreground-subtle shrink-0">
                      gate {c.gate.toFixed(3)}
                    </span>
                  </div>
                  <div className="mt-1 text-xs text-foreground-subtle">
                    {c.spans[0] && <>&ldquo;{c.spans[0].surface}&rdquo; &middot; </>}
                    {c.assertion
                      ? ASSERTION_WHY[c.assertion] ?? c.assertion
                      : "not asserted"}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
