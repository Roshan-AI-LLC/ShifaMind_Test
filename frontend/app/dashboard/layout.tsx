import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'
import { Sidebar } from '@/components/layout/Sidebar'
import { Header } from '@/components/layout/Header'

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

  // Check admin role for admin routes
  const { data: doctor } = await supabase
    .from('doctors')
    .select('role')
    .eq('id', user.id)
    .single()

  const isAdmin = doctor?.role === 'admin'

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-deep)' }}>
      <Sidebar isAdmin={isAdmin} />
      <Header />
      {/* Main content — offset for sidebar (64px) + header (64px) */}
      <main className="ml-16 pt-16 min-h-screen">
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  )
}
