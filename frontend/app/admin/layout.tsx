import type { Metadata } from 'next'
import { AppShell } from '@/components/layout/AppShell'

export const metadata: Metadata = { title: 'Admin' }

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return <AppShell requireAdmin>{children}</AppShell>
}
