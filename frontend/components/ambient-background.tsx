"use client"

export function AmbientBackground() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
      {/* Deep background */}
      <div className="absolute inset-0 bg-background" />

      {/* Faint brand grid (masked at the top, like the website) */}
      <div className="absolute inset-0 grid-bg opacity-60" />

      {/* Aurora wash — theme-aware, matches roshan-ai.com hero */}
      <div className="absolute inset-x-0 top-[-10%] flex justify-center">
        <div className="aurora h-[520px] w-[1100px] max-w-full" />
      </div>

      {/* Soft accent orb - bottom right for depth */}
      <div
        className="absolute -bottom-[20%] -right-[10%] w-[50%] h-[50%] rounded-full animate-float-delayed animate-glow-pulse"
        style={{
          background:
            "radial-gradient(circle, color-mix(in oklab, var(--accent-warm) 12%, transparent) 0%, transparent 70%)",
          animationDelay: "-12s",
        }}
      />

      {/* Noise texture overlay */}
      <div className="absolute inset-0 noise-overlay" />
    </div>
  )
}
