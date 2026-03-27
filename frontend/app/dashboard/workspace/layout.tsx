import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Workspace',
  description: 'Analyze clinical notes with Phase 1 ICD-10 predictions',
}

export default function WorkspaceLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>
}
