import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'
import { AppShell } from '@/components/layout/AppShell'

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) redirect('/login')

  const { data: doctor } = await supabase
    .from('doctors')
    .select('role')
    .eq('id', user.id)
    .single()

  if (doctor?.role !== 'admin') redirect('/dashboard')

  return (
    <AppShell isAdmin>{children}</AppShell>
  )
}
