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

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className="flex-1 h-1.5 rounded-full bg-white/[0.06] overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${pct}%`, background: color }}
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
