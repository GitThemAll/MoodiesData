"use client"

import type React from "react"

import { useEffect, useState } from "react"
import { useRouter, usePathname } from "next/navigation"

interface AuthGuardProps {
  children: React.ReactNode
}

export function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter()
  const pathname = usePathname()
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null)

  useEffect(() => {
    const checkAuth = () => {
      // Check if user is on login or signup page
      const publicRoutes = ["/login", "/signup"]
      if (publicRoutes.includes(pathname)) {
        setIsAuthenticated(true)
        return
      }

      // Check for auth token in localStorage
      const token = localStorage.getItem("authToken")
      const user = localStorage.getItem("user")

      if (!token || !user) {
        // No auth data found, redirect to login
        router.push("/login")
        return
      }

      try {
        // Validate user data structure
        const userData = JSON.parse(user)
        if (!userData || (!userData.email && !userData.user?.email)) {
          // Invalid user data, redirect to login
          localStorage.removeItem("authToken")
          localStorage.removeItem("user")
          router.push("/login")
          return
        }

        // User is authenticated
        setIsAuthenticated(true)

        // If user is on root path and authenticated, redirect to dashboard
        if (pathname === "/") {
          router.push("/dashboard")
          return
        }
      } catch (error) {
        // Invalid user data format, redirect to login
        console.error("Invalid user data:", error)
        localStorage.removeItem("authToken")
        localStorage.removeItem("user")
        router.push("/login")
      }
    }

    checkAuth()
  }, [pathname, router])

  // Show loading while checking authentication
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-500">Checking authentication...</p>
        </div>
      </div>
    )
  }

  // Render children if authenticated or on public routes
  return <>{children}</>
}
