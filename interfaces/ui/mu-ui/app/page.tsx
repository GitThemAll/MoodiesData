"use client"

import { redirect } from "next/navigation"

export default function HomePage() {
  // Simple server-side redirect to dashboard
  redirect("/dashboard")
}
