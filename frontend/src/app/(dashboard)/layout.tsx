import { Sidebar } from "@/components/layout/sidebar"
import { TopNav } from "@/components/layout/top-nav"
import { AuthProvider } from "@/components/providers/auth-provider"
import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import { getMe } from "@/lib/api/auth"

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const cookieStore = await cookies()
  const token = cookieStore.get("astra_token")?.value

  if (!token) {
    redirect("/login")
  }

  let user = null
  try {
    user = await getMe(token)
  } catch (error) {
    // Token is invalid or expired
    redirect("/login")
  }

  return (
    <AuthProvider initialUser={user}>
      <div className="flex h-screen overflow-hidden bg-background">
        <Sidebar />
        <div className="flex flex-col flex-1 overflow-hidden">
          <TopNav />
          <main className="flex-1 overflow-y-auto p-6">
            {children}
          </main>
        </div>
      </div>
    </AuthProvider>
  )
}
