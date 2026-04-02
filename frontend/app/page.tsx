import Link from "next/link"
import { Brain, ArrowRight, Activity, Shield, Zap } from "lucide-react"
import { AmbientBackground } from "@/components/ambient-background"
import { GlassCard } from "@/components/ui/glass-card"
import { Button } from "@/components/ui/button"

const features = [
  {
    icon: Activity,
    title: "ICD-10 Prediction",
    description: "AI-powered diagnosis coding from clinical notes using BioClinicalBERT",
  },
  {
    icon: Zap,
    title: "Real-time Analysis",
    description: "Get instant predictions with confidence scores and contributing concepts",
  },
  {
    icon: Shield,
    title: "Clinical Context",
    description: "Chat with AI to explore diagnosis reasoning and clinical implications",
  },
]

export default function HomePage() {
  return (
    <div className="relative min-h-screen">
      <AmbientBackground />
      
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header */}
        <header className="flex items-center justify-between p-4 lg:p-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary/20 border border-primary/30 flex items-center justify-center">
              <Brain className="w-5 h-5 text-primary" />
            </div>
            <span className="font-semibold text-lg text-foreground">ShifaMind</span>
          </div>
          <Link href="/login">
            <Button variant="outline" className="border-white/[0.12] bg-white/[0.04] hover:bg-white/[0.08] text-foreground">
              Sign In
            </Button>
          </Link>
        </header>

        {/* Hero */}
        <main className="flex-1 flex items-center justify-center p-4 lg:p-8">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <div className="space-y-4 animate-fade-in">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-medium">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                </span>
                Powered by BioClinicalBERT
              </div>
              
              <h1 className="text-4xl lg:text-6xl font-semibold text-foreground text-balance leading-tight">
                Clinical AI for{" "}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-primary/70">
                  Smarter Diagnoses
                </span>
              </h1>
              
              <p className="text-lg lg:text-xl text-foreground-muted max-w-2xl mx-auto text-balance">
                Transform clinical notes into accurate ICD-10 predictions with explainable AI. 
                Built for clinicians who value precision and transparency.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in stagger-1">
              <Link href="/login">
                <Button 
                  size="lg" 
                  className="bg-primary hover:bg-primary/90 text-primary-foreground font-medium shadow-[0_0_30px_rgba(78,205,196,0.4)] hover:shadow-[0_0_40px_rgba(78,205,196,0.5)] transition-all"
                >
                  Get Started
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
              <Link href="/login">
                <Button 
                  variant="outline" 
                  size="lg"
                  className="border-white/[0.12] bg-white/[0.04] hover:bg-white/[0.08] text-foreground"
                >
                  Try Demo
                </Button>
              </Link>
            </div>

            {/* Features */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-12 animate-fade-in stagger-2">
              {features.map((feature, index) => {
                const Icon = feature.icon
                return (
                  <GlassCard 
                    key={feature.title} 
                    hover 
                    className={`text-left stagger-${index + 3}`}
                  >
                    <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center mb-4">
                      <Icon className="w-5 h-5 text-primary" />
                    </div>
                    <h3 className="text-foreground font-medium">{feature.title}</h3>
                    <p className="text-foreground-muted text-sm mt-1">{feature.description}</p>
                  </GlassCard>
                )
              })}
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="p-4 lg:p-6 text-center text-sm text-foreground-subtle">
          <p>© 2024 ShifaMind. Clinical AI Platform.</p>
        </footer>
      </div>
    </div>
  )
}
