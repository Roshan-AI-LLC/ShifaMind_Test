'use client'

import { useEffect, useState } from 'react'
import { cn } from '@/lib/utils'

interface ConfidenceBarProps {
  value: number // 0–1
  showLabel?: boolean
  className?: string
}

function getConfidenceColor(value: number): string {
  if (value >= 0.7) return '#4ecdc4'
  if (value >= 0.4) return '#ffd93d'
  return 'rgba(255,255,255,0.3)'
}

export function ConfidenceBar({ value, showLabel = true, className }: ConfidenceBarProps) {
  const pct = Math.round(value * 100)
  const color = getConfidenceColor(value)
  const [width, setWidth] = useState(0)

  useEffect(() => {
    // rAF ensures the 0→pct transition actually plays
    const id = requestAnimationFrame(() => setWidth(pct))
    return () => cancelAnimationFrame(id)
  }, [pct])

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className="flex-1 h-1.5 rounded-full bg-white/[0.06] overflow-hidden">
        <div
          className="h-full rounded-full"
          style={{
            width: `${width}%`,
            background: color,
            transition: 'width 600ms cubic-bezier(0.16, 1, 0.3, 1)',
          }}
        />
      </div>
      {showLabel && (
        <span
          className="text-xs font-mono w-9 text-right shrink-0"
          style={{ color }}
        >
          {pct}%
        </span>
      )}
    </div>
  )
}
