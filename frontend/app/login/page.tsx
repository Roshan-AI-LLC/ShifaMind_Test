"use client"

import * as React from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Mail, Lock, ArrowRight, Sparkles, ArrowLeft } from "lucide-react"
import { AmbientBackground } from "@/components/ambient-background"
import { GlassCard } from "@/components/ui/glass-card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { cn } from "@/lib/utils"
import { createClient } from "@/lib/supabase"
import { requestAccess } from "./actions"

type AuthMode = "password" | "magic-link"

export default function LoginPage() {
  const router = useRouter()
  const [mode, setMode] = React.useState<AuthMode>("password")
  const [email, setEmail] = React.useState("")
  const [password, setPassword] = React.useState("")
  const [isLoading, setIsLoading] = React.useState(false)
  const [magicLinkSent, setMagicLinkSent] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  
  const [isRequestingAccess, setIsRequestingAccess] = React.useState(false)
  const [reqLoading, setReqLoading] = React.useState(false)
  const [reqSuccess, setReqSuccess] = React.useState(false)
  const [reqError, setReqError] = React.useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    const supabase = createClient()

    if (mode === "magic-link") {
      const basePath = process.env.NEXT_PUBLIC_BASE_PATH || ""
      const { error } = await supabase.auth.signInWithOtp({
        email,
        options: { emailRedirectTo: `${window.location.origin}${basePath}/dashboard` },
      })
      if (error) {
        setError(error.message)
      } else {
        setMagicLinkSent(true)
      }
    } else {
      const { error } = await supabase.auth.signInWithPassword({ email, password })
      if (error) {
        setError(error.message)
      } else {
        router.push("/dashboard")
        router.refresh()
      }
    }

    setIsLoading(false)
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center p-4">
      <AmbientBackground />

      <div className="relative z-10 w-full max-w-md space-y-6 enter-fade-up">
        {/* Logo + wordmark */}
        <div className="text-center flex flex-col items-center gap-3">
          <div className="enter-fade-up inline-flex items-center gap-2 rounded-full border border-subtle bg-glass px-3 py-1 text-[0.7rem] font-medium uppercase tracking-[0.14em] text-muted-foreground backdrop-blur">
            ShifaMind · A Roshan AI product
          </div>
          <div className="inline-flex items-center justify-center w-20 h-20 float-y">
            <img src="/icon_transparent.png" className="w-full h-full object-contain" alt="ShifaMind Logo" />
          </div>
          <div>
            <h1 className="font-display text-3xl font-bold tracking-[-0.02em] text-foreground">
              Welcome <span className="gradient-text">back</span>
            </h1>
            <p className="text-muted-foreground text-sm mt-1.5">
              Sign in to continue concept-grounded ICD-10 coding
            </p>
          </div>
        </div>

        {/* Login Card */}
        <GlassCard className="relative overflow-hidden enter-fade-up enter-d-1" glow="teal">
          {/* Mode toggle */}
          <div className="flex p-1 mb-6 bg-muted rounded-xl">
            <button
              type="button"
              onClick={() => { setMode("password"); setMagicLinkSent(false); setError(null) }}
              className={cn(
                "flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200",
                mode === "password"
                  ? "glass-strong text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              Password
            </button>
            <button
              type="button"
              onClick={() => { setMode("magic-link"); setMagicLinkSent(false); setError(null) }}
              className={cn(
                "flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200",
                mode === "magic-link"
                  ? "glass-strong text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
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
              {/* Error message */}
              {error && (
                <div className="px-4 py-3 rounded-lg bg-destructive/10 border border-destructive/30 text-sm text-destructive">
                  {error}
                </div>
              )}

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
                    className="pl-10 bg-glass border-subtle text-foreground placeholder:text-foreground-subtle focus:border-primary focus:ring-primary/20"
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
                      className="pl-10 bg-glass border-subtle text-foreground placeholder:text-foreground-subtle focus:border-primary focus:ring-primary/20"
                    />
                  </div>
                </div>
              )}

              {/* Submit button */}
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-medium ring-glow transition-all duration-200 hover:-translate-y-0.5"
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

        {/* Request Access Card */}
        <GlassCard padding="sm" className="border-primary/20">
          <div className="flex flex-col items-start gap-3">
            <div className="flex items-center gap-3 w-full">
              <div className="shrink-0 w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground">Need Access?</p>
                <p className="text-xs text-foreground-muted mt-0.5">
                  Request an invite to ShifaMind Platform
                </p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsRequestingAccess(!isRequestingAccess)}
                className="shrink-0 text-primary hover:text-primary hover:bg-primary/10"
              >
                {isRequestingAccess ? "Cancel" : "Request Access"}
              </Button>
            </div>
            
            {isRequestingAccess && (
              <div className="w-full pt-4 mt-2 border-t border-subtle animate-fade-in">
                {reqSuccess ? (
                  <div className="text-center py-4 space-y-2">
                    <div className="mx-auto w-10 h-10 rounded-full bg-green-500/20 flex items-center justify-center">
                      <Sparkles className="w-5 h-5 text-green-400" />
                    </div>
                    <p className="text-sm font-medium text-foreground">Request Sent!</p>
                    <p className="text-xs text-foreground-muted">We'll review it and get back to you shortly.</p>
                  </div>
                ) : (
                  <form 
                    className="space-y-4"
                    onSubmit={async (e) => {
                      e.preventDefault();
                      setReqLoading(true);
                      setReqError(null);
                      const fd = new FormData(e.currentTarget);
                      const res = await requestAccess(fd);
                      if (res.success) {
                        setReqSuccess(true);
                      } else {
                        setReqError(res.error || "An error occurred.");
                      }
                      setReqLoading(false);
                    }}
                  >
                    {reqError && (
                      <div className="px-3 py-2 rounded-lg bg-destructive/10 border border-destructive/30 text-xs text-destructive">
                        {reqError}
                      </div>
                    )}
                    <div className="space-y-2">
                      <Label htmlFor="req-name" className="text-xs text-foreground-muted">Full Name</Label>
                      <Input id="req-name" name="name" required disabled={reqLoading} className="h-8 text-sm bg-glass border-subtle" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="req-email" className="text-xs text-foreground-muted">Work Email</Label>
                      <Input id="req-email" name="email" type="email" required disabled={reqLoading} className="h-8 text-sm bg-glass border-subtle" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="req-org" className="text-xs text-foreground-muted">Organization</Label>
                      <Input id="req-org" name="organization" required disabled={reqLoading} className="h-8 text-sm bg-glass border-subtle" />
                    </div>
                    <Button type="submit" size="sm" disabled={reqLoading} className="w-full bg-primary hover:bg-primary/90 text-primary-foreground text-sm font-medium transition-all">
                      {reqLoading ? (
                        <span className="flex items-center gap-2">
                          <span className="w-3 h-3 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                          Sending...
                        </span>
                      ) : "Send Request"}
                    </Button>
                  </form>
                )}
              </div>
            )}
          </div>
        </GlassCard>

        {/* Back link */}
        <p className="text-center text-sm text-foreground-muted">
          <Link href="https://roshan-ai.com/products/shifamind/" className="hover:text-foreground transition-colors inline-flex items-center gap-1">
            <ArrowLeft className="w-3 h-3" />
            Back to main site
          </Link>
        </p>
      </div>
    </div>
  )
}
