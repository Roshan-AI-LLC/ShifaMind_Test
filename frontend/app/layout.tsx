import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'ShifaMind Platform',
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
        {children}
      </body>
    </html>
  )
}
