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
        'glass animate-fade-in',
        hover && 'glass-hover cursor-pointer transition-colors duration-200',
        onClick && 'cursor-pointer',
        className
      )}
    >
      {children}
    </div>
  )
}
