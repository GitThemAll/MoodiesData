"use client"

import { useState, useEffect } from "react"
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

interface DistributionData {
  range: string
  count: number
}

export function CLVDistribution() {
  const [data, setData] = useState<DistributionData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        // Mock data - replace with actual API call
        const mockData: DistributionData[] = [
          { range: "€0-50", count: 120 },
          { range: "€0-100", count: 450 },
          { range: "€100-200", count: 280 },
          { range: "€200-500", count: 680 },
          { range: "€500+", count: 420 },
        ]

        // Simulate API delay
        await new Promise((resolve) => setTimeout(resolve, 800))
        setData(mockData)
      } catch (err) {
        console.error("Failed to fetch distribution data:", err)
        setError(err instanceof Error ? err.message : "Failed to fetch data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-500">Loading distribution data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-[400px]">
        <div className="text-center">
          <p className="text-sm text-red-500 mb-2">Error loading data</p>
          <p className="text-xs text-gray-400">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <XAxis dataKey="range" tick={{ fontSize: 12 }} axisLine={{ stroke: "#e5e7eb" }} />
        <YAxis tick={{ fontSize: 12 }} axisLine={{ stroke: "#e5e7eb" }} />
        <Tooltip
          formatter={(value) => [`${value} customers`, "Count"]}
          labelStyle={{ color: "#374151" }}
          contentStyle={{
            backgroundColor: "#f9fafb",
            border: "1px solid #e5e7eb",
            borderRadius: "6px",
          }}
        />
        <Bar dataKey="count" fill="#4ade80" radius={[4, 4, 0, 0]} name="Customers" />
      </BarChart>
    </ResponsiveContainer>
  )
}
