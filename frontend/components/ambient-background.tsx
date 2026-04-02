"use client"

export function AmbientBackground() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
      {/* Deep background */}
      <div className="absolute inset-0 bg-background" />
      
      {/* Teal orb - top left */}
      <div 
        className="absolute -top-[20%] -left-[10%] w-[60%] h-[60%] rounded-full animate-float animate-glow-pulse"
        style={{
          background: "radial-gradient(circle, rgba(78, 205, 196, 0.15) 0%, rgba(78, 205, 196, 0.05) 40%, transparent 70%)",
        }}
      />
      
      {/* Red orb - bottom right */}
      <div 
        className="absolute -bottom-[20%] -right-[10%] w-[50%] h-[50%] rounded-full animate-float-delayed animate-glow-pulse"
        style={{
          background: "radial-gradient(circle, rgba(255, 107, 107, 0.12) 0%, rgba(255, 107, 107, 0.04) 40%, transparent 70%)",
          animationDelay: "-12s",
        }}
      />
      
      {/* Noise texture overlay */}
      <div className="absolute inset-0 noise-overlay" />
    </div>
  )
}
