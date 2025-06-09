"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Users, DollarSign, TrendingUp } from "lucide-react"

interface ClusterCardData {
  conversion_rate: string
  customer_count: number
  label: string
  total_revenue: string
}

interface ApiResponse {
  data: ClusterCardData[]
  status: string
}

// Color mapping for different clusters
const getClusterColor = (label: string) => {
  const colorMap: { [key: string]: string } = {
    "Cluster -1": "bg-gray-500",
    "NL Dormant Value Buyers": "bg-orange-500",
    "Low-Intent Pay-Later Shoppers": "bg-yellow-500",
    "Highly Engaged Dutch Customers": "bg-purple-500",
    "Inactive Belgian Shoppers": "bg-green-500",
  }
  return colorMap[label] || "bg-blue-500"
}

export function ClusterCards() {
  const [data, setData] = useState<ClusterCardData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch("http://localhost:5000/ml/clustering-cards-metrics")

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
        console.error("Failed to fetch cluster cards data:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
              </CardTitle>
              <div className="h-3 w-3 bg-gray-200 rounded-full animate-pulse" />
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
              <div className="h-6 bg-gray-200 rounded animate-pulse"></div>
              <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <p className="text-sm text-red-500 mb-2">Error loading cluster data</p>
          <p className="text-xs text-gray-400">{error}</p>
        </div>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center p-8">
        <p className="text-sm text-gray-500">No cluster data available</p>
      </div>
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {data.map((cluster) => (
        <Card key={cluster.label}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{cluster.label}</CardTitle>
            <div className={`h-3 w-3 rounded-full ${getClusterColor(cluster.label)}`} />
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center space-x-2">
              <Users className="h-4 w-4 text-muted-foreground" />
              <span className="text-2xl font-bold">{cluster.customer_count.toLocaleString()}</span>
            </div>
            <div className="flex items-center space-x-2">
              <DollarSign className="h-4 w-4 text-muted-foreground" />
              <span className="text-lg font-semibold">{cluster.total_revenue}</span>
            </div>
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">{cluster.conversion_rate} conversion rate</span>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
