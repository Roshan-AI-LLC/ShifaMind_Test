import { cn } from '@/lib/utils'

interface ConceptBadgeProps {
  concept: string
  score: number
  active?: boolean
  className?: string
}

function getBorderColor(score: number): string {
  if (score >= 0.7) return '#4ecdc4'
  if (score >= 0.4) return '#ffd93d'
  return 'rgba(255,255,255,0.2)'
}

export function ConceptBadge({ concept, score, active = true, className }: ConceptBadgeProps) {
  const borderColor = getBorderColor(score)

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium',
        'border-l-2 bg-white/[0.04] border border-white/[0.06]',
        !active && 'opacity-30',
        className
      )}
      style={{ borderLeftColor: borderColor }}
    >
      <span className="text-white/80">{concept}</span>
      <span className="font-mono opacity-60" style={{ color: borderColor }}>
        {(score * 100).toFixed(0)}%
      </span>
    </span>
  )
}
