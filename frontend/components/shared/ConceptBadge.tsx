import { cn } from '@/lib/utils'

interface ConceptBadgeProps {
  concept: string
  score: number
  active?: boolean
  className?: string
}

function getAccentColor(score: number): string {
  if (score >= 0.7) return '#4ecdc4'
  if (score >= 0.4) return '#ffd93d'
  return 'rgba(255,255,255,0.3)'
}

export function ConceptBadge({ concept, score, active = true, className }: ConceptBadgeProps) {
  const accent = getAccentColor(score)
  const isHigh = score >= 0.7

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium',
        !active && 'opacity-30',
        className
      )}
      style={{
        background: isHigh
          ? `linear-gradient(90deg, rgba(78,205,196,${(score * 0.25).toFixed(2)}), rgba(78,205,196,${(score * 0.45).toFixed(2)}))`
          : 'rgba(255,255,255,0.04)',
        border: `1px solid ${accent}30`,
        borderLeft: `2px solid ${accent}`,
      }}
    >
      <span style={{ color: isHigh ? 'rgba(255,255,255,0.9)' : 'rgba(255,255,255,0.7)' }}>
        {concept.replace(/_/g, ' ')}
      </span>
      <span className="font-mono" style={{ color: accent, opacity: 0.85 }}>
        {(score * 100).toFixed(0)}%
      </span>
    </span>
  )
}
