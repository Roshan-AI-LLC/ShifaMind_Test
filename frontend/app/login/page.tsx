"use client"

import * as React from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Brain, Mail, Lock, ArrowRight, Sparkles, ArrowLeft } from "lucide-react"
import { AmbientBackground } from "@/components/ambient-background"
import { GlassCard } from "@/components/ui/glass-card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { cn } from "@/lib/utils"

type AuthMode = "password" | "magic-link"

export default function LoginPage() {
  const router = useRouter()
  const [mode, setMode] = React.useState<AuthMode>("password")
  const [email, setEmail] = React.useState("")
  const [password, setPassword] = React.useState("")
  const [isLoading, setIsLoading] = React.useState(false)
  const [magicLinkSent, setMagicLinkSent] = React.useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))

    if (mode === "magic-link") {
      setMagicLinkSent(true)
      setIsLoading(false)
    } else {
      // For demo, just redirect to dashboard
      router.push("/dashboard")
    }
  }

  const handleDemoLogin = () => {
    setEmail("demo@shifamind.me")
    setPassword("demo123")
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center p-4">
      <AmbientBackground />
      
      <div className="relative z-10 w-full max-w-md space-y-6 animate-fade-in">
        {/* Logo */}
        <div className="text-center space-y-3">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/20 border border-primary/30 shadow-[0_0_40px_rgba(78,205,196,0.3)]">
            <Brain className="w-8 h-8 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-semibold text-foreground">ShifaMind</h1>
            <p className="text-foreground-muted text-sm mt-1">Clinical AI Diagnosis Platform</p>
          </div>
        </div>

        {/* Login Card */}
        <GlassCard className="relative overflow-hidden" glow="teal">
          {/* Mode toggle */}
          <div className="flex p-1 mb-6 bg-white/[0.04] rounded-xl">
            <button
              type="button"
              onClick={() => { setMode("password"); setMagicLinkSent(false); }}
              className={cn(
                "flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200",
                mode === "password" 
                  ? "bg-white/[0.08] text-foreground" 
                  : "text-foreground-muted hover:text-foreground"
              )}
            >
              Password
            </button>
            <button
              type="button"
              onClick={() => { setMode("magic-link"); setMagicLinkSent(false); }}
              className={cn(
                "flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200",
                mode === "magic-link" 
                  ? "bg-white/[0.08] text-foreground" 
                  : "text-foreground-muted hover:text-foreground"
              )}
            >
              Magic Link
            </button>
          </div>

          {magicLinkSent ? (
            <div className="text-center py-6 space-y-4">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-primary/20">
                <Mail className="w-6 h-6 text-primary" />
              </div>
              <div>
                <h2 className="text-lg font-medium text-foreground">Check your email</h2>
                <p className="text-foreground-muted text-sm mt-1">
                  We&apos;ve sent a magic link to <span className="text-foreground">{email}</span>
                </p>
              </div>
              <Button
                variant="ghost"
                onClick={() => setMagicLinkSent(false)}
                className="text-foreground-muted hover:text-foreground"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to login
              </Button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Email field */}
              <div className="space-y-2">
                <Label htmlFor="email" className="text-foreground-muted">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground-subtle" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="doctor@hospital.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="pl-10 bg-white/[0.04] border-white/[0.08] text-foreground placeholder:text-foreground-subtle focus:border-primary focus:ring-primary/20"
                  />
                </div>
              </div>

              {/* Password field (only for password mode) */}
              {mode === "password" && (
                <div className="space-y-2">
                  <Label htmlFor="password" className="text-foreground-muted">Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground-subtle" />
                    <Input
                      id="password"
                      type="password"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      className="pl-10 bg-white/[0.04] border-white/[0.08] text-foreground placeholder:text-foreground-subtle focus:border-primary focus:ring-primary/20"
                    />
                  </div>
                </div>
              )}

              {/* Submit button */}
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-medium shadow-[0_0_20px_rgba(78,205,196,0.3)] hover:shadow-[0_0_30px_rgba(78,205,196,0.4)] transition-all duration-200"
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                    {mode === "password" ? "Signing in..." : "Sending link..."}
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    {mode === "password" ? "Sign In" : "Send Magic Link"}
                    <ArrowRight className="w-4 h-4" />
                  </span>
                )}
              </Button>
            </form>
          )}
        </GlassCard>

        {/* Demo credentials card */}
        <GlassCard padding="sm" className="border-primary/20">
          <div className="flex items-start gap-3">
            <div className="shrink-0 w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground">Demo Access</p>
              <p className="text-xs text-foreground-muted mt-0.5">
                Use demo@shifamind.me / demo123 to explore
              </p>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleDemoLogin}
              className="shrink-0 text-primary hover:text-primary hover:bg-primary/10"
            >
              Use Demo
            </Button>
          </div>
        </GlassCard>

        {/* Back link */}
        <p className="text-center text-sm text-foreground-muted">
          <Link href="/" className="hover:text-foreground transition-colors inline-flex items-center gap-1">
            <ArrowLeft className="w-3 h-3" />
            Back to main site
          </Link>
        </p>
      </div>
    </div>
  )
}
