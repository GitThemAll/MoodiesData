"use client"

import { useState, useEffect } from "react"
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"

interface DistributionData {
  range: string
  count: number
}

interface ApiResponse {
  distribution: {
    [key: string]: number
  }
}

export function CLVDistribution() {
  const [data, setData] = useState<DistributionData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch("http://localhost:5000/clv/lifetime_clv_distribution")

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const result: ApiResponse = await response.json()

        if (result.distribution) {
          // Convert the distribution object to array format for the chart
          // Define the correct order based on the expected API response
          const rangeOrder = ["0-50", "50-100", "100-200", "200-300", "300-400", "400-500", "500+"]

          const distributionArray = rangeOrder
            .filter((range) => result.distribution[range] !== undefined) // Only include ranges that exist in the data
            .map((range) => ({
              range: range, // Keep the original range format from API
              count: result.distribution[range],
            }))

          // Also include any ranges from the API that might not be in our predefined order
          Object.keys(result.distribution).forEach((range) => {
            if (!rangeOrder.includes(range)) {
              distributionArray.push({
                range: range,
                count: result.distribution[range],
              })
            }
          })

          console.log("CLV Distribution data:", distributionArray)
          console.log("Original API response:", result.distribution)
          setData(distributionArray)
        } else {
          throw new Error("Invalid response format - missing distribution")
        }
      } catch (err) {
        console.error("Failed to fetch CLV distribution data:", err)
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

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[400px]">
        <p className="text-sm text-gray-500">No distribution data available</p>
      </div>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 60, bottom: 80 }}>
        <XAxis
          dataKey="range"
          tick={{ fontSize: 12 }}
          axisLine={{ stroke: "#e5e7eb" }}
          angle={-45}
          textAnchor="end"
          height={60}
          label={{
            value: "CLV Range ($)",
            position: "insideBottom",
            offset: -10,
            style: { textAnchor: "middle", fontSize: "14px", fontWeight: "500" },
          }}
        />
        <YAxis
          tick={{ fontSize: 12 }}
          axisLine={{ stroke: "#e5e7eb" }}
          label={{
            value: "Number of Customers",
            angle: -90,
            position: "insideLeft",
            style: { textAnchor: "middle", fontSize: "14px", fontWeight: "500" },
          }}
        />
        <Tooltip
          formatter={(value) => [`${value} customers`, "Count"]}
          labelFormatter={(label) => `CLV Range: $${label}`}
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
