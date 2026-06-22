"use client"

import { createContext, useContext, useEffect, useState, ReactNode } from "react"
import { User } from "@/types"
import { getMe } from "@/lib/api/auth"
import Cookies from "js-cookie"
import { useRouter } from "next/navigation"

interface AuthContextType {
  user: User | null
  isLoading: boolean
  logout: () => void
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: true,
  logout: () => {},
})

export function AuthProvider({ children, initialUser }: { children: ReactNode, initialUser?: User | null }) {
  const [user, setUser] = useState<User | null>(initialUser || null)
  const [isLoading, setIsLoading] = useState(!initialUser)
  const router = useRouter()

  useEffect(() => {
    if (initialUser) {
      setIsLoading(false)
      return
    }

    const fetchUser = async () => {
      try {
        const token = Cookies.get("astra_token")
        if (!token) throw new Error("No token")
        const userData = await getMe()
        setUser(userData)
      } catch (error) {
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }

    fetchUser()
  }, [initialUser])

  const logout = () => {
    Cookies.remove("astra_token")
    setUser(null)
    window.location.href = "/login"
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
