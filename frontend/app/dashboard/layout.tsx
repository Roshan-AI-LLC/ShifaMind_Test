import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'
import { AppShell } from '@/components/layout/AppShell'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  const { data: doctor } = await supabase
    .from('doctors')
    .select('role')
    .eq('id', user.id)
    .single()

  const isAdmin = doctor?.role === 'admin'

  return (
    <div className="min-h-screen relative" style={{ background: 'var(--bg-deep)' }}>
      {/* Ambient orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div
          className="absolute w-[500px] h-[500px] rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(78,205,196,0.12), transparent 70%)',
            top: '-5%', left: '-5%',
            filter: 'blur(80px)',
            animation: 'float 25s ease-in-out infinite',
          }}
        />
        <div
          className="absolute w-[400px] h-[400px] rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(167,139,250,0.07), transparent 70%)',
            bottom: '-10%', right: '-5%',
            filter: 'blur(80px)',
            animation: 'float 25s ease-in-out infinite',
            animationDelay: '-8s',
          }}
        />
      </div>
      <AppShell isAdmin={isAdmin}>{children}</AppShell>
    </div>
  )
}
