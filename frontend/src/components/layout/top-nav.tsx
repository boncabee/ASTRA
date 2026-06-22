"use client"

import { useTheme } from "next-themes"
import { Moon, Sun, User as UserIcon, LogOut } from "lucide-react"
import { useAuth } from "@/components/providers/auth-provider"

export function TopNav() {
  const { theme, setTheme } = useTheme()
  const { user, logout } = useAuth()

  return (
    <header className="h-14 border-b border-border bg-card flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-muted-foreground hidden sm:inline-block">
          Enterprise-Grade Self-Hosted Security
        </span>
      </div>
      
      <div className="flex items-center gap-4">
        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-9 w-9"
        >
          <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </button>

        {user && (
          <div className="flex items-center gap-3 border-l border-border pl-4">
            <div className="flex flex-col items-end hidden sm:flex">
              <span className="text-sm font-medium leading-none">{user.username}</span>
              <span className="text-xs text-muted-foreground mt-1">{user.role}</span>
            </div>
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-secondary">
              <UserIcon className="h-4 w-4" />
            </div>
            <button 
              onClick={logout}
              className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring hover:bg-destructive hover:text-destructive-foreground h-9 px-3"
            >
              <LogOut className="h-4 w-4 mr-2" />
              Log out
            </button>
          </div>
        )}
      </div>
    </header>
  )
}
