import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'History',
  description: 'Review past predictions and conversations',
}

export default function HistoryLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>
}
