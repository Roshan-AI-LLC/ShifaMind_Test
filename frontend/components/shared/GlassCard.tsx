'use client'

import { cn } from '@/lib/utils'

interface GlassCardProps {
  children: React.ReactNode
  className?: string
  hover?: boolean
  onClick?: () => void
}

export function GlassCard({ children, className, hover = false, onClick }: GlassCardProps) {
  return (
    <div
      onClick={onClick}
      className={cn(
        'rounded-2xl animate-fade-in',
        hover && 'cursor-pointer transition-all duration-200',
        onClick && 'cursor-pointer',
        className
      )}
      style={{
        background: 'rgba(255, 255, 255, 0.04)',
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        boxShadow: '0 4px 24px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255,255,255,0.04)',
        ...(hover && { transition: 'background 0.2s, box-shadow 0.2s' }),
      }}
      onMouseEnter={hover ? e => {
        (e.currentTarget as HTMLDivElement).style.background = 'rgba(255,255,255,0.06)'
        ;(e.currentTarget as HTMLDivElement).style.boxShadow = '0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.06)'
      } : undefined}
      onMouseLeave={hover ? e => {
        (e.currentTarget as HTMLDivElement).style.background = 'rgba(255,255,255,0.04)'
        ;(e.currentTarget as HTMLDivElement).style.boxShadow = '0 4px 24px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.04)'
      } : undefined}
    >
      {children}
    </div>
  )
}
