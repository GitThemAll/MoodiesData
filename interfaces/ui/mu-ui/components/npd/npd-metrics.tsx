"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface NPDStats {
  average_next_purchase_days: number
  highest_next_purchase_days: number
  lowest_next_purchase_days: number
}

export function NPDMetrics() {
  const [metrics, setMetrics] = useState<NPDStats>({
    highest_next_purchase_days: 0,
    lowest_next_purchase_days: 0,
    average_next_purchase_days: 0,
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch("http://localhost:5000/npd-stats")

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result: NPDStats = await response.json()
        setMetrics(result)
      } catch (err) {
        console.error("Failed to fetch NPD stats:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="grid gap-6 md:grid-cols-3">
        {[...Array(3)].map((_, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle className="text-lg">
                <div className="h-6 bg-gray-200 rounded animate-pulse"></div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center">
                <div className="h-12 bg-gray-200 rounded animate-pulse"></div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="grid gap-6 md:grid-cols-3">
        {[...Array(3)].map((_, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle className="text-lg">NPD Metric</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center">
                <div className="text-sm text-red-500">Error loading data</div>
                <div className="text-xs text-gray-400 mt-1">{error}</div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  return (
    <div className="grid gap-6 md:grid-cols-3">
      {/* Highest Next Purchase Date */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Highest Next Purchase Date</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center">
            <div className="text-4xl font-bold">{metrics.highest_next_purchase_days} Days</div>
          </div>
        </CardContent>
      </Card>

      {/* Lowest Next Purchase Date */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Lowest Next Purchase Date</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center">
            <div className="text-4xl font-bold">{metrics.lowest_next_purchase_days} Days</div>
          </div>
        </CardContent>
      </Card>

      {/* Average Next Purchase Date */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Avg. Next Purchase Date</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center">
            <div className="text-4xl font-bold">{metrics.average_next_purchase_days} Days</div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
