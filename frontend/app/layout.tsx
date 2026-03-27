import type { Metadata } from 'next'
import { ToastProvider } from '@/components/shared/Toast'
import './globals.css'

export const metadata: Metadata = {
  title: {
    template: '%s — ShifaMind',
    default: 'ShifaMind Platform',
  },
  description: 'AI-assisted clinical decision support for physicians',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="min-h-screen antialiased" style={{ background: 'var(--bg-deep)' }}>
        <ToastProvider>
          {children}
        </ToastProvider>
      </body>
    </html>
  )
}
