import { AppShell } from "@/components/app-shell"

// Mock user for now - will be replaced with real auth
const mockUser = {
  name: "Dr. Smith",
  email: "smith@hospital.com",
  initials: "DS",
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <AppShell 
      user={mockUser}
      isAdmin={false}
      isDemoMode={true}
    >
      {children}
    </AppShell>
  )
}
