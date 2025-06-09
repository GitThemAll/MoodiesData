"use client"

import { useState, useEffect } from "react"
import { Badge } from "@/components/ui/badge"

interface DiscountData {
  discount_code: string
  revenue: string
  rank: number
}

interface ApiResponse {
  data: DiscountData[]
  status: string
}

export function TopDiscountRevenue() {
  const [data, setData] = useState<DiscountData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch("http://localhost:5000/insights/top-discount-revenue")

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result: ApiResponse = await response.json()

        if (result.status === "success" && result.data) {
          setData(result.data)
        } else {
          throw new Error("Invalid response format")
        }
      } catch (err) {
        console.error("Failed to fetch top discount codes:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch data")
        // Fallback data for demo
        setData([
          { discount_code: "SUMMER25", revenue: "$67,890", rank: 1 },
          { discount_code: "WELCOME10", revenue: "$54,320", rank: 2 },
          { discount_code: "FLASH50", revenue: "$43,210", rank: 3 },
          { discount_code: "LOYALTY15", revenue: "$38,950", rank: 4 },
          { discount_code: "NEWBIE20", revenue: "$32,670", rank: 5 },
        ])
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[280px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-500">Loading top discount codes...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-[280px]">
        <div className="text-center">
          <p className="text-sm text-red-500 mb-2">Error loading data</p>
          <p className="text-xs text-gray-400">{error}</p>
        </div>
      </div>
    )
  }

  const getRankColor = (rank: number) => {
    switch (rank) {
      case 1:
        return "bg-yellow-500 text-white"
      case 2:
        return "bg-gray-400 text-white"
      case 3:
        return "bg-orange-600 text-white"
      default:
        return "bg-purple-500 text-white"
    }
  }

  return (
    <div className="space-y-4">
      <div className="text-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Top 5 Discount Codes by Revenue</h3>
        <p className="text-sm text-gray-500">Most profitable discount campaigns</p>
      </div>

      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.discount_code} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <Badge
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${getRankColor(item.rank)}`}
              >
                {item.rank}
              </Badge>
              <div>
                <p className="font-medium text-gray-900">{item.discount_code}</p>
                <p className="text-sm text-gray-500">Discount Code</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-lg font-bold text-green-600">{item.revenue}</p>
              <p className="text-xs text-gray-500">Total Revenue</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
