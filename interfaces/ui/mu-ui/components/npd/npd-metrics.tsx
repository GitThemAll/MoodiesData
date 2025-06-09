"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function NPDMetrics() {
  const [metrics, setMetrics] = useState({
    highest: 25,
    lowest: 3,
    average: 12,
  })

  useEffect(() => {
    // Calculate metrics from the same mock data
    const mockData = [
      { days_to_purchase: 5 },
      { days_to_purchase: 12 },
      { days_to_purchase: 8 },
      { days_to_purchase: 15 },
      { days_to_purchase: 3 },
      { days_to_purchase: 21 },
      { days_to_purchase: 7 },
      { days_to_purchase: 18 },
      { days_to_purchase: 10 },
      { days_to_purchase: 14 },
      { days_to_purchase: 6 },
      { days_to_purchase: 25 },
      { days_to_purchase: 9 },
      { days_to_purchase: 16 },
      { days_to_purchase: 4 },
    ]

    const days = mockData.map((item) => item.days_to_purchase)
    const highest = Math.max(...days)
    const lowest = Math.min(...days)
    const average = Math.round(days.reduce((sum, day) => sum + day, 0) / days.length)

    setMetrics({ highest, lowest, average })
  }, [])

  return (
    <div className="grid gap-6 md:grid-cols-3">
      {/* Highest Next Purchase Date */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Highest Next Purchase Date</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center">
            <div className="text-4xl font-bold">{metrics.highest} Days</div>
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
            <div className="text-4xl font-bold">{metrics.lowest} Days</div>
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
            <div className="text-4xl font-bold">{metrics.average} Days</div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
