"use client"

import { useState, useEffect } from "react"
import { Badge } from "@/components/ui/badge"

interface SkuData {
  sku: string
  revenue: string
  rank: number
}

export function TopSkusRevenue() {
  const [data, setData] = useState<SkuData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Format number as currency
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
    }).format(value)
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch("http://localhost:5000/insights/shopify/sku-revenue")

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result = await response.json()

        if (result.data) {
          // Convert the object to array and sort by revenue (descending)
          const skuArray = Object.entries(result.data)
            .map(([sku, revenue]) => ({
              sku,
              revenue: typeof revenue === "number" ? revenue : 0,
            }))
            .sort((a, b) => b.revenue - a.revenue)
            .slice(0, 5) // Get top 5
            .map((item, index) => ({
              sku: item.sku,
              revenue: formatCurrency(item.revenue),
              rank: index + 1,
            }))

          setData(skuArray)
        } else {
          throw new Error("Invalid response format")
        }
      } catch (err) {
        console.error("Failed to fetch top SKUs:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch data")
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
          <p className="text-sm text-gray-500">Loading top SKUs...</p>
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
        return "bg-blue-500 text-white"
    }
  }

  return (
    <div className="space-y-4">
      <div className="text-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Top 5 SKUs by Revenue</h3>
        <p className="text-sm text-gray-500">Highest performing products</p>
      </div>

      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.sku} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <Badge
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${getRankColor(item.rank)}`}
              >
                {item.rank}
              </Badge>
              <div>
                <p className="font-medium text-gray-900">{item.sku}</p>
                <p className="text-sm text-gray-500">Product SKU</p>
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
