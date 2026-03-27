import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Chat',
  description: 'Clinical AI assistant grounded in your predictions',
}

export default function ChatLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>
}
